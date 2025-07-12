# app.py
import os
import key # Assuming key.py contains your API key

# No necesitas cambiar esto, ya que solo establece la variable de entorno
# Cambiado a GOOGLE_API_KEY para ser más explícito para Gemini, aunque LangChain usará lo que esté en openai_api_key
os.environ["GOOGLE_API_KEY"] = key.OPENAI_API_KEY # Asumiendo que OPENAI_API_KEY en tu key.py es tu clave de Gemini

############################################################

from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
# Importa la clase correcta para Gemini desde langchain-google-genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from operator import itemgetter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_base.db")
db = SQLDatabase.from_uri(f"sqlite:///{db_path}")
#print(db.dialect)
#print(db.get_usable_table_names())

# --- Modificación para usar Gemini de forma nativa con langchain-google-genai ---
# Elimina openai_api_base y usa google_api_key o simplemente deja que LangChain lo recoja de las variables de entorno
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",  # O el modelo Gemini que prefieras (gemini-1.5-pro, etc.)
    temperature=0,
    # No necesitas openai_api_base si usas ChatGoogleGenerativeAI
    # No necesitas openai_api_key si la variable de entorno GOOGLE_API_KEY está configurada
)
# --- Fin de la modificación para Gemini ---

chain = create_sql_query_chain(llm, db)
response = chain.invoke({"question": "How many employees are there"})

###
execute_query = QuerySQLDataBaseTool(db=db)
write_query = create_sql_query_chain(llm, db)
# Nota: La siguiente línea estaba comentada, si necesitas esta cadena específica, descoméntala.
# chain = write_query | execute_query
# chain.invoke({"question": "How many employees are there"})

###################

answer_prompt = PromptTemplate.from_template(
    """
    Eres un asistente útil que responde a las preguntas de los usuarios basándose en los datos de una base de datos SQLite.
    Tu tarea es:
    1. Dada una pregunta del usuario, genera una consulta SQL de SQLite3 válida.
    2. Ejecuta la consulta y revisa los resultados.
    3. Formula una respuesta clara y concisa utilizando ÚNICAMENTE los datos obtenidos de la consulta SQL.
    4. Si la consulta SQL no devuelve datos o no es relevante para la pregunta, responde que no puedes encontrar la información o que necesitas más detalles.
    5. Siempre devuelve la respuesta en español.
    6. NO incluyas la consulta SQL en la respuesta final, a menos que se te pida explícitamente.
    7. NO incluyas explicaciones sobre cómo se obtuvo la información, solo la respuesta directa.

    Pregunta del usuario: {question}
    Consulta SQL: {query}
    Resultado SQL: {result}
    Respuesta: """
)

answer = answer_prompt | llm | StrOutputParser()
chain = (
    RunnablePassthrough.assign(query=write_query).assign(
        result=itemgetter("query") | execute_query
    )
    | answer
)

def answer(question):
    result = chain.invoke({"question": f"{question}"})
    return result# app.py
import os
import key # Assuming key.py contains your API key

# No necesitas cambiar esto, ya que solo establece la variable de entorno
# Cambiado a GOOGLE_API_KEY para ser más explícito para Gemini, aunque LangChain usará lo que esté en openai_api_key
os.environ["GOOGLE_API_KEY"] = key.OPENAI_API_KEY # Asumiendo que OPENAI_API_KEY en tu key.py es tu clave de Gemini

############################################################

from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
# Importa la clase correcta para Gemini desde langchain-google-genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from operator import itemgetter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_base.db")
db = SQLDatabase.from_uri(f"sqlite:///{db_path}")
#print(db.dialect)
#print(db.get_usable_table_names())

# --- Modificación para usar Gemini de forma nativa con langchain-google-genai ---
# Elimina openai_api_base y usa google_api_key o simplemente deja que LangChain lo recoja de las variables de entorno
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",  # O el modelo Gemini que prefieras (gemini-1.5-pro, etc.)
    temperature=0,
    # No necesitas openai_api_base si usas ChatGoogleGenerativeAI
    # No necesitas openai_api_key si la variable de entorno GOOGLE_API_KEY está configurada
)
# --- Fin de la modificación para Gemini ---

chain = create_sql_query_chain(llm, db)
response = chain.invoke({"question": "How many employees are there"})

###
execute_query = QuerySQLDataBaseTool(db=db)
write_query = create_sql_query_chain(llm, db)
# Nota: La siguiente línea estaba comentada, si necesitas esta cadena específica, descoméntala.
# chain = write_query | execute_query
# chain.invoke({"question": "How many employees are there"})

###################

answer_prompt = PromptTemplate.from_template(
    """
    Eres un asistente útil que responde a las preguntas de los usuarios basándose en los datos de una base de datos SQLite.
    Tu tarea es:
    1. Dada una pregunta del usuario, genera una consulta SQL de SQLite3 válida.
    2. Ejecuta la consulta y revisa los resultados.
    3. Formula una respuesta clara y concisa utilizando ÚNICAMENTE los datos obtenidos de la consulta SQL.
    4. Si la consulta SQL no devuelve datos o no es relevante para la pregunta, responde que no puedes encontrar la información o que necesitas más detalles.
    5. Siempre devuelve la respuesta en español.
    6. NO incluyas la consulta SQL en la respuesta final, a menos que se te pida explícitamente.
    7. NO incluyas explicaciones sobre cómo se obtuvo la información, solo la respuesta directa.

    Pregunta del usuario: {question}
    Consulta SQL: {query}
    Resultado SQL: {result}
    Respuesta: """
)

answer = answer_prompt | llm | StrOutputParser()
chain = (
    RunnablePassthrough.assign(query=write_query).assign(
        result=itemgetter("query") | execute_query
    )
    | answer
)

def answer(question):
    result = chain.invoke({"question": f"{question}"})
    return result