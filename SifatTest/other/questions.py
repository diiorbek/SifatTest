import sqlite3
import pandas as pd

def add_question(question, a_var, b_var, c_var, d_var, correct_answer, kind):
    connection = sqlite3.connect("baza/questions.db")
    cursor = connection.cursor()

    command = f"""
    INSERT INTO {kind} (question, a_var, b_var, c_var, d_var, correct_answer)
    VALUES (?, ?, ?, ?, ?, ?);
    """

    params = (question, a_var, b_var, c_var, d_var, correct_answer)

    try:
        cursor.execute(command, params)
        connection.commit()
    except sqlite3.Error as e:
        print(f"Xatolik: {e}")
    finally:
        connection.close()

def find_result_index(user_id, index):
    data = pd.read_csv("data.csv")
    indexs = [i for i, val in enumerate(data["ID"]) if user_id == int(val)]

    if index >= len(indexs):
        return "Index out of range"

    son = indexs[index]

    return (f"Bu sizning {index+1}-chi yechgan testingiz.\n"
            f"Test <i><b>{data['kind'][son]}</b></i> bo'yicha bo'lgan.\n\n"
            f"Bu testdagi maksimum ball: <b>{data['max_result'][son]}</b>\n"
            f"Siz to'plagan ball esa: <b>{data['result'][son]}</b>\n"
            f"Bu testni siz <b>{data['percent'][son]}</b> foiz yechgansiz!\n\n"
            f"Sana: <code>{data['date'][son]}</code>")

def new_mistakes(user_id, question, user_answer, correct_answer, test):
    connection = sqlite3.connect("baza/mistakes.db")
    cursor = connection.cursor()

    try:
        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS mistakes_{user_id} (
            question TEXT,
            user_answer TEXT,
            correct_answer TEXT,
            test INTEGER
        );
        """)

        command2 = f"""
        INSERT INTO mistakes_{user_id}
        VALUES (?, ?, ?, ?);
        """

        params = (question, user_answer, correct_answer, test)
        cursor.execute(command2, params)
        connection.commit()

    except sqlite3.Error as e:
        print(f"Xatolik: {e}")
    finally:
        connection.close()

def show_mistakes(user_id, test):
    connection = sqlite3.connect("baza/mistakes.db")
    cursor = connection.cursor()

    command = f"""
    SELECT * FROM mistakes_{user_id} WHERE test = {test};
    """

    cursor.execute(command)
    mistakes = cursor.fetchall()

    txt = ""
    for index, mistake in enumerate(mistakes):
        question = mistake[0].replace("<", "&lt;").replace(">", "&gt;")
        user_answer = mistake[1].replace("<", "&lt;").replace(">", "&gt;")
        correct_answer = mistake[2].replace("<", "&lt;").replace(">", "&gt;")
        
        txt += (f"{index+1}) Savol: <b>{question}</b>\n\n"
                f"To'g'ri javob: <b>{correct_answer}</b>\n"
                f"Sizning javobingiz: <i><code>{user_answer}</code></i>\n\n")
                
    return txt


