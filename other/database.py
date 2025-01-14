import sqlite3

def new_user(full_name, username, id):

    connection = sqlite3.connect("baza/users.db")

    command = f"""
        INSERT INTO users 
        VALUES ('{full_name}', '{username}', '{id}');

    """
    
    cursor = connection.cursor()
    cursor.execute(command)
    
    connection.commit()
    
def all_users_id():
    connection = sqlite3.connect("baza/users.db")
    
    command = """
    SELECT id FROM users
    
    """
    
    cursor = connection.cursor()
    cursor.execute(command)
    
    all_id = cursor.fetchall()
    id_list = []
    for id in all_id:
        for id2 in id:
            id_list.append(id2)
    
    return id_list
