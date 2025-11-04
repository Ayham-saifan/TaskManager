from typing import List, Dict, TypedDict
from langgraph.graph import StateGraph, START, END
from taskmanager import TaskModel  # import the model class


# TypedDict for the state
class TaskState(TypedDict):
    tasks: List[str]
    generated: str
    classified: Dict[str, List[str]]
    summary: str
    plan: str

class TaskManager:
    def __init__(self):
        self.model = TaskModel()
        self.graph = StateGraph(TaskState)
        self._build_graph()
        self.app = self.graph.compile()

    def _build_graph(self):
        # Nodes
        self.graph.add_node("input_tasks", self.input_tasks)
        self.graph.add_node("generate_task", self.generate_task)
        self.graph.add_node("classify_tasks", self.classify_tasks)
        self.graph.add_node("summarize_tasks", self.summarize_tasks)
        self.graph.add_node("plan_tasks", self.plan_tasks)

        # Edges
        self.graph.add_edge(START, "input_tasks")
        self.graph.add_edge("input_tasks", "generate_task")
        self.graph.add_edge("generate_task", "classify_tasks")
        self.graph.add_edge("classify_tasks", "summarize_tasks")
        self.graph.add_edge("summarize_tasks", "plan_tasks")
        self.graph.add_edge("plan_tasks", END)

    # Node functions
    def input_tasks(self, state: TaskState):
        return {"tasks": state["tasks"]}

    def generate_task(self, state: TaskState):
        prompt = f"Suggest 3 sub tasks related to the input task as bullet points without any describtion and put each one in a new line: \n{state['tasks']}"
        generated = self.model.invoke(prompt)
        return {"generated": generated.replace("-", "").split("\n")}

    def classify_tasks(self, state: TaskState):
        prompt = f"""Classify the following tasks into categories like 'Study', 'Personal', 'Work'. Ignore empty categories.and make it in the form of new lines 
Tasks: {state['generated']}"""
        classified = self.model.invoke(prompt)
        return {"classified": classified.replace("-", "").split("\n")}

    def summarize_tasks(self, state: TaskState):
        prompt = f"Summarize the following tasks in less than 35 words:\n{state['generated']}"
        summary = self.model.invoke(prompt)
        return {"summary": summary}

    def plan_tasks(self, state: TaskState):
        prompt = f"""Prioritize the following tasks and give a time-based plan in less than 50 words and seprate them by new lines
Tasksand put each one in a new line without numbering : {state['generated']}"""
        plan = self.model.invoke(prompt)
        return {"plan": plan.replace("-", "").split("\n")}

    def run(self, input_data: dict):
        return self.app.invoke(input_data)


# Example usage
if __name__ == "__main__":
    input_data = {"tasks": ""}
    manager = TaskManager()
    result = manager.run(input_data)

    print("\n=== GENERATION ===")
    print(result["generated"])
    print("\n=== CLASSIFICATION ===")
    print(result["classified"])
    print("\n=== SUMMARY ===")
    print(result["summary"])
    print("\n=== PLAN ===")
    print(result["plan"])
