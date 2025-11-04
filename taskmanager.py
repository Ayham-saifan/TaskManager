from langchain_openai import ChatOpenAI

class TaskModel:
    def __init__(self, model_name="gpt-4o-mini"):
        self.llm = ChatOpenAI(model=model_name)

    def invoke(self, prompt: str) -> str:
        """Invoke the LLM with a prompt and return the content"""
        response = self.llm.invoke(prompt)
        return response.content
