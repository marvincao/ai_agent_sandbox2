""" 📈 AI Tikcer Agent """

from datetime import datetime
from dotenv import load_dotenv
from os import getenv
from pathlib import Path

from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools

load_dotenv()

''' Ticker
    NVDA, TSLA, AAPL, GOOG, MSFT, AMZN
'''
ticker = "TSLA"

timestamp = datetime.now().strftime("%Y%m%d%H%M")

# Ensure the output directory exists
output_dir = Path('../output/ticker')
output_dir.mkdir(parents=True, exist_ok=True)
output_file = f"{output_dir}/{ticker}.{timestamp}.md"

agent = Agent(
    model=Gemini(
        # id=getenv("GEMINI_LLM_MODEL"),
        id="gemini-2.0-flash-exp",
        api_key=getenv("GEMINI_API_KEY"),
    ),
    tools=[
        DuckDuckGoTools(), 
        YFinanceTools(enable_all=True),
    ],
    instructions=["Use markdown tables to display data"],
    expected_output="a professional report in markdown format without any initial nor immediate steps and planning.",
    # show_tool_calls=True,
    add_datetime_to_instructions=True,
    add_history_to_messages=True,
    num_history_responses=12,
    save_response_to_file=output_file,
    debug_mode=True,
    markdown=True,
    telemetry=False,
)

agent.print_response(
    message=f"Write a thorough report on {ticker}, get all financial information and latest news",
    stream=True,
)
