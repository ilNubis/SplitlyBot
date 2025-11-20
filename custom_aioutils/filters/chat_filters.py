from typing import Union, Dict, Any
from aiogram.types import Message
from aiogram.filters import Filter


class UserJoinChat(Filter):
    def __init__(self, user_id: int) -> None:
        super().__init__()
        self.user_id: int = user_id

    async def __call__(self, *args: Any, **kwargs: Any) -> Union[bool, Dict[str, Any]]:
        msg: Message= args[0]

        if not msg.new_chat_member:
            return False

        return msg.new_chat_member["id"] == self.user_id


class UserLeftChat(Filter):
    def __init__(self, user_id: int) -> None:
        super().__init__()
        self.user_id: int = user_id

    async def __call__(self, *args: Any, **kwargs: Any) -> Union[bool, Dict[str, Any]]:
        msg: Message = args[0]
        

        if not msg.left_chat_member:
            return False

        return msg.left_chat_member.id == self.user_id