import sqlite3
import random
import pandas as pd

def test(kind):
    connection = sqlite3.connect("baza/questions.db")
    command = f"SELECT * FROM {kind}"
    cursor = connection.cursor()
    cursor.execute(command)
    begin_test = cursor.fetchall()

    test_list = []

    for test in begin_test:
        question_id = test[0]
        options = list(test[1:-1])
        correct = test[-1]
        random.shuffle(options)
        test_list.append([question_id] + options + [correct])

    random.shuffle(test_list)
    test_list = test_list[:10]
    return test_list


tests = [
        # Aiogram
        ["Aiogram botida dispatcherni qanday yaratamiz?", "dp = Dispatcher(bot)", "dp = Dispatch(bot)", "dp = Dispatchar(bot)", "dp = BotDispatcher(BOT)", "dp = Dispatcher(bot)"],
        ["Botda HTML formatida xabar yuborish uchun qaysi parametrdan foydalaniladi?", "message_type='html'", "parse_mode='html'", "message_format='html'", "format='html'", "parse_mode='html'"],
        ["Foydalanuvchiga xabar yuborib, unga tugmalarni biriktirish uchun qaysi parametr ishlatiladi?", "buttons=...", "keyboard_buttons=...", "inline_buttons=...", "reply_markup=...", "reply_markup=..."],
        ["Xabarni javob sifatida yuborish uchun qaysi metod ishlatiladi?", "bot.send_message()", "bot.reply_message()", "message.answer()", "message.send_response()", "message.answer()"],
        ["Botga xabar kelganida uni qabul qilish uchun qaysi dekorator ishlatiladi?", "@dp.callback_handler()", "@dp.callback_handler()", "@dp.message_handler()", "@dp.event_handler()", "@dp.message_handler()"],
        ["Botda xabar yuborishda foydalanuvchining ismini qo'shish uchun qanday o'zgaruvchi ishlatiladi?", "message.user.first_name", "message.from_user.first_name", "message.from_user_id.first_name", "message.from_user.full_name", "message.from_user.first_name"],
        ["Aiogram'da start_polling() funksiyasi nima uchun ishlatiladi?", "Botni ishga tushirish", "API-ni kuzatish uchun", "Foydalanuvchi holatini boshqarish uchun", "Inline tugmalarni yaratish uchun", "Botni ishga tushirish"],
        ["Aiogram botida Token ni xavfsiz saqlash uchun qaysi usul ishlatiladi?", "Matnli faylda saqlash", "Kod ichida qoldirish", ".env faylida saqlash", "Faylga yozib qo'yish", ".env faylida saqlash"],
        ["Callback Query handler orqali kelgan ma'lumotni olish uchun qaysi xususiyat ishlatiladi?", "callback.query", "callback.data", "callback.answer", "callback.message", "callback.data"],
        ["SQLite ma'lumotlar bazasidan ma'lumotlarni olish uchun qaysi buyruq ishlatiladi?", "FETCH", "PULL", "GET", "SELECT", "SELECT"]
]




def all_answers():
    connection = sqlite3.connect("baza/questions.db")
    answers_list = []

    for language in ["python", "django", "aiogram", "kompyuter_savodxonligi"]:
        command = f"SELECT a_var,b_var,c_var,d_var FROM {language}"
        cursor = connection.cursor()

        cursor.execute(command)
        answers = cursor.fetchall()
        for answer in answers:
            for u in answer:
                answers_list.append(u)

    return answers_list


async def users_rating(bot):
    df = pd.read_csv("data.csv")

    df['percent'] = df['percent'].str.rstrip('%').astype(float)
    
    df = df.sort_values('percent', ascending=False).drop_duplicates(subset='ID')
    
    top_10 = df.head(10)
    
    result_text = "🏆 Top 10ta eng ko'p yechgan odamlar:\n\n"
    for i, row in enumerate(top_10.itertuples(), 1):
        user = await bot.get_chat(chat_id=row.ID)
        if row.kind == "Kompyuter_savodxonligi":
            result_text += f"{i}. 👤{user.full_name}, Kompyuter savodxonligi - {int(row.percent)}%\n"
        
        else:
            result_text += f"{i}. 👤{user.full_name}, {row.kind.capitalize()} - {int(row.percent)}%\n"
        
    result_text += "\n💪 Yaxshi, shu tarzda davom etamiz!"
    
    return result_text


async def exam_rating(bot):
    df = pd.read_csv("data.csv")

    df['percent'] = df['percent'].str.rstrip('%').astype(float)

    df = df[df['is_exam'] == True]

    df = df.sort_values('percent', ascending=False).drop_duplicates(subset='ID')

    top_10 = df.head(10)

    result_text = "🏆 Top 10ta eng ko'p yechgan odamlar:\n\n"
    for i, row in enumerate(top_10.itertuples(), 1):
        user = await bot.get_chat(chat_id=row.ID)

        if row.kind == "Kompyuter_savodxonligi":
            result_text += f"{i}. 👤{user.full_name}, Kompyuter savodxonligi - {int(row.percent)}%\n"
        else:
            result_text += f"{i}. 👤{user.full_name}, {row.kind.capitalize()} - {int(row.percent)}%\n"
        
    result_text += "\n💪 Yaxshi, shu tarzda davom etamiz!"
    
    return result_text





