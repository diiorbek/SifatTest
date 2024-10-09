import asyncio
import logging
from aiogram.client.bot import DefaultBotProperties
from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import Message, CallbackQuery, FSInputFile, InlineKeyboardButton
from aiogram import F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from config import TOKEN, ADMINS, CHANNELS
from other.database import new_user, all_users_id
from other.questions import add_question, find_result_index, new_mistakes, show_mistakes
from buttons import buttons
from states import Form, Adverts, MessageAdmin, AdminStates
from other.start import test, all_answers, exam_test, users_rating
from other.for_admin import save_data, create_diagram, data, users_count#, IsCheckSubChannels
# from aiogram.client.session.aiohttp import AiohttpSession

import time
import pandas as pd

logging.basicConfig(level=logging.INFO)

# session = AiohttpSession(proxy='http://proxy.server:3128')

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
users = dict()
mistakes = {}
to_admin = dict()
is_exam = [False]
exam_txt = [""]

def create_inline_keyboard(user_id):
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(
        text="Javob berish",
        callback_data=f"reply:{user_id}"
    )


    return keyboard_builder.as_markup()

def create_exam_keyboard(user_id):
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(
        text="Ha✅",
        callback_data=f"start_exam:yes_{user_id}"
    )

    keyboard_builder.button(
        text="Yoq❌",
        callback_data=f"start_exam:no_{user_id}"
    )


    return keyboard_builder.as_markup()


def len_tests(user_id):
  data = pd.read_csv("data.csv")

  ids = list(data["ID"])

  return ids.count(user_id)


@dp.message(Command("start"))
async def command_start_handler(message: Message):

    txt = (f"👋 Assalomu alaykum, {message.from_user.full_name}! Sizni botimizda ko'rganimdan xursandman!\n"
           "Ushbu botda siz dasturlash bo'yicha turli testlarni yechishingiz mumkin.\n"
           "🎯 O'yinni boshlash uchun sizga tegishli testni tanlang va savollarga javob bering.\n"
           "Omad tilayman! 🍀")
    try:
        new_user(message.from_user.full_name, message.from_user.username, message.from_user.id)
        await bot.send_message(chat_id=message.from_user.id, text=txt, reply_markup=buttons.menu)
    except:
        await bot.send_message(chat_id=message.from_user.id, text=txt, reply_markup=buttons.menu)



# @dp.message(IsCheckSubChannels())
# async def kanalga_obuna(message:Message):
#     text = ""
#     inline_channel = InlineKeyboardBuilder()
#     for index,channel in enumerate(CHANNELS):
#         ChatInviteLink = await bot.create_chat_invite_link(channel)
#         inline_channel.add(InlineKeyboardButton(text=f"{index+1}-kanal",url=ChatInviteLink.invite_link))
#     inline_channel.adjust(1,repeat=True)
#     button = inline_channel.as_markup()
#     await message.answer(f"{text} kanallarga azo bo'ling",reply_markup=button)

@dp.message(F.text == "Mening natijam🎯")
async def result_of_user(message: types.Message):
    # user_id = message.from_user.id
    await show_page(message.from_user.id, 0)

async def show_page(user_id: int, page: int):

    total_tests = len_tests(user_id=user_id)
    if total_tests != 0:
        buttons_per_page = 5
        pages = (total_tests + buttons_per_page - 1) // buttons_per_page

        builder = InlineKeyboardBuilder()

        start_index = page * buttons_per_page
        end_index = min(start_index + buttons_per_page, total_tests)

        for i in range(start_index, end_index):
            builder.add(InlineKeyboardButton(text=f"Test {i + 1}", callback_data=f"test_{i}"))

        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton(text="⬅️ Ortga", callback_data=f"prev_{page - 1}"))
        if page < pages - 1:
            navigation_buttons.append(InlineKeyboardButton(text="Oldinga ➡️", callback_data=f"next_{page + 1}"))

        if navigation_buttons:
            builder.add(*navigation_buttons)
        builder.adjust(1)


        await bot.send_message(chat_id=user_id, text=f"Sizning yechgan testlaringiz. {page + 1} bet:", reply_markup=builder.as_markup())

    else:
        await bot.send_message(chat_id=user_id, text=f"Afsuski, siz hozircha test yechmagansiz😔 \nTest yechish uchun 'Test yechish📃' tugmasini bosing!")

