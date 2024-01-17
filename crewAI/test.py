
from langchain_openai import ChatOpenAI
from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_KEY")

from langchain.tools import DuckDuckGoSearchRun
search_tool = DuckDuckGoSearchRun()

# Define your agents with roles and goals
researcher = Agent(
  role='高級研究分析師',
  goal='發現人工智慧和數據科學的前沿發展',
  backstory="""您在一家領先的科技智庫工作。
   您的專長在於識別新興趨勢。
   您有剖析複雜數據並呈現的技巧
   可行的見解。""",
  verbose=True,
  allow_delegation=False,
  tools=[search_tool],
  llm=ChatOpenAI(model="gpt-4-1106-preview", openai_api_key=OPENAI_KEY)
)
writer = Agent(
  role='技術內容策略師',
  goal='製作有關技術進步的引人注目的內容',
  backstory="""您是一位著名的內容策略師，以
   您富有洞察力和引人入勝的文章。
   您將複雜的概念轉化為引人入勝的敘述。""",
  verbose=True,
  allow_delegation=True,
  llm=ChatOpenAI(model="gpt-4-1106-preview", openai_api_key=OPENAI_KEY)
)

# Create tasks for your agents
task1 = Task(
  description="""對2024年人工智慧最新進展進行全面分析。
  確定關鍵趨勢、突破性技術和潛在的行業影響。
  您的最終答案必須是完整的分析報告""",
  agent=researcher
)

task2 = Task(
  description="""利用提供的見解，開發一個引人入勝的博客
   這篇文章強調了最重要的人工智慧進步。
   您的貼文應該內容豐富且易於理解，適合精通科技的受眾。
   讓它聽起來很酷，避免使用複雜的單詞，這樣聽起來就不像人工智慧。
   您的最終答案是大約200字左右的小文章。""",
  agent=writer
)

# Instantiate your crew with a sequential process
crew = Crew(
  agents=[researcher, writer],
  tasks=[task1, task2],
  verbose=2, 
)

# Get your crew to work!
result = crew.kickoff()

print("######################")
print(result)