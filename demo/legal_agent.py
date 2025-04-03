"""🧠 AI Legal Consultant

The agent uses a PDF knowledge base of "Computer Crime" database.

Control embedding rate limits with the `rate_limit` parameter.

"""

import time

from datetime import datetime
from dotenv import load_dotenv
from os import getenv
from pathlib import Path
from textwrap import dedent

from agno.agent import Agent
from agno.models.google import Gemini
from agno.embedder.google import GeminiEmbedder
from agno.document.chunking.agentic import AgenticChunking
from agno.knowledge.pdf_url import PDFUrlKnowledgeBase
from agno.vectordb.lancedb import LanceDb, SearchType


load_dotenv()

"""
# Allegations | Computer Crimes
allegation = "Trespassing in a Government Computer"
allegation = "Disclosing an Intercepted Communication"
allegation = "spoofing Email Address"
"""
allegation = "Wire Fraud"

# Convert to a URL-safe format
url_safe_topic = allegation.lower().replace(" ", "-")

# Rate limiting parameters
REQUEST_LIMIT = 5
TIME_WINDOW = 60  # seconds
request_timestamps = []

# Ensure the output directory exists
timestamp = datetime.now().strftime("%Y%m%d%H%M")
output_dir = Path('../output/legal')
output_dir.mkdir(parents=True, exist_ok=True)
output_file = f"{output_dir}/{timestamp}.{url_safe_topic}.md"

def make_request_with_rate_limit(func, *args, **kwargs):
    # timestamp of the current request
    current_time = time.time()
    request_timestamps.append(current_time)
    
    # Remove requests outside the time window
    while request_timestamps and request_timestamps[0] < current_time - TIME_WINDOW:
        request_timestamps.pop(0)
    
    # Check if the request limit has been reached
    if len(request_timestamps) > REQUEST_LIMIT:
        wait_time = TIME_WINDOW - (current_time - request_timestamps[0])
        if wait_time > 0:
            time.sleep(wait_time)
    
    # Make the request
    return func(*args, **kwargs)

class RateLimitedGeminiEmbedder(GeminiEmbedder):
    def embed(self, *args, **kwargs):
        return make_request_with_rate_limit(super().embed, *args, **kwargs)


knowledge_base = PDFUrlKnowledgeBase(
    urls=[
        "https://www.justice.gov/d9/criminal-ccips/legacy/2015/01/14/ccmanual_0.pdf",
    ],
    vector_db=LanceDb(
        table_name="legal_docs",
        uri="../vectordb/lancedb",
        search_type=SearchType.vector,
        embedder=RateLimitedGeminiEmbedder(
            api_key=getenv("GEMINI_API_KEY"),
        ),
    ),
    chunking_strategy=AgenticChunking(
        # model=getenv("GEMINI_LLM_MODEL"),
        model="gemini-2.0-flash-exp",
    ),
)

# Comment out after first run
# knowledge_base.load(
#     recreate=True,
#     # upsert=True,
# )

legal_agent = Agent(
    name="LegalAdvisor",
    model=Gemini(
        id="gemini-2.0-flash-exp",
        api_key=getenv("GEMINI_API_KEY"),
    ),
    instructions=[
        "Provide legal information and advice based on the knowledge base.",
        "Include relevant legal citations and sources when answering questions.",
        "Always clarify that you're providing general legal information, not professional legal advice.",
        "Recommend consulting with a licensed attorney for specific legal situations.",
    ],
    expected_output="a professional report in markdown format without any initial nor immediate steps and planning.  make sure it is UTF8 compatible. at the end of report include references. have a compelling title.",
    knowledge=knowledge_base,
    search_knowledge=True,
    # show_tool_calls=True,
    save_response_to_file=output_file,
    debug_mode=True,
    markdown=True,
    telemetry=False,
)

# print the response
legal_agent.print_response(
    f"What are the legal consequences and criminal penalties for {allegation}?",
    stream=True,
)
