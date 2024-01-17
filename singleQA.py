from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_KEY")

gpt4 = ChatOpenAI(model="gpt-4-1106-preview", openai_api_key=OPENAI_KEY)

q = """"""

manager_msg = [
        SystemMessage(content=""),
        HumanMessage(content=q),
    ]
print(gpt4.invoke(manager_msg).content)