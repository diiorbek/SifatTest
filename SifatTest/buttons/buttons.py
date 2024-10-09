from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Test yechish📃"), KeyboardButton(text="Mening natijam🎯")],
        [KeyboardButton(text="Reyting🏆")],
        [KeyboardButton(text="Admin bilan bog'lanish🧑🏻‍💻")]
    ],
    resize_keyboard=True
)

subjects = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Python"), KeyboardButton(text="Aiogram")],
        [KeyboardButton(text="Django"), KeyboardButton(text="Kompyuter_savodxonligi")],
        [KeyboardButton(text="🔙Orqaga")]
    ],
    resize_keyboard=True
)

admin = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Savol qo'shish📄"), KeyboardButton(text="Reklama yuborish📩")],
        [KeyboardButton(text="Foydalanuvchilar datasi🗂️"), KeyboardButton(text="Foydalanuvchilar diagrammasi📊")],
        [KeyboardButton(text="Imtihonni boshlash☑️"), KeyboardButton(text="Imtihonni tugatish🛑")],
        [KeyboardButton(text="Foydalanuvchilar soni👤")]
    ],
    resize_keyboard=True
)

kind_of_subjects = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="python"), KeyboardButton(text="aiogram")],
        [KeyboardButton(text="django"), KeyboardButton(text="kompyuter_savodxonligi")]
    ],
    resize_keyboard=True
)

test_end = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Xatolarni ko'rmoq⚠️", callback_data="mistakes")],
    ]
)

back = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔙Ortga", callback_data="back")]
    ]
)

results_back = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Xatolarni ko'rmoq⚠️", callback_data="see_mistakes")],
        [InlineKeyboardButton(text="🔙Ortga", callback_data="results_back")]
    ]
)

results_back2 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔙Ortga", callback_data="results_back")]
    ]
)


back_to_result = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔙Ortga", callback_data="back_to_result")]
    ]
)

add_question = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Savol qo'shish📄")]
    ],
    resize_keyboard=True
)

reply_message = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Javob berish✨", callback_data="reply_message")],
        [InlineKeyboardButton(text="O'chirish❌", callback_data="delete_message")]
    ]
)

solve_exam = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Testni yechish🏃‍♂️", callback_data="start_solving_exam")]
    ]
)

rating_back = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔙Orqaga")]
    ],
    resize_keyboard=True
)