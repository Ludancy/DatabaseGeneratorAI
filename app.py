import key
import os

os.environ["OPENAI_API_KEY"] = key.OPENAI_API_KEY

############################################################

from langchain_community.utilities import SQLDatabase

db = SQLDatabase.from_uri("sqlite:///data_base.db")
#print(db.dialect)
#print(db.get_usable_table_names())

from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
chain = create_sql_query_chain(llm, db)
response = chain.invoke({"question": "How many employees are there"})

###
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool

execute_query = QuerySQLDataBaseTool(db=db)
write_query = create_sql_query_chain(llm, db)
chain = write_query | execute_query
#chain.invoke({"question": "How many employees are there"})

###################

from operator import itemgetter

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

answer_prompt = PromptTemplate.from_template(
    """
Data una pregunta del usuario:
1. crea una consulta de sqlite3 que sea valida
2. revisa los resultados
3. devuelve el dato
4. si tienes que hacer alguna aclaración o devolver cualquier texto que sea siempre en español

Question: {question}
SQL Query: {query}
SQL Result: {result}
Answer: """

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





