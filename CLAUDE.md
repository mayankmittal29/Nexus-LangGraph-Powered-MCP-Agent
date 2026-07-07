# CLAUDE.md

This file gives Claude Code (or any AI coding assistant) the context needed to work in this repository.

## What this project is

A tool-using chatbot built on **LangGraph** with a **Streamlit** frontend. The core idea: a single LLM node in a small cyclic graph decides, on every turn, whether to answer directly or call a tool (web search, stock price lookup, or a tool exposed by a remote/local **MCP** — Model Context Protocol — server). Tool results feed back into the same node until the LLM produces a final answer. Every conversation is persisted to SQLite via a LangGraph checkpointer, keyed by a per-session `thread_id`, so past conversations are browsable and resumable from the sidebar.

This is an educational/personal project exploring LangGraph patterns — it evolved through several throwaway prototypes (plain graph → SQLite-persisted graph → single custom tool → RAG variant) before landing on the current MCP-integrated design. Those prototypes live in `iterations_files/` for reference only; they are not wired into the running app and should not be modified or extended — treat them as read-only history.

## Architecture at a glance

- **`backend/`** — pure LangGraph/agent logic, no Streamlit imports. Could be reused behind any frontend.
  - `config.py` — the only place `os.getenv` is called; every setting (LLM provider, DB path, tool keys, MCP server locations) flows through here.
  - `async_runtime.py` — a dedicated background asyncio event loop + `run_async`/`submit_async_task` helpers. Exists because Streamlit's script-rerun model is synchronous but LangGraph's checkpointer, MCP client, and `astream` are async. This bridge is what makes streaming and persistence work without blocking the UI thread.
  - `llm.py` — provider selection. `LLM_PROVIDER=openai` (default) uses `ChatOpenAI()`; `LLM_PROVIDER=gemini` uses `ChatGoogleGenerativeAI(model=GEMINI_MODEL)`. Only one provider is instantiated per process.
  - `tools.py` — defines `search_tool` (DuckDuckGo) and `get_stock_price` (Alpha Vantage), plus a `MultiServerMCPClient` that loads tools from configured MCP servers (`arith`: local stdio server; `expense`: remote streamable-HTTP server). MCP loading is wrapped in a try/except — if a server is unreachable, the app degrades gracefully and just runs with fewer tools rather than crashing.
  - `state.py` — `ChatState` TypedDict: a single `messages` field reduced with LangGraph's `add_messages`.
  - `checkpointer.py` — `AsyncSqliteSaver` over `aiosqlite`, plus `retrieve_all_threads()` used to populate the sidebar's thread list.
  - `graph.py` — builds the actual `StateGraph`: `chat_node` (async, calls `llm_with_tools.ainvoke`) with a conditional edge (`tools_condition`) to a `ToolNode`, looping back to `chat_node`. Exports the compiled `chatbot`.
  - `__init__.py` — re-exports `chatbot`, `retrieve_all_threads`, `submit_async_task`, `run_async` as the package's public surface, so the frontend imports from `backend` rather than reaching into submodules.

- **`frontend/`** — pure Streamlit UI, no graph-construction logic. Only imports the already-compiled `chatbot` from `backend`.
  - `session.py` — session-state init, thread creation/reset, loading a past thread's messages via `chatbot.get_state(...)`.
  - `sidebar.py` — "New Chat" button and the clickable list of past thread IDs.
  - `chat.py` — renders message history and handles a new user turn: runs `chatbot.astream(..., stream_mode="messages")` on the background loop via a `queue.Queue` bridge, yields only `AIMessage` content chunks to `st.write_stream`, and shows a live `st.status` widget while `ToolMessage`s arrive.
  - `app.py` — wires `session` + `sidebar` + `chat` together into the page flow.

- **`streamlit_app.py`** (repo root) — the actual entrypoint Streamlit runs (`streamlit run streamlit_app.py`). It just calls `frontend.app.main()`. Kept at the root (rather than inside `frontend/`) so `frontend/` and `backend/` can use ordinary package-relative imports without path hacks.

## Conventions to preserve

- **No business logic changes without being asked.** The current module split is a direct, line-for-line extraction of the original two-file implementation (`langgraph_mcp_backend.py` + `streamlit_frontend_mcp.py`, now removed) into packages — behavior is intentionally unchanged.
- **Config only in `backend/config.py`.** Don't scatter `os.getenv` calls elsewhere; add new settings there with a sensible default matching prior hardcoded behavior.
- **Keep `backend/` Streamlit-free.** It should stay usable from a non-Streamlit context (API server, CLI, tests) in the future.
- **MCP tool loading must stay best-effort.** Never let a missing/unreachable MCP server crash startup — the try/except in `load_mcp_tools()` is intentional.
- **The async bridge is load-bearing.** Do not call LangGraph's async APIs (`ainvoke`, `astream`, checkpointer coroutines) directly from Streamlit's main thread — always go through `run_async`/`submit_async_task` in `async_runtime.py`.
- **`iterations_files/` is frozen.** Don't refactor, modularize, or "fix" those files — they're kept as-is for historical reference.
- No test suite exists by design for this project at this stage — don't add one unless explicitly asked.

## Where to look for things

| Need to... | Look in |
|---|---|
| Add/modify a tool | `backend/tools.py` |
| Change which LLM/model is used | `backend/llm.py`, `.env` (`LLM_PROVIDER`, `GEMINI_MODEL`) |
| Change graph routing/nodes | `backend/graph.py` |
| Change what's persisted or how threads are listed | `backend/checkpointer.py` |
| Change chat UI / streaming behavior | `frontend/chat.py` |
| Change sidebar / thread switching | `frontend/sidebar.py` |
| Add a new environment variable | `backend/config.py` + `.env.example` |