@dp.message(F.text == "Reyting🏆")
async def show_users_rating(message: Message):
    rating_txt = await users_rating(bot=bot)
    await message.answer(text=rating_txt, reply_markup=buttons.rating_back)

@dp.message(F.text == "Imtihonni boshlash☑️")
async def admin_start_exam(message: Message):
    if str(message.from_user.id) in ADMINS:
        if is_exam[0] == False:
            await message.answer(text="Sifat imtihoniga start berildi🥳\nImtihonni tugatish uchun 'Imtihonni tugatish🛑' tugmasini bosing!")
            is_exam.clear()
            is_exam.append(True)
        else:
            await message.answer(text="Hozrida imtihon ketmoqda...\nImtihonni to'xtatish uchun 'Imtihonni tugatish🛑' tugmasini bosing!")

@dp.message(F.text == "Imtihonni tugatish🛑")
async def admin_start_exam(message: Message):
    if str(message.from_user.id) in ADMINS:
        if is_exam[0] == False:
            await message.answer(text="Hozirda imtihon bo'lmayapti...\nImtihonni boshlash uchun 'Imtihonni boshlash☑️' tugmasini bosing!")
        else:
            await message.answer(text=f"Sifat imtihoni yakunlandi🤚\nNatijalar🚀:\n\n{exam_txt[0]}Hun tarzda davom etamiz😉")
            exam_txt[0] = ""
            is_exam.clear()
            is_exam.append(False)


@dp.message(F.text == "Test yechish📃")
async def start_test(message: Message):
    await bot.send_message(chat_id=message.from_user.id, text="Nima bo'yicha test yechmoqchisiz?", reply_markup=buttons.subjects)

@dp.message(F.text=="🔙Orqaga")
async def back_menu_handler(message: Message):
    # user_id = message.from_user.id
    txt = (f"👋 Assalomu alaykum, {message.from_user.full_name}! Sizni botimizda ko'rganimdan xursandman!\n"
           "Ushbu botda siz dasturlash bo'yicha turli testlarni yechishingiz mumkin.\n"
           "🎯 O'yinni boshlash uchun sizga tegishli testni tanlang va savollarga javob bering.\n"
           "Omad tilayman! 🍀")
    try:
        new_user(message.from_user.full_name, message.from_user.username, message.from_user.id)
        await bot.send_message(chat_id=message.from_user.id, text=txt, reply_markup=buttons.menu)
    except:
        await bot.send_message(chat_id=message.from_user.id, text=txt, reply_markup=buttons.menu)

    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)

@dp.message(Command("exam"))
async def start_exam(message: Message):
    if is_exam[0] == True:
        for admin in ADMINS:
            btn = create_exam_keyboard(message.from_user.id)
            user = await bot.get_chat(chat_id=message.from_user.id)
            await bot.send_message(chat_id=admin, text=f"@{user.username} ekzamenda qatnashmoqchi!\nRuxsat berasizmi?", reply_markup=btn)

@dp.message(F.text.in_(["Kompyuter_savodxonligi", "Python", "Django", "Aiogram"]))
async def start_the_test(message: Message):
    # global testing
    if message.from_user.id not in list(users.keys()):
        testing = test(message.text.lower())
        users[message.from_user.id] = {
            "question": 1,
            "correct": 0,
            "kind": message.text,
            "testing": testing,
            "answers": [],
            "exam": False
        }

        builder = InlineKeyboardBuilder()
        for count,i in enumerate(users[message.from_user.id]['testing'][0][1:-1]):
            builder.add(types.InlineKeyboardButton(text=str(i), callback_data=str(i)))
        builder.adjust(2)
        await bot.send_message(chat_id=message.from_user.id, text=f"1. {users[message.from_user.id]['testing'][0][0]}", reply_markup=builder.as_markup())

    else:
        await message.answer(f"Siz hozirda {users[message.from_user.id]['kind']} bo'yicha test yechmoqdasiz!\nShu testni tugatib, keyin yangi test yechishingiz mumkin!")



