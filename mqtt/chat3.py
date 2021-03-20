import time
import curses
import requests
import sys
import re

idx = sys.argv[1]

#/mnt/d/DYSK_KOPIA4/00_sem3/protokoly2/jakub-szczepanski/PROJEKT_PSW/mqtt

gracz1 = ''
gracz2 = ''

stdscr = curses.initscr()
stdscr.clear()
curses.curs_set(0)
curses.start_color()
curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_MAGENTA)

while True:
    try:
        time.sleep(0.4)
        url = f"http://localhost:5000/games/{idx}/mqtt_backup"
        a = requests.get(url)
        for i in range(1, len(a.json())):
            if re.match(r'\[(.*?)\]', a.json()[i]):
                gracz1 = re.match(r'\[(.*?)\]', a.json()[i]).group(0)
                break
        for k in range(i + 1, len(a.json())):
            if re.match(r'\[(.*?)\]', a.json()[k]) and re.match(r'\[(.*?)\]', a.json()[k]) != gracz1:
                gracz2 = re.match(r'\[(.*?)\]', a.json()[k]).group(0)
                break
            else:
                pass
        for l in range(1, len(a.json())):
            if gracz1 in a.json()[l][0:len(gracz1)]:
                curses.curs_set(0)
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(l - 1, 0, a.json()[l])
                stdscr.attroff(curses.color_pair(1))
                stdscr.refresh()
            else:
                curses.curs_set(0)
                stdscr.attron(curses.color_pair(2))
                stdscr.addstr(l - 1, 0, a.json()[l])
                stdscr.attroff(curses.color_pair(2))
                stdscr.refresh()
    except:
        pass

    # print(gracz1, gracz2)

    # for i in range(1, len(a.json())):
    #     print(len(a.json()))
