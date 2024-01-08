from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from chat_prompt import ENGINEER, PLANNER, SUMMARIZER, MANAGER
from execute import execute_code
from dotenv import load_dotenv
import re
import os

load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_KEY")

gpt4 = ChatOpenAI(model="gpt-4-1106-preview", openai_api_key=OPENAI_KEY)

role_prompt = {
    'Engineer':"你是一個工程師，"+ENGINEER,
    'Planner':"你是一個規劃者，"+PLANNER,
    'Summarizer':"你是一個總結者"+SUMMARIZER,
    'Manager':MANAGER,
}

# user 發問
quesion = input('請輸入你的問題: ')
init_chat = {'role':'Customer', 'msg':quesion}

# Set msg history
msg_his = [init_chat]

# Group chat
while(1):

    # Manager 決定下一個發言的角色和內容
    manager_msg = [
        SystemMessage(content=role_prompt['Manager']),
        HumanMessage(content=f"{msg_his}"),
    ]
    res = eval(gpt4.invoke(manager_msg).content)
    next_role = res['role']
    next_msg = res['msg']
    print('--------------------------------------------------------------------------------')
    print(f'Manager 對 {next_role} 發問:\n{next_msg}')

    # 被選定的角色發言
    if next_role == 'Customer':
        user_msg = input('你有甚麼反饋，如果你想結束這個會議，輸出 EXIT: ')
        if user_msg == 'EXIT':
            break
        msg_his.append({'role':'Customer', 'msg':user_msg})
    else:
        role_msg = [
            SystemMessage(content=role_prompt[next_role]), # 帶入該角色的 prompt
            HumanMessage(content=next_msg),
        ]
        res = gpt4.invoke(role_msg).content

        # 檢查輸出的是不是 code block
        pattern = r"```([\s\S]+?)```"
        match = re.search(pattern, res)
        if match:
            extracted_code = match.group(1)
            res = execute_code(extracted_code)
            print(f"程式的執行結果是: {res}")
            msg_his.append({'role':next_role, 'msg':f"程式的執行結果是: {res}"})
        else:
            print(f"{next_role} 回答:\n{res}")
            msg_his.append({'role':next_role, 'msg':res})
print('--------------------------------------------------------------------------------')
print('會議結束')