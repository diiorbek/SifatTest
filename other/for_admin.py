import pandas as pd
import matplotlib.pyplot as plt
from aiogram import Bot, Dispatcher, filters
from aiogram.types import Message
from config import CHANNELS, TOKEN
import datetime
import sqlite3



def save_data(full_name, user_id, result, max_result, kind, is_exam):
    date = datetime.datetime.now().strftime("%d.%m.%Y")
    percent = int(result / max_result * 100)
    df = pd.DataFrame({
        "full_name": [full_name],
        "ID": [user_id],
        "result": [result],
        "max_result": [max_result],
        "percent": [f"{percent}%"],
        "kind": [kind],
        "date": [date],
        "is_exam": [is_exam],
    })
    df.to_csv("data.csv", header=False, mode="a", index=False)


def data():
    csv = pd.read_csv("data.csv")
    csv.to_excel("data.xlsx", index=False)


def create_diagram():
    df = pd.read_csv("data.csv")
    zur = 0
    yaxshi = 0
    qoniqarli = 0
    qoniqarsiz = 0

    results = df['percent']
    for result in results:
        if int(result[:-1]) >= 90:
            zur += 1
        elif int(result[:-1]) >= 75:
            yaxshi += 1
        elif int(result[:-1]) >= 50:
            qoniqarli += 1
        else:
            qoniqarsiz += 1

    labels = ["Zo'r", "Yaxshi", "Qoniqarli", "Qoniqarsiz"]
    colors = ['#21db14', '#0000ff', '#FF8000', '#ff0000']
    sizes = [zur, yaxshi, qoniqarli, qoniqarsiz]
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors)
    plt.savefig('data.png', format='png')


def get_user_results(user_id):
    user = {}
    user_data = []
    df = pd.read_csv("data.csv")
    indices = df[df['ID'] == user_id].index

    for u in indices:
        ID = df['ID'][u]
        result = df['result'][u]
        max_result = df['max_result'][u]
        kind = df['kind'][u]
        date = df['date'][u]
        user_data.append((ID, result, max_result, kind, date))

    user[user_id] = user_data
    return user

def users_count():
    connection = sqlite3.connect("baza/users.db")
    command = "SELECT * FROM users"
    cursor = connection.cursor()
    count_of_users = cursor.execute(command).fetchall()
    connection.close()
    return len(count_of_users)

