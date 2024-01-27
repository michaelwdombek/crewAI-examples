from langchain.agents import Tool
from langchain_experimental.utilities import PythonREPL


class PythonREPLRun(Tool):
    def __init__(self):
        super().__init__()
        self.name = "Python REPL"
        self.description = "Run Python REPL"

    def run(self):
        repl = PythonREPL()
        repl.run()
        return repl.result