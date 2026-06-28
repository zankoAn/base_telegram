from apps.telegram.handlers.base_handlers import BaseHandler
from apps.telegram.telegram import Telegram
from apps.telegram.telegram_models import (
    InlineQueryResultArticle,
    InputTextMessageContent,
    Update,
)


class InlineQueryHandler(BaseHandler):
    def __init__(self, update: Update, bot: Telegram):
        super().__init__(update, bot)
        self.callback_handlers = {
            "a": self.test_a,
        }

    def test_a(self):
        self.bot.answer_inline_query(
            self.inline_query.id,
            [
                InlineQueryResultArticle(
                    id=str(self.inline_query.id),
                    title="Title A",
                    input_message_content=InputTextMessageContent(
                        message_text="inline msg a"
                    ),
                )
            ],
        )

    def handle(self):
        if self.is_update_mode():
            return

        if self.is_user_block():
            return

        _handler = self.callback_handlers.get(self.inline_query.query)
        if _handler:
            return _handler()
