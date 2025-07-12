# app.py
import os
import key # Assuming key.py contains your API key

os.environ["GOOGLE_API_KEY"] = key.OPENAI_API_KEY

############################################################

from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from operator import itemgetter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda


# --- Database connection and introspection test (keep this for initial checks) ---
try:
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_base.db")
    db = SQLDatabase.from_uri(f"sqlite:///{db_path}")

    print("--- Database Connection Check ---")
    print(f"Database dialect: {db.dialect}")
    usable_tables = db.get_usable_table_names()
    print(f"Usable table names: {usable_tables}")
    if "clientes" in usable_tables:
        print("Attempting to query 'clientes' table directly...")
        test_query_result = db.run("SELECT id, nombre, apellido FROM clientes LIMIT 3;")
        print(f"Direct query result from 'clientes': {test_query_result}")
    else:
        print("Table 'clientes' not found by LangChain.")
except Exception as e:
    print(f"ERROR: Failed to connect to or introspect database: {e}")
    exit()
print("--- End Database Connection Check ---")
# --- End database connection check ---


llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0,
)

# Your existing chain definitions
execute_query = QuerySQLDataBaseTool(db=db)
write_query = create_sql_query_chain(llm, db)

answer_prompt = PromptTemplate.from_template(
    """
    Eres un asistente útil que responde a las preguntas de los usuarios basándose en los datos de una base de datos SQLite.
    Tu tarea es:
    1. Dada una pregunta del usuario, genera una consulta SQL de SQLite3 válida.
    2. Ejecuta la consulta y revisa los resultados.
    3. Formula una respuesta clara y concisa utilizando ÚNICAMENTE los datos obtenidos de la consulta SQL.
    4. Si la consulta SQL no devuelve datos o no es relevante para la pregunta, responde que no puedes encontrar la información o que necesitas más detalles.
    5. Siempre devuelve la respuesta en español.
    6. NO incluyas la consulta SQL en la respuesta final, a menos que se te pida explícally.
    7. NO incluyas explicaciones sobre cómo se obtuvo la información, solo la respuesta directa.

    Pregunta del usuario: {question}
    Consulta SQL: {query}
    Resultado SQL: {result}
    Respuesta: """
)

answer = answer_prompt | llm | StrOutputParser()

# --- Custom function to strip markdown code block fences ---
def strip_sql_markdown(sql_query: str) -> str:
    # Remove markdown code block fences (```sql and ```)
    sql_query = sql_query.strip()
    if sql_query.startswith("```sql"):
        sql_query = sql_query[len("```sql"):].strip()
    elif sql_query.startswith("```"): # In case it's just ``` without 'sql'
        sql_query = sql_query[len("```"):].strip()
    if sql_query.endswith("```"):
        sql_query = sql_query[:-len("```")].strip()
    return sql_query

# --- Custom functions to print intermediate steps for debugging ---
def log_intermediate_steps(data):
    print("\n--- LLM Generated SQL Query (Raw) ---")
    print(f"Question: {data['question']}")
    print(f"Generated SQL: {data['query']}")
    return data

def log_stripped_sql(data):
    print("\n--- Stripped SQL Query (Before Execution) ---")
    print(f"Stripped SQL: {data['stripped_query']}")
    return data

def log_final_result(data):
    print("\n--- SQL Execution Result ---")
    print(f"Question: {data['question']}")
    print(f"Generated SQL: {data['query']}") # This is the original, unstripped query
    print(f"SQL Result: {data['result']}")
    return data
# --- End of custom functions ---


chain = (
    RunnablePassthrough.assign(query=write_query) # LLM writes the query (with markdown)
    .assign(temp_data=log_intermediate_steps) # Log the raw generated SQL
    .assign(
        # CORRECTED: Use RunnableLambda to apply strip_sql_markdown to the 'query' key's value
        stripped_query=RunnableLambda(lambda x: strip_sql_markdown(x["query"]))
    )
    .assign(temp_data_stripped=log_stripped_sql) # Log the stripped SQL
    .assign(
        result=itemgetter("stripped_query") | execute_query # Execute the stripped query
    )
    .assign(temp_data_2=log_final_result) # Log the SQL result
    | answer
)

def answer(question):
    result = chain.invoke({"question": f"{question}"})
    return result