from wikipediaapi import Wikipedia

import itertools

import psycopg2

import time

from config import host, user, password, db_name

conn = psycopg2.connect(database=db_name,
                        user=user,
                        password=password,
                        host=host
                        )
conn.autocommit = True


def race(start, finish):
    wk = Wikipedia('uk')
    shortcut = [start, ]
    page = wk.page(start)
    link = list(itertools.islice((link for link in page.links), 200))
    for check in link:
        check = check.replace("'", "").replace(" ", "_")
        try:
            with conn.cursor() as cur:
                cur.execute(f"""SELECT link FROM all_link WHERE link = ('{check}')""")
                test = cur.fetchone()
                if test is None:
                    cur.execute(f"""INSERT INTO all_link(link)VALUES ('{check}')""")
                    cur.execute(f"""INSERT INTO parents_link(link) VALUES ()""")
                elif check in test:
                    continue
        except Exception as _ex:
            print("[INFO]", _ex)

    with conn.cursor() as cur:
        cur.execute(f"""SELECT link FROM all_link""")
        parent_link = cur.fetchone()
        for new_check in parent_link:
            new_page = wk.page(new_check)
            new_link = list(itertools.islice((link for link in new_page.links), 200))

    return new_link

star = 'Дружба'
end = 'Арка'

print(race(star, end))

# try:
#     with conn.cursor() as cur:
#         cur.execute(f"""SELECT link FROM all_link WHERE link = ('{check}')""")
#         test = cur.fetchone()
#         if test is None:
#             cur.execute(f"""INSERT INTO all_link(link) VALUES ('{check}')""")
#         elif check in test:
#             continue
# except Exception as _ex:
#     print("[INFO]", _ex)
