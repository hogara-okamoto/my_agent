from google.adk.agents.llm_agent import Agent
from google.adk.models import Gemini
# from google.adk.tools import google_search
from google.api_core import retry

# Import other agents and tools
from time_agent.agent import get_current_time
from fee_rate.agent import get_fee_for_payment_method
from exchange_rate.agent import get_exchange_rate

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
        model="gemini-2.5-flash",
        retry_options=retry_config
    ),
    description="A simple agent that can answer general questions.",
    instruction="""You are a helpful assistant that can:
- Get current time in cities using the get_current_time tool (extract the city name from the user's query)
- Look up transaction fees for payment methods using the get_fee_for_payment_method tool
- Look up exchange rates between currencies using the get_exchange_rate tool

When a user asks about time (e.g., "What time is it in Tokyo?"), extract the city name (e.g., "Tokyo") and use get_current_time with that city name. When they ask about fees, use get_fee_for_payment_method. When they ask about exchange rates, use get_exchange_rate.""",
    tools=[get_current_time, get_fee_for_payment_method, get_exchange_rate],
)

print("✅ Root Agent defined with sub-agents as tools.")