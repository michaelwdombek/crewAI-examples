import sys
import os
import json
from typing import List, Dict

from crewai import Agent, Task, Crew
from langchain.agents.agent_toolkits import FileManagementToolkit
from langchain.agents  import AgentType, load_tools





human_as_a_tool = load_tools(["human"])

def load_environment_variable(variable_name: str) -> str:
    """Loads the value of a specified environment variable."""
    return os.getenv(variable_name)




LIST_OF_AGENTS = ["manager", "programmer",]


AGENT_TOOLS_CONFIG = {
        "manager": human_as_a_tool,
        "programmer":[],
        "writer": [],
        "tester": []
    }

                
def load_agents_config(path: str = "./agents_config.json") -> Dict[str, Dict[str, str]]:
    """Loads the agents configuration file."""
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError as e:
        print(f"Agents configuration file not found at {path}.")
        sys.exit(1)

def _create_agents(
        agents_config: Dict, 
        list_of_agents: List[str], 
        dict_of_agent_tools: Dict[str, Dict[str, List[str]]]) -> Dict[str, Agent]:
    """ creates a list of Crew AI Agents, based on the agents configuration file, adds the tools to each agent, and returns the list of agents. """

    return {agent: Agent(tools=dict_of_agent_tools[agent], **agents_config[agent]) for agent in list_of_agents}

    
    #return [Agent(tools=dict_of_agent_tools[agent], **agents_config[agent]) for agent in list_of_agents]

def _create_tasks(base_task: str, kickoff_agent: str) -> List[Task]:
    """Creates a list of tasks, based on the base task and the kickoff agent."""
    return [Task(description=base_task,agent=kickoff_agent)]
        


def main():
    
    high_level_task = '''write, test and document a python script with the following functionality:
    * connect to a webserver with a directory listing
    * download all files of the type .ipxe
    * download all files of type iso that have matching .ipxe files
    you can ask a human for clarification if the tasks are unclear.
    '''

    agents_config = load_agents_config()
    agents = _create_agents(agents_config, LIST_OF_AGENTS, AGENT_TOOLS_CONFIG)
    task= _create_tasks(base_task=high_level_task, kickoff_agent=agents["manager"])
    
    pyteam = Crew(
        agents=[agent for agent in agents.values()],
        tasks=task,
        verbose=2)

    pyteam.kickoff()


if __name__ == '__main__':
    main()


