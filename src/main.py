import asyncio
from contextlib import asynccontextmanager
import sys
from pathlib import Path

from fastapi import FastAPI
import uvicorn

sys.path.append(str(Path(__file__).parent.parent))

from src.bot.bot import create_bot_app
from src.api.auth import router as router_auth
from src.api.post import router as router_post


@asynccontextmanager
async def lifespan(app: FastAPI):
    bot_app = create_bot_app()

    await bot_app.initialize()
    await bot_app.start()
    polling_task = asyncio.create_task(bot_app.updater.start_polling())

    yield

    await bot_app.updater.stop()
    await bot_app.stop()
    await bot_app.shutdown()

    polling_task.cancel()
    try:
        await polling_task
    except asyncio.CancelledError:
        pass


app = FastAPI(lifespan=lifespan)

app.include_router(router_auth)
app.include_router(router_post)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True)
