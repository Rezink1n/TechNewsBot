import sqlite3

# conn = sqlite3.connect('files/users.db')
# cur = conn.cursor()


def create_db():
    conn = sqlite3.connect('files/users.db')
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
       id TEXT PRIMARY KEY,
       name TEXT,
       username TEXT);
    """)
    conn.commit()


def add_user(id, name, username):
    conn = sqlite3.connect('files/users.db')
    cur = conn.cursor()
    cur.execute(f"""INSERT INTO users(id, name, username) 
       VALUES('{id}', '{name}', '{username}');""")
    conn.commit()


def del_user(id):
    conn = sqlite3.connect('files/users.db')
    cur = conn.cursor()
    cur.execute(f"""DELETE FROM users WHERE id = '{id}';""")
    conn.commit()


def all_users_id():
    conn = sqlite3.connect('files/users.db')
    cur = conn.cursor()
    cur.execute("SELECT id FROM users;")
    users = cur.fetchall()
    id_list = []
    for id in users:
        id_list.append(id[0])
    return id_list


def all_users_info():
    conn = sqlite3.connect('files/users.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM users;")
    users_list = cur.fetchall()
    return users_list


def command():
    return


def main():
    pass


if __name__ == '__main__':
    main()