@dp.callback_query(F.data)
async def test_1(callback: CallbackQuery, state: FSMContext):

    if callback.data in all_answers():

        full_name = callback.from_user.full_name

        try:
            builder = InlineKeyboardBuilder()
            for count,i in enumerate(users[callback.from_user.id]['testing'][users[callback.from_user.id]["question"]][1:-1]):
                builder.add(types.InlineKeyboardButton(text=str(i), callback_data=str(i)))
            builder.adjust(2)
            await bot.edit_message_text(chat_id=callback.from_user.id, text=f"{users[callback.from_user.id]['question']+1}. {users[callback.from_user.id]['testing'][users[callback.from_user.id]['question']][0]}", message_id=callback.message.message_id, reply_markup=builder.as_markup())

            users[callback.from_user.id]["question"] += 1
            users[callback.from_user.id]["answers"].append(callback.data)


        except IndexError:



            users[callback.from_user.id]["answers"].append(callback.data)


            for i in range(0, users[callback.from_user.id]['question']):
                if users[callback.from_user.id]["answers"][i] == users[callback.from_user.id]['testing'][i][-1]:
                    users[callback.from_user.id]["correct"] += 1
                else:
                        new_mistakes(user_id=str(callback.from_user.id), question=users[callback.from_user.id]['testing'][i][0], user_answer=users[callback.from_user.id]["answers"][i], correct_answer=users[callback.from_user.id]['testing'][i][-1], test=(int(len_tests(callback.from_user.id))+1))

            nat = users[callback.from_user.id]["correct"]
            questions_count = users[callback.from_user.id]["question"]
            percent = nat / questions_count * 100

            if percent >= 90:
                tabrik = "Siz testni juda ham zo'r yechdingiz!\nEndi esa boshqa fanlardan bilimingizni sinab ko'ring!\nTestimiz yoqdi degan umiddamiz🥰"

            elif percent >= 70 and nat <= 80:
                tabrik = "Siz testni yaxshi yechdingiz, lekin bundan ham zo'r yechishingiz mumkin edi. Testni yana bir marta yechib ko'ring!"

            elif percent >= 50 and nat <= 60:
                tabrik = "Afsuski, siz testni juda ham yaxshi yechmadingiz😔\nTestni qaytadan o'tib ko'ring."

            elif percent < 50:
                tabrik = "Afsuski, siz testni juda yomon yechdingiz😭\nTestni qayta yechib ko'rishingiz shart!"

            global txt
            txt = f"Tabriklaymiz, {full_name}! Siz testni tugatdingiz🥳\nSizning natijangiz: {users[callback.from_user.id]['correct']}/{users[callback.from_user.id]['question']} | {int(percent)}%\n{tabrik}"


            if percent == 100:
                await bot.send_message(chat_id=callback.from_user.id, text=txt)

            if percent < 100 and percent >= 50:
                await bot.send_message(chat_id=callback.from_user.id, text=txt, reply_markup=buttons.test_end)

            if percent < 50:
                voice = FSInputFile("voice.ogg")
                await bot.send_audio(chat_id=callback.from_user.id, audio=voice, caption=txt, reply_markup=buttons.test_end)


            
            save_data(full_name=callback.from_user.full_name, user_id=callback.from_user.id, result=users[callback.from_user.id]["correct"], max_result=users[callback.from_user.id]["question"], kind=users[callback.from_user.id]["kind"], is_exam=users[callback.from_user.id]["exam"])

            for admin in ADMINS:
                if users[callback.from_user.id]['exam'] == False:
                    await bot.send_message(chat_id=admin, text=f"{full_name} testni tugatdi!\n{users[callback.from_user.id]['kind']} bo'yicha {users[callback.from_user.id]['correct']}/{users[callback.from_user.id]['question']} | {int(percent)}% yechdi.")

                if users[callback.from_user.id]['exam'] == True:
                    await bot.send_message(chat_id=admin, text=f"@{callback.from_user.username} ekzamen testini tugatdi!\nEkzamenni {users[callback.from_user.id]['correct']}/{users[callback.from_user.id]['question']} | {int(percent)}% yechdi.")
            
            if users[callback.from_user.id]['exam'] == True:
                exam_txt[0] += f"• 👤{callback.from_user.full_name} - {int(percent)}%\n"
                print(exam_txt[0])
            await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
            del users[callback.from_user.id]

    else:
        if callback.data == "mistakes":
            user_mistakes = int(len_tests(callback.from_user.id))
            mistakes_txt = show_mistakes(user_id=callback.from_user.id, test=user_mistakes)
            await bot.send_message(chat_id=callback.from_user.id, text=mistakes_txt, reply_markup=buttons.back)
            await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)


        elif callback.data.startswith('prev_') or callback.data.startswith('next_'):
            global page
            # user_id = callback.from_user.id
            action, page = callback.data.split('_')
            page = int(page)

            if action == 'prev':
                page = max(page, 0)
            elif action == 'next':
                total_tests = len_tests(user_id=callback.from_user.id)
                buttons_per_page = 5
                pages = (total_tests + buttons_per_page - 1) // buttons_per_page
                page = min(page, pages - 1)

            await show_page(callback.from_user.id, page)
            await callback.answer()
            await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
        elif callback.data.startswith("test_"):
            global son
            # user_id = callback.from_user.id
            word,son = callback.data.split("_")
            son = int(son)
            your_mistakes = show_mistakes(callback.from_user.id, son+1)
            test_txt = find_result_index(user_id=callback.from_user.id, index=son)

            if your_mistakes != "":
                await bot.send_message(chat_id=callback.from_user.id, text=test_txt, reply_markup=buttons.results_back)
                await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)

            else:
                await bot.send_message(chat_id=callback.from_user.id, text=test_txt, reply_markup=buttons.results_back2)
                await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)


        elif callback.data == "back":

            await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
            await bot.send_message(chat_id=callback.from_user.id, text=txt, reply_markup=buttons.test_end)

        elif callback.data == "results_back":
            try:
                # user_id = callback.from_user.id
                await show_page(user_id=callback.from_user.id, page=page)
                await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
            except:
                user_id = callback.from_user.id
                await show_page(user_id=callback.from_user.id, page=0)
                await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)

        elif callback.data == "see_mistakes":
            all_mistakes = show_mistakes(user_id=callback.from_user.id, test=son+1)
            await bot.send_message(chat_id=callback.from_user.id, text=all_mistakes, reply_markup=buttons.back_to_result)
            await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)


        elif callback.data == "back_to_result":
            # user_id = callback.from_user.id
            test_txt = find_result_index(user_id=callback.from_user.id, index=son)

            await bot.send_message(chat_id=callback.from_user.id, text=test_txt, reply_markup=buttons.results_back)
            await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)

        elif callback.data == "reply_message":
            # await state.set_state(AdminSend.admin_text)
            await callback.message.answer(text="Javob yozing!")

        elif callback.data.startswith("reply:"):
            user_id = int(callback.data.split(":")[1])
            await callback.message.answer("Javobingizni yuboring📩")
            await state.update_data(reply_user_id=user_id)
            await state.set_state(AdminStates.waiting_for_reply_message)
            await callback.answer()

        elif callback.data.startswith("start_exam"):
            ruxsat = callback.data.split(":")[1]
            exam_user_id = ruxsat.split("_")[1]
            ruxsat = ruxsat.split("_")[0]
            if ruxsat == "yes":
                start_solving_exam = InlineKeyboardBuilder()
                start_solving_exam.button(
                    text="Testni yechish🏃‍♂️",
                    callback_data=f"start_solving_exam:{exam_user_id}"
                )

                await bot.send_message(chat_id=exam_user_id, text="Admin sizga ekzamenda qatnashishga ruxsat berdi✅", reply_markup=start_solving_exam.as_markup())


            if ruxsat == "no":
                await bot.send_message(chat_id=exam_user_id, text="Admin sizga ekzamenda qatnashishga ruxsat bermadi❌")


        elif callback.data.startswith("start_solving_exam"):
            examing_user_id = int(callback.data.split(":")[1])

            testing = exam_test()
            users[examing_user_id] = {
                "question": 1,
                "correct": 0,
                "kind": "python",
                "testing": testing,
                "answers": [],
                "exam": True
            }

            builder = InlineKeyboardBuilder()
            for count,i in enumerate(users[examing_user_id]['testing'][0][1:-1]):
                builder.add(types.InlineKeyboardButton(text=str(i), callback_data=str(i)))
            builder.adjust(2)
            await bot.send_message(chat_id=examing_user_id, text=f"1. {users[examing_user_id]['testing'][0][0]}", reply_markup=builder.as_markup())
            await callback.message.delete()

