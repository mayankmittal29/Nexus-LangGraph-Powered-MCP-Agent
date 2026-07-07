"""SQLite-backed checkpointer used for conversation persistence and thread
history retrieval."""
import aiosqlite
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

from . import config
from .async_runtime import run_async


async def _init_checkpointer():
    conn = await aiosqlite.connect(database=config.CHECKPOINT_DB_PATH)
    return AsyncSqliteSaver(conn)


checkpointer = run_async(_init_checkpointer())


async def _alist_threads():
    all_threads = set()
    async for checkpoint in checkpointer.alist(None):
        all_threads.add(checkpoint.config["configurable"]["thread_id"])
    return list(all_threads)


def retrieve_all_threads():
    return run_async(_alist_threads())
