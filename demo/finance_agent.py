"""🗞️ AI Finance Agent Team

A powerful market watch team of AI agents working together to provide 
comprehensive financial analysis and news reporting. 

The team consists of:
1. Web Agent: Searches and analyzes latest news
2. Finance Agent: Analyzes financial data and market trends
3. Lead Editor: Coordinates and combines insights from both agents

"""

import yaml

from datetime import datetime
from os import getenv
from pathlib import Path
from dotenv import load_dotenv
from textwrap import dedent

from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools
from agno.tools.calculator import CalculatorTools

load_dotenv()

agents_config_file = '../config/finance/agents.yaml'
tasks_config_file = '../config/finance/tasks.yaml'
with open(agents_config_file, 'r', encoding='utf-8') as file:
    agents_config = yaml.safe_load(file)
with open(tasks_config_file, 'r', encoding='utf-8') as file:
    tasks_config = yaml.safe_load(file)
    
today = datetime.now().strftime("%Y-%m-%d")
timestamp = datetime.now().strftime("%Y%m%d%H%M")
MODEL = "gemini-2.0-flash"
# MODEL = getenv("GEMINI_LLM_MODEL")
API_KEY = getenv("GEMINI_API_KEY")

# Ensure the output directory exists
output_dir = Path('../output/finance')
output_dir.mkdir(parents=True, exist_ok=True)
output_file = f"{output_dir}/{timestamp}.md"

web_agent = Agent(
    name="Web Agent",
    model=Gemini(
        id=MODEL,
        api_key=API_KEY,
    ), 
    role=agents_config['research_analyst']['role'],
    goal=agents_config['research_analyst']['goal'],
    instructions=dedent(agents_config['research_analyst']['instructions']),
    tools=[DuckDuckGoTools()],
    show_tool_calls=True,
    markdown=True,
    telemetry=False,
)

finance_agent = Agent(
    name="Finance Agent",
    role=agents_config['financial_analyst']['role'],
    goal=agents_config['financial_analyst']['goal'],
    instructions=dedent(agents_config['financial_analyst']['instructions']),
    model=Gemini(
        id=MODEL,
        api_key=API_KEY,
    ), 
    tools=[
        YFinanceTools(
            # stock_price=True, 
            # analyst_recommendations=True,
            # stock_fundamentals=True,
            # historical_prices=True,
            # company_info=True,
            # company_news=True
            enable_all=True,
        ),
        CalculatorTools(
            # enables addition, subtraction, multiplication, division, check prime, exponential, factorial, square root
            enable_all=True,
        )        
    ],
    show_tool_calls=True,
    add_datetime_to_instructions=True,
    markdown=True,
    telemetry=False,
)

agent_team = Agent(
    team=[web_agent, finance_agent],
    model=Gemini(
        id=MODEL,
        api_key=API_KEY,
    ), 
    role=agents_config['lead_editor']['role'],
    goal=agents_config['lead_editor']['goal'],
    instructions=dedent(agents_config['lead_editor']['instructions']),
    expected_output=dedent(tasks_config['lead_editor']['expected_output']),
    # show_tool_calls=True,
    add_datetime_to_instructions=True,
    save_response_to_file=output_file,
    markdown=True,
    debug_mode=False,
    telemetry=False,
)

# Advanced queries to explore:
"""
"Analyze the impact of AI developments on NVIDIA's stock (NVDA)"
"Analyze recent developments and financial performance of TSLA"
"What's the latest news and financial performance of Apple (AAPL)?"
"How are EV manufacturers performing? Focus on Tesla (TSLA) and Rivian (RIVN)"
"What's the market outlook for semiconductor companies like AMD and Intel?"
"Summarize recent developments and stock performance of Microsoft (MSFT)"
"Compare the financial performance and recent news of major cloud providers (AMZN, MSFT, GOOGL)"
"What's the impact of recent Fed decisions on banking stocks? Focus on JPM and BAC"
"Analyze the gaming industry outlook through ATVI, EA, and TTWO performance"
"How are social media companies performing? Compare META and SNAP"
"""

MESSAGE="""
"Compare the financial performance and recent news of major cloud providers (AMZN, MSFT, GOOGL)"
"""

if __name__ == "__main__":
    agent_team.print_response(
        message=dedent(MESSAGE),
        stream=True
    )
