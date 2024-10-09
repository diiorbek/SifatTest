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

def exam_test():
    connection = sqlite3.connect("baza/questions.db")
    command = f"SELECT * FROM python"
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
    test_list = test_list[:20]
    return test_list




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





