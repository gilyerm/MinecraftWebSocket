from collections.abc import Callable, Coroutine

from src.bedrock.context import Context

EventHandler = Callable[[Context], Coroutine]


class Event:
    name: str
    handler: EventHandler

    def __init__(self, name: str, handler: EventHandler) -> None:
        self.name = name
        self.handler = handler

    async def __call__(self, ctx: Context, /) -> None:
        return await self.handler(ctx)
