import math
import os
from typing import Optional, Type

# Starndard Langchain example
from langchain.agents import create_spark_sql_agent
from langchain.agents.agent_toolkits import SparkSQLToolkit
from langchain.chat_models import ChatOpenAI

# Import things that are needed generically
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool
from langchain.tools.file_management.read import ReadFileTool
from langchain.utilities.spark_sql import SparkSQL

import autogen

config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        "model": ["gpt-4-1106-preview"],
    },
)
class CircumferenceToolInput(BaseModel):
    radius: float = Field()


class CircumferenceTool(BaseTool):
    name = "circumference_calculator"
    description = "Use this tool when you need to calculate a circumference using the radius of a circle"
    args_schema: Type[BaseModel] = CircumferenceToolInput

    def _run(self, radius: float):
        return float(radius) * 2.0 * math.pi


def get_file_path_of_example():
    # Get the current working directory
    current_dir = os.getcwd()

    # Go one directory up
    parent_dir = os.path.dirname(current_dir)

    # Move to the target directory
    target_folder = os.path.join(parent_dir, "test")

    # Construct the path to your target file
    file_path = os.path.join(target_folder, "test_files/radius.txt")

    return file_path

# Define a function to generate llm_config from a LangChain tool


def generate_llm_config(tool):
    # Define the function schema based on the tool's args_schema
    function_schema = {
        "name": tool.name.lower().replace(" ", "_"),
        "description": tool.description,
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    }

    if tool.args is not None:
        function_schema["parameters"]["properties"] = tool.args

    return function_schema


# Instantiate the ReadFileTool
read_file_tool = ReadFileTool()
custom_tool = CircumferenceTool()

# Construct the llm_config
llm_config = {
    # Generate functions config for the Tool
    "functions": [
        generate_llm_config(custom_tool),
        generate_llm_config(read_file_tool),
    ],
    "config_list": config_list,  # Assuming you have this defined elsewhere
    "timeout": 120,
}

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    human_input_mode="TERMINATE",
    max_consecutive_auto_reply=10,
    code_execution_config={
        "work_dir": "coding",
        "use_docker": False,
    },  # Please set use_docker=True if docker is available to run the generated code. Using docker is safer than running the generated code directly.
)

# Register the tool and start the conversation
user_proxy.register_function(
    function_map={
        custom_tool.name: custom_tool._run,
        read_file_tool.name: read_file_tool._run,
    }
)

chatbot = autogen.AssistantAgent(
    name="chatbot",
    system_message="For coding tasks, only use the functions you have been provided with. Reply TERMINATE when the task is done.",
    llm_config=llm_config,
)

user_proxy.initiate_chat(
    chatbot,
    message=f"我想知道半徑3.361的圓周長是多少",
)