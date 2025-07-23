from typing import Iterator
from agno.agent import Agent, RunResponse
from agno.models.google import Gemini
from agno.workflow import Workflow
from agno.utils.pprint import pprint_run_response
from dotenv import load_dotenv
import os
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# Define the workflow
class MyWorkflow(Workflow):
    # Update the model ID to use Gemini
    agent1 = Agent(model=Gemini(id="gemini-1.5-flash", api_key=GOOGLE_API_KEY)) # <-- Changed here
    agent2 = Agent(model=Gemini(id="gemini-1.5-flash", api_key=GOOGLE_API_KEY)) # <-- Changed here
    
    def my_custom_flow(self, message: str) -> Iterator[RunResponse]:
        # Agent 1 processes initial request
        result1 = self.agent1.run(message)
        yield result1

        # Extract the first message's content
        content1 = result1.messages[0].content if result1.messages else ""
        
        # Agent 2 processes the output of agent 1
        result2 = self.agent2.run(f"Analyze this: {content1}")
        yield result2

if __name__ == "__main__":
    workflow = MyWorkflow()
    # Convert the generator to a list to run the workflow
    response_generator = workflow.my_custom_flow("Tell me about artificial intelligence")
    responses = list(response_generator)

    # Iterate over the list of responses and print each one
    for response in responses:
        pprint_run_response(response, markdown=True, show_time=True)