# @dp.message(AdminSend.admin_text)
# async def admin_sending(message: Message, state: FSMContext):
#     admin_text = message.text
#     await state.update_data(admin_text=admin_text)

#     await bot.send_message(chat_id=to_admin[])
    # to_admin

@dp.startup()
async def start_bot():
    for admin in ADMINS:
        try:
            await bot.send_message(chat_id=admin, text="Bot ishga tushdi!")
        except Exception as e:
            logging.error(f"{admin} Adminga yuborishda xatolik yuz berdi: {e}")

@dp.shutdown()
async def shutdown_bot():
    for admin in ADMINS:
        try:
            await bot.send_message(chat_id=admin, text="Bot ishdan to'xtadi!")
        except Exception as e:
            logging.error(f"{admin} Adminga yuborishda xatolik yuz berdi: {e}")

from aiogram.types import ContentType

@dp.message(F.text == "Admin bilan bog'lanish🧑🏻‍💻")
async def message_to_admin(message: Message, state: FSMContext):
    await message.answer("👨‍💼Admin uchun xabar yuboring!")
    await state.set_state(AdminStates.waiting_for_admin_message)

@dp.message(AdminStates.waiting_for_admin_message, F.content_type.in_([
    ContentType.TEXT, ContentType.AUDIO, ContentType.VOICE, ContentType.VIDEO,
    ContentType.PHOTO, ContentType.ANIMATION, ContentType.STICKER,
    ContentType.LOCATION, ContentType.DOCUMENT, ContentType.CONTACT,
    ContentType.VIDEO_NOTE
]))

