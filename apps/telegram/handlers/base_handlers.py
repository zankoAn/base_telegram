import threading
from typing import cast

from django.contrib.auth.models import make_password
from django.utils.functional import cached_property

from apps.account.models import User as UserDB
from apps.bot.models import BotUpdateStatus
from apps.common._message import MessageManager
from apps.telegram.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from apps.telegram.telegram import Telegram
from apps.telegram.telegram_models import Chat, Update, User


class BaseHandler:
    """
    Base handler class that provides common utilities for processing Telegram updates,
    such as accessing user, chat, and message details.
    """

    def __init__(self, update: Update, bot: Telegram):
        """
        Initializes the handler with the incoming update and bot instance.
        """
        self.update = update
        self.bot = bot
        self.reply_keyboard = ReplyKeyboardBuilder()
        self.inline_keyboard = InlineKeyboardBuilder()
        self.bot_messages = MessageManager()

    @property
    def chat(self) -> Chat:
        """
        Returns the chat object from the update, if available.
        """
        chat = None
        if self.update.message:
            chat = self.update.message.chat

        if self.update.callback_query and self.update.callback_query.message:
            chat = self.update.callback_query.message.chat

        return cast(Chat, chat)

    @property
    def user(self) -> User:
        """
        Returns the user object who sent the update, if available.
        """
        user = None
        if self.update.message:
            user = self.update.message.from_user

        if self.update.callback_query:
            user = self.update.callback_query.from_user

        if self.update.inline_query:
            user = self.update.inline_query.from_user

        return cast(User, user)

    @property
    def chat_id(self) -> int:
        return self.chat.id if self.chat else 0

    @cached_property
    def user_obj(self) -> UserDB:
        if not self.is_private() or not self.user:
            return cast(UserDB, None)

        user, _ = UserDB.objects.get_or_create(
            user_id=self.user_id,
            defaults={
                "username": self.user.username or str(self.user_id),
                "password": make_password(str(self.user_id)),
                "first_name": self.user.first_name,
                "last_name": self.user.last_name or str(self.user_id),
            },
        )
        return user

    @property
    def user_step(self) -> str:
        return self.user_obj.step if self.user_obj else ""

    @property
    def user_id(self) -> int:
        return self.user.id if self.user else 0

    @property
    def text(self) -> str:
        text = ""
        if self.update.message:
            text = self.update.message.text

        if self.update.callback_query:
            text = self.update.callback_query.message.text

        return cast(str, text)

    def is_private(self) -> bool:
        if self.chat:
            return self.chat.type == "private"

        return False

    def is_group(self) -> bool:
        if self.chat:
            return self.chat.type in ("supergroup", "group")

        return False

    def is_update_mode(self):
        if self.user_obj.is_superuser:
            return False

        update_obj = BotUpdateStatus.objects.first()
        if update_obj and update_obj.is_update:
            return self.bot.send_message(self.chat_id, text=update_obj.update_msg)

        return False

    def is_user_block(self):
        if self.user_obj and not self.user_obj.is_active:
            return self.bot.send_message(self.chat_id, text="شما در ربات بلاک شده اید")

        return False

    def run_function_in_thread(self, func, *args, **kwargs):
        """
        Run the given function in a separate thread.
        """
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
        return thread
