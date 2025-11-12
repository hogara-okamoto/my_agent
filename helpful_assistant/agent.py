from google.adk.agents.llm_agent import Agent
from google.adk.models import Gemini
from google.adk.tools import google_search
from google.api_core import retry

# Configure retry options
retry_config = retry.Retry(
    initial=1.0,
    maximum=10.0,
    multiplier=2.0,
    deadline=60.0,
)

root_agent = Agent(
    name="helpful_assistant",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    description="A simple agent that can answer general questions.",
    instruction="You are a helpful assistant. Use Google Search for current info or if unsure.",
    tools=[google_search],
)

print("✅ Root Agent defined.")