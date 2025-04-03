"""🔍 AI News Agent 
"""

from datetime import datetime
from dotenv import load_dotenv
from os import getenv
from pathlib import Path
from textwrap import dedent

from agno.agent import Agent
from agno.models.google import Gemini

load_dotenv()

"""
# Examples
MESSAGE="International News"
MESSAGE="News from Toronto, Canada?"
MESSAGE="News from Canada?"
MESSAGE="News about Singer Adele?"
"""
MESSAGE="News from USA?"

timestamp = datetime.now().strftime("%Y%m%d%H%M")

output_dir = Path('../output/news')
output_dir.mkdir(parents=True, exist_ok=True)
output_file = f"{output_dir}/{timestamp}.news.md"

agent = Agent(
    model=Gemini(
        # id="gemini-2.0-flash",                # 15RPM
        # id=getenv("GEMINI_LOG_MODEL"),        # 10RPM, not working
        id=getenv("GEMINI_LLM_MODEL"),        #  5RPM
        api_key=getenv("GEMINI_API_KEY"),
        grounding=True,
    ), 
    # show_tool_calls=True,
    add_datetime_to_instructions=True,
    save_response_to_file=output_file,
    debug_mode=True,
    markdown=True,
    telemetry=False,
)

agent.print_response(
        message=dedent(MESSAGE), 
        stream=True
    )
