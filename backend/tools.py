"""Tool definitions: a web search tool, a stock-price tool, and MCP tools
loaded from the configured MCP servers."""
import requests
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import BaseTool, tool
from langchain_mcp_adapters.client import MultiServerMCPClient

from . import config
from .async_runtime import run_async

search_tool = DuckDuckGoSearchRun(region=config.DUCKDUCKGO_REGION)


@tool
def get_stock_price(symbol: str) -> dict:
    """
    Fetch latest stock price for a given symbol (e.g. 'AAPL', 'TSLA')
    using Alpha Vantage.
    """
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": symbol,
        "apikey": config.ALPHA_VANTAGE_API_KEY,
    }
    r = requests.get(config.ALPHA_VANTAGE_BASE_URL, params=params)
    return r.json()


mcp_client = MultiServerMCPClient(
    {
        "arith": {
            "transport": "stdio",
            "command": config.MCP_ARITH_COMMAND,
            "args": [config.MCP_ARITH_SERVER_PATH],
        },
        "expense": {
            "transport": "streamable_http",  # if this fails, try "sse"
            "url": config.MCP_EXPENSE_SERVER_URL,
        },
    }
)


def load_mcp_tools() -> list[BaseTool]:
    try:
        return run_async(mcp_client.get_tools())
    except Exception:
        return []


def get_all_tools() -> list[BaseTool]:
    return [search_tool, get_stock_price, *load_mcp_tools()]
