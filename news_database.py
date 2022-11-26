import sqlite3

# conn = sqlite3.connect('files/news.db')
# cur = conn.cursor()


def create_db():
    conn = sqlite3.connect('files/news.db')
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS news(
       number INT PRIMARY KEY,
       time TEXT,
       bold TEXT,
       slim TEXT,
       link TEXT UNIQUE,
       sent BOOL);
    """)
    conn.commit()


def add_news_db(time, bold, slim, link):
    conn = sqlite3.connect('files/news.db')
    cur = conn.cursor()
    cur.execute("SELECT link FROM news;")
    link_list = cur.fetchall()
    fancy_link_list = []
    for l in link_list:
        fancy_link_list.append(l[0])
    if link not in fancy_link_list:
        cur.execute("SELECT number FROM news;")
        number = len(cur.fetchall()) + 1
        cur.execute(f"""INSERT INTO news(number, time, bold, slim, link, sent)
            VALUES('{number}', '{time}', '{bold}', '{slim}', '{link}', 'False');""")
        conn.commit()
        print(' > Saved')
    else:
        pass


def get_unread_news():
    conn = sqlite3.connect('files/news.db')
    cur = conn.cursor()
    cur.execute("SELECT time, bold, slim, link FROM news WHERE sent = 'False';")
    unread_news = cur.fetchall()
    cur.execute("UPDATE news SET sent = 'True' WHERE sent = 'False';")
    conn.commit()
    return unread_news


def main():
    conn = sqlite3.connect('files/news.db')
    cur = conn.cursor()
    cur.execute("UPDATE news SET sent = 'False' WHERE sent = 'True' and number > 48;")
    conn.commit()
    pass


if __name__ == '__main__':
    main()
