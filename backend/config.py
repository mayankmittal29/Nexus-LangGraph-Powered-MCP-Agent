"""Central configuration for the backend, loaded from environment variables."""
import os

from dotenv import load_dotenv

load_dotenv()

# -------------------
# LLM provider
# -------------------
# "openai" or "gemini"
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

# -------------------
# Checkpointer / persistence
# -------------------
CHECKPOINT_DB_PATH = os.getenv("CHECKPOINT_DB_PATH", "chatbot.db")

# -------------------
# Tools
# -------------------
DUCKDUCKGO_REGION = os.getenv("DUCKDUCKGO_REGION", "us-en")

ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY", "")
ALPHA_VANTAGE_BASE_URL = "https://www.alphavantage.co/query"

# -------------------
# MCP servers
# -------------------
MCP_ARITH_COMMAND = os.getenv("MCP_ARITH_COMMAND", "python3")
MCP_ARITH_SERVER_PATH = os.getenv(
    "MCP_ARITH_SERVER_PATH", "/Users/nitish/Desktop/mcp-math-server/main.py"
)
MCP_EXPENSE_SERVER_URL = os.getenv(
    "MCP_EXPENSE_SERVER_URL", "https://splendid-gold-dingo.fastmcp.app/mcp"
)
