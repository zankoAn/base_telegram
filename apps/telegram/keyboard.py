from apps.telegram.telegram_models import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    ReplyMarkup,
)


class ReplyKeyboardBuilder:
    def home_keyboard(self) -> ReplyMarkup:
        keyboard = [
            [KeyboardButton(text="دکمه دوم"), KeyboardButton(text="دکمه اول")],
            [KeyboardButton(text="دکمه چهارم"), KeyboardButton(text="دکمه سوم")],
        ]
        markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
        return markup

    def back_keyboard(self) -> ReplyMarkup:
        keyboard = [[KeyboardButton(text="بازگشت")]]
        markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
        return markup

    def remove_keyboard(self) -> ReplyMarkup:
        markup = ReplyKeyboardRemove()
        return markup


class InlineKeyboardBuilder:
    def first_keyboard(self) -> ReplyMarkup:
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
        return makrup

    def sponsor_channel_keyboard(self, channels) -> ReplyMarkup:
        keyboard = [[]]
        for channel in channels.order_by("-other"):
            keyboard.append(
                [InlineKeyboardButton(text=f"{channel.name}", url=channel.link)]
            )

        if keyboard:
            keyboard.append(
                [
                    InlineKeyboardButton(
                        text="تایید عضویت ✅", callback_data="joined_to_sponsor"
                    )
                ]
            )

        markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
        return markup

    def remove_keyboard(self) -> ReplyMarkup:
        markup = ReplyKeyboardRemove()
        return markup