async def handle_admin_message(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name or ""

    if username:
        user_identifier = f"@{username}"
    else:
        user_identifier = f"{first_name} {last_name}".strip()
    video_note = message.video_note
    inline_keyboard = create_inline_keyboard(user_id)
    for admin_id in ADMINS:
        try:
            if video_note:
                print('adfs', message.video_note.file_id)
                # Echo the video note back to the user
                await bot.send_video_note(
                    admin_id,
                    video_note.file_id,
                    reply_markup=inline_keyboard
                )
            elif message.text:
                await bot.send_message(
                    admin_id,
                    f"👤Foydalanuvchi: {user_identifier}\n📜Xabar: {message.text}",
                    reply_markup=inline_keyboard
                )
            elif message.audio:
                await bot.send_audio(
                    admin_id,
                    message.audio.file_id,
                    caption=f"👤Foydalanuvchi: {user_identifier}\n🎙Audio xabar",
                    reply_markup=inline_keyboard
                )
            elif message.voice:
                await bot.send_voice(
                    admin_id,
                    message.voice.file_id,
                    caption=f"👤Foydalanuvchi: {user_identifier}\n⏺Voice xabar",
                    reply_markup=inline_keyboard
                )
            elif message.video:
                await bot.send_video(
                    admin_id,
                    message.video.file_id,
                    caption=f"👤Foydalanuvchi: {user_identifier}\n▶️Video xabar",
                    reply_markup=inline_keyboard
                )
            elif message.photo:
                await bot.send_photo(
                    admin_id,
                    message.photo[-1].file_id,  # using the highest resolution photo
                    caption=f"👤Foydalanuvchi: {user_identifier}\n🏞Rasm xabar",
                    reply_markup=inline_keyboard
                )
            elif message.animation:
                await bot.send_animation(
                    admin_id,
                    message.animation.file_id,
                    caption=f"👤Foydalanuvchi: {user_identifier}\n📜GIF xabar",
                    reply_markup=inline_keyboard
                )
            elif message.sticker:
                await bot.send_sticker(
                    admin_id,
                    message.sticker.file_id,
                    reply_markup=inline_keyboard
                )
            elif message.location:
                await bot.send_location(
                    admin_id,
                    latitude=message.location.latitude,
                    longitude=message.location.longitude,
                    reply_markup=inline_keyboard
                )
            elif message.document:
                await bot.send_document(
                    admin_id,
                    message.document.file_id,
                    caption=f"👤Foydalanuvchi: {user_identifier}\n🗂Hujjat xabar",


                    reply_markup=inline_keyboard
                )
            elif message.contact:
                await bot.send_contact(
                    admin_id,
                    phone_number=message.contact.phone_number,
                    first_name=message.contact.first_name,
                    last_name=message.contact.last_name or "",
                    reply_markup=inline_keyboard
                )
        except Exception as e:
            logging.error(f"Error sending message to admin {admin_id}: {e}")

    await state.clear()
    await bot.send_message(user_id, "Admin sizga javob berishi mumkin!✅")


@dp.message(AdminStates.waiting_for_reply_message)
async def handle_admin_reply(message: Message, state: FSMContext):
    data = await state.get_data()
    original_user_id = data.get('reply_user_id')

    if original_user_id:
        try:
            if message.text:
                await bot.send_message(original_user_id, f"Admin javobi✅\n{message.text}")
            elif message.voice:
                await bot.send_voice(original_user_id, message.voice.file_id)

            elif message.video_note:
                await bot.send_video_note(original_user_id, message.video_note.file_id)

            elif message.audio:
                await bot.send_audio(original_user_id, message.audio.file_id)

            elif message.sticker:
                await bot.send_sticker(original_user_id, message.sticker.file_id)

            elif message.video:
                await bot.send_video(original_user_id, message.video.file_id)


            await bot.send_message(ADMINS[0], "Foydalanuvchiga habaringiz yuborildi!✅")
            await state.clear()  # Clear state after sending the reply
        except Exception as e:
            print(f"Error sending reply to user {original_user_id}: {e}")
            await message.reply("Xatolik: Javob yuborishda xato yuz berdi.")
    else:
        await message.reply("Xatolik: Javob yuborish uchun foydalanuvchi ID topilmadi.")



@dp.message(Command("help"))
async def command_help_handler(message: Message):
    txt = """❓ Yordam kerakmi? Mana botning asosiy funksiyalari:
- /start - o'yinni boshlash 🚀
- /about - bot haqida ma'lumot ℹ️
- /help - yordam bo'limi 📚

Savollarga javob berishda muammo yuzaga kelsa yoki boshqa yordam kerak bo'lsa, bu yerga yozing. Biz sizga yordam berishdan mamnunmiz! 💬

    """
    await message.answer(text=txt)

@dp.message(Command("about"))
async def command_about_handler(message: Message):
    txt = """ℹ️ Bu bot dasturlash bo'yicha bilimlaringizni sinab ko'rish uchun yaratilgan. Botda siz turli darajadagi testlarni yechib, o'z bilimlaringizni oshirishingiz mumkin.

🧠 Bot doimiy ravishda yangilanib boriladi va yangi savollar qo'shilib turadi.
🎉 Maqsadimiz - sizning dasturlashga bo'lgan qiziqishingizni oshirish va bilimlaringizni mustahkamlash. 🚀"""
    await message.answer(text=txt)

@dp.message(Command("admin"))
async def command_admin_handler(message: Message):
    if str(message.from_user.id) in ADMINS:
        await message.answer(text="Assalomu alaykum, Admin!", reply_markup=buttons.admin)

@dp.message(F.text == "Foydalanuvchilar datasi🗂️")
async def send_data(message: Message):
    if str(message.from_user.id) in ADMINS:
        data()
        input_file = FSInputFile("data.xlsx")
        await bot.send_document(chat_id=message.from_user.id, document=input_file)

@dp.message(F.text == "Foydalanuvchilar diagrammasi📊")
async def send_data(message: Message):
    if str(message.from_user.id) in ADMINS:
        create_diagram()
        photo = FSInputFile("data.png")
        await message.answer_photo(photo=photo)

@dp.message(F.text=="Reklama yuborish📩")
async def advert_dp(message:Message,state:FSMContext):
    if str(message.from_user.id) in ADMINS:
        await state.set_state(Adverts.adverts)
        await message.answer(text="Reklama yuborishingiz mumkin !")

@dp.message(Adverts.adverts)
async def send_advert(message:Message,state:FSMContext):

    message_id = message.message_id
    from_chat_id = message.from_user.id
    users = all_users_id()
    count = 0
    for user in users:
        try:
            await bot.copy_message(chat_id=user,from_chat_id=from_chat_id,message_id=message_id)
            count += 1
        except:
            pass
        time.sleep(0.5)

    await message.answer(f"Reklama {count}ta foydalanuvchiga yuborildi")
    await state.clear()


@dp.message(F.text == "Foydalanuvchilar soni👤")
async def show_users_count(message: Message):
    if str(message.from_user.id) in ADMINS:
        await message.answer(f"Hozrida botda foydalanuvchilar soni: {users_count()}ta.")


@dp.message(F.text == "Savol qo'shish📄")
async def add_question_admin(message: Message, state: FSMContext):
    if str(message.from_user.id) in ADMINS:
        await state.set_state(Form.question)
        await bot.send_message(chat_id=message.from_user.id, text="Savolni kiriting!")

@dp.message(F.text, Form.question)
async def question_state(message: Message, state: FSMContext):
    question = message.text
    await state.update_data(question=question)
    await state.set_state(Form.a_var)
    await bot.send_message(chat_id=message.from_user.id, text="A variantni kiriting!")

@dp.message(F.text, Form.a_var)
async def a_var_state(message: Message, state: FSMContext):
    a_var = message.text
    await state.update_data(a_var=a_var)
    await state.set_state(Form.b_var)
    await bot.send_message(chat_id=message.from_user.id, text="B variantni kiriting!")

@dp.message(F.text, Form.b_var)
async def b_var_state(message: Message, state: FSMContext):
    b_var = message.text
    await state.update_data(b_var=b_var)
    await state.set_state(Form.c_var)
    await bot.send_message(chat_id=message.from_user.id, text="C variantni kiriting!")

@dp.message(F.text, Form.c_var)
async def c_var_state(message: Message, state: FSMContext):
    c_var = message.text
    await state.update_data(c_var=c_var)
    await state.set_state(Form.d_var)
    await bot.send_message(chat_id=message.from_user.id, text="D variantni kiriting!")

@dp.message(F.text, Form.d_var)
async def d_var_state(message: Message, state: FSMContext):
    d_var = message.text
    await state.update_data(d_var=d_var)
    await state.set_state(Form.correct_answer)
    await bot.send_message(chat_id=message.from_user.id, text="To'g'ri javobi bor variantni kiriting!")

@dp.message(F.text, Form.correct_answer)
async def correct_answer_state(message: Message, state: FSMContext):
    your_correct_answer = message.text
    await state.update_data(correct_answer=your_correct_answer)
    await state.set_state(Form.kind)
    await message.answer(text="Testingiz nima bo'yichaligini tanlang!", reply_markup=buttons.kind_of_subjects)


@dp.message(F.text, Form.kind)
async def kind_state(message: Message, state: FSMContext):
    your_kind = message.text
    await state.update_data(kind=your_kind)

    data = await state.get_data()
    question = data.get('question')

    a_var = data.get('a_var')
    b_var = data.get('b_var')
    c_var = data.get('c_var')
    d_var = data.get('d_var')
    correct_answer = str(data.get('correct_answer')).lower()
    kind = data.get('kind')

    if correct_answer == "a":
        correct_answer = a_var
    elif correct_answer == "b":
        correct_answer = b_var
    elif correct_answer == "c":
        correct_answer = c_var
    elif correct_answer == "d":
        correct_answer = d_var

    try:
        add_question(question=question, a_var=a_var, b_var=b_var, c_var=c_var, d_var=d_var, correct_answer=correct_answer, kind=kind)
        await message.answer(text="Savolingiz bazaga muvaffaqiyatli saqlandi✅", reply_markup=buttons.add_question)

    except:
        await message.answer(text="Afsuski, savolingiz bazaga saqlanmadi❌", reply_markup=buttons.add_question)

    data.clear()

async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
