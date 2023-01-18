from typing import List

from wikipediaapi import Wikipedia

# create max len in list
import itertools

import time

import psycopg2
from config import host, user, password, db_name

conn = psycopg2.connect(database=db_name,
                        user=user,
                        password=password,
                        host=host
                        )
conn.autocommit = True

requests_per_minute = 100
links_per_page = 200


class WikiRacer:

    def find_path(self, start: str, finish: str) -> List[str]:

        shortcut = [start, ]
        # Create list of all available link on start page
        wk = Wikipedia('uk')
        page = wk.page(start)
        link = list(itertools.islice((link for link in page.links), 200))
        for check in link:
            check = check.replace("'", "").replace(" ", "_")
            try:
                with conn.cursor() as cur:
                    cur.execute(f"""SELECT link FROM all_link WHERE link = ('{check}')""")
                    test = cur.fetchone()
                    if test is None:
                        cur.execute(f"""INSERT INTO all_link(link) VALUES ('{check}')""")
                    elif check in test:
                        continue
            except Exception as _ex:
                print("[INFO]", _ex)

            # We select links from the first list-link one by one, and look for matches
            new_page = wk.page(check)
            new_link = list(itertools.islice((link for link in new_page.links), 200))
            # when we find matches, we added them to shortcut list
            if finish in new_link:
                shortcut.append(check.replace('_', ' '))
                target = new_link.index(finish)
                shortcut.append(new_link[target])
                break

            else:
                # created a request time limit by using time.sleep
                print('working...')
                # time.sleep(0.6)
                continue

        #   Exit Conditions
        if len(shortcut) == 1:
            return []
        else:
            return shortcut
