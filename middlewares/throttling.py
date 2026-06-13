import asyncio
from typing import Any, Callable, Dict, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message

class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, slow_down_time: float = 1.0):
        """
        slow_down_time: Xabarlar orasidagi majburiy kechikish vaqti (soniyada).
        Masalan: 1.0 = 1 soniyada faqat 1 ta xabar.
        """
        self.slow_down_time = slow_down_time
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        # Kod ishga tushishidan oldin majburiy sun'iy kechikish (sleep) beramiz
        await asyncio.sleep(self.slow_down_time)
        
        # Kechikish tugagach, xabarni keyingi bosqichga (handlerga) uzatamiz
        return await handler(event, data)