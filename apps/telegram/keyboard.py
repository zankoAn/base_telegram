from apps.telegram.telegram_models import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)


class ReplyKeyboardBuilder:
    def home_keyboard(self):
        keyboard = [
            [KeyboardButton(text="دکمه دوم"), KeyboardButton(text="دکمه اول")],
            [KeyboardButton(text="دکمه چهارم"), KeyboardButton(text="دکمه سوم")],
        ]
        markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
        return markup.to_dict()

    def back_keyboard(self):
        keyboard = [[KeyboardButton(text="بازگشت")]]
        markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
        return markup.to_dict()

    def remove_keyboard(self):
        markup = ReplyKeyboardMarkup()
        return markup.to_dict()


class InlineKeyboardBuilder:
    def first_keyboard(self):
        keyboard = [
            [
                InlineKeyboardButton(text="دکمه دوم", callback_data="second_button"),
                InlineKeyboardButton(text="دکمه اول", callback_data="first_button"),
            ],
            [
                InlineKeyboardButton(text="دکمه چهارم", callback_data="fourth_button"),
                InlineKeyboardButton(text="دکمه سوم", callback_data="third_button"),
            ],
        ]
        makrup = InlineKeyboardMarkup(inline_keyboard=keyboard)
        return makrup.to_dict()

    def sponsor_channel_keyboard(self, channels):
        keyboard = [[]]
        for channel in channels.order_by("-other"):
            keyboard.append(
                InlineKeyboardMarkup(text=f"{channel.name}", url=channel.link)
            )

        if keyboard:
            keyboard.append(
                InlineKeyboardMarkup(
                    text="تایید عضویت ✅", callback_data="joined_to_sponsor"
                )
            )

        markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
        return markup.to_dict()

    def remove_keyboard(self):
        markup = InlineKeyboardMarkup()
        return markup.to_dict()
