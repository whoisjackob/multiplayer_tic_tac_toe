import time
import curses
import requests
import os
import re
import uuid
import keyboard

# import dolacz
# import nowa_gra

credits1 = "autor: Jakub Szczepański"
credits2 = "Program na zaliczenie przedmiotu Protokoły Sieci Web"
legend = "[STRZAŁKI GÓRA DÓŁ] - Nawigacja\n[ENTER] - Zatwierdź"
name = ""
logo = []

stdscr = curses.initscr()


# nowa gra ==================

def stworz_gre(stdscr):
    stdscr.clear()
    curses.curs_set(0)
    h, w = stdscr.getmaxyx()
    stdscr.addstr(h // 2, (w // 2) - len("Podaj swoje imię") // 2, "Podaj swoje imię")
    stdscr.refresh()
    time.sleep(2)
    stdscr.clear()
    curses.endwin()
    czysc()
    imie = input()
    if re.match('^[\dA-za-z]+$', imie):
        stworzenie_req(imie, h, w)
    else:
        time.sleep(2)
        stdscr.clear()
        curses.curs_set(0)
        h, w = stdscr.getmaxyx()
        stdscr.addstr(h // 2, (w // 2) - len("Imie może sie skladac tylko z małych i dużych liter oraz cyfr") // 2,
                      "Imie może sie skladac tylko z małych i dużych liter oraz cyfr")
        stdscr.refresh()
        time.sleep(2)
        curses.wrapper(stworz_gre)


def stworzenie_req(imie, h, w):
    # print("imie to {}".format(imie))
    url = 'http://localhost:5000/games'
    myobj = {"gracz1_name": imie, "gracz1_lifes": 10, "gracz2_name": "", "gracz2_lifes": 10, "gracz1_choice": "",
             "gracz2_choice": "", "nr_chatu_priv": str(uuid.uuid4()), "nr_chatu_pub": str(uuid.uuid4()),
             "ogladajacy": "None", "mqtt_backup": "None"}
    z = requests.post(url, json=myobj)
    gra_id = z.json()["_id"]
    url2 = url + "/" + gra_id
    czysc()
    curses.doupdate()
    while True:
        c = requests.get(url2)
        print(c.json())
        if c.json()["gracz2_name"] != "":
            stdscr.clear()
            stdscr.addstr(h // 2, w // 2 - len("Twoim przeciwnikiem jest {}".format(c.json()["gracz2_name"])) // 2,
                          "Twoim przeciwnikiem jest {}".format(c.json()["gracz2_name"]))
            stdscr.refresh()
            time.sleep(1.5)
            selected_row_idx2 = 0
            # rozgrywka
            gierka1(c, h, w, selected_row_idx2)
        else:
            stdscr.clear()
            stdscr.addstr(h // 2, w // 2 - len("Proszę czekać na drugiego gracza") // 2,
                          "Proszę czekać na drugiego gracza")
            stdscr.refresh()
            time.sleep(0.3)
            stdscr.addstr(h // 2, (w // 2) + (len("Proszę czekać na drugiego gracza") // 2) + 1, ".")
            stdscr.refresh()
            time.sleep(0.3)
            stdscr.addstr(h // 2, (w // 2) + (len("Proszę czekać na drugiego gracza") // 2) + 2, ".")
            stdscr.refresh()
            time.sleep(0.3)
            stdscr.addstr(h // 2, (w // 2) + (len("Proszę czekać na drugiego gracza") // 2) + 3, ".")
            stdscr.refresh()
            time.sleep(0.3)
            time.sleep(1.5)


def gierka1(c, h, w, selected_row_idx2):
    # c to caly request
    stdscr.clear()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_MAGENTA)
    stdscr.refresh()
    stdscr.addstr(0, 0, "Ilość żyć gracza [{}]: {}".format(c.json()["gracz1_name"], c.json()["gracz1_lifes"]))
    stdscr.addstr(0, w - len("Ilość żyć gracza [{}]: {}".format(c.json()["gracz2_name"], c.json()["gracz2_name"])),
                  "Ilość żyć gracza [{}]: {}".format(c.json()["gracz2_name"], c.json()["gracz2_lifes"]))
    stdscr.addstr(0, (w // 2) - (len("Twój prywatny klucz chatu to:") // 2), "Twój prywatny klucz chatu to:")
    stdscr.addstr(1, (w // 2) - (len(c.json()["nr_chatu_priv"]) // 2), c.json()["nr_chatu_priv"])
    stdscr.addstr(2, (w // 2) - (len("Aby włączyć chat wciśnij F1") // 2), "Aby włączyć chat wciśnij F1")
    #lista ogladajacych
    stdscr.addstr(4, 0, "Oglądający: ")
    for i in range(1, len(c.json()["ogladajacy"])):
        stdscr.attron(curses.color_pair(4))
        stdscr.addstr(5 + i, 0, c.json()["ogladajacy"][i])
        stdscr.attroff(curses.color_pair(4))
    menu3 = ["PAPIER", "KAMIEN", "NOZYCE"]
    for idx2, row in enumerate(menu3):
        x = w // 2 - len(row) // 2
        y = h // 2 - len(menu3) // 2 + idx2
        if idx2 == selected_row_idx2:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)
    stdscr.refresh()
    while True:
        key = stdscr.getch()
        if key == curses.KEY_UP and selected_row_idx2 > 0:
            selected_row_idx2 -= 1
            gierka1(c, h, w, selected_row_idx2)
        # wejscie do chatu1
        elif key == curses.KEY_F1:
            os.system(
                f"cmd.exe /c start cmd.exe /c wsl.exe python3 mqtt/chat1.py {c.json()['gracz2_name']} {c.json()['nr_chatu_priv']}")
            gierka1(c, h, w, selected_row_idx2)
        elif key == curses.KEY_DOWN and selected_row_idx2 < len(menu3) - 1:
            selected_row_idx2 += 1
            gierka1(c, h, w, selected_row_idx2)
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if selected_row_idx2 == 0:
                url3 = "http://localhost:5000/games/" + c.json()["_id"]
                patch = {"gracz1_choice": menu3[0]}
                requests.patch(url3, json=patch)
                oczekiwanie1(c.json()["_id"])
            elif selected_row_idx2 == 1:
                url3 = "http://localhost:5000/games/" + c.json()["_id"]
                patch = {"gracz1_choice": menu3[1]}
                requests.patch(url3, json=patch)
                oczekiwanie1(c.json()["_id"])
            else:
                url3 = "http://localhost:5000/games/" + c.json()["_id"]
                patch = {"gracz1_choice": menu3[2]}
                requests.patch(url3, json=patch)
                oczekiwanie1(c.json()["_id"])


def oczekiwanie1(id):
    h, w = stdscr.getmaxyx()
    stdscr.addstr(h - 3, (w // 2) - (len("Czekaj na ruch drugiego gracza...") // 2),
                  "Czekaj na ruch drugiego gracza...")
    stdscr.refresh()
    while True:
        url4 = "http://localhost:5000/games/" + id
        o = requests.get(url4)
        drugi = o.json()["gracz2_choice"]
        if drugi != "":
            break
        else:
            time.sleep(1)
    wybor1 = o.json()["gracz1_choice"]
    wybor2 = o.json()["gracz2_choice"]
    gracz1 = o.json()["gracz1_name"]
    gracz2 = o.json()["gracz2_name"]
    stan_zycia1 = o.json()["gracz1_lifes"]
    stan_zycia2 = o.json()["gracz2_lifes"]
    if wybor1 == "PAPIER" and wybor2 == "KAMIEN":
        url4 = "http://localhost:5000/games/" + id
        stan_zycia2 -= 1
        patch = {"gracz2_lifes": stan_zycia2}
        requests.patch(url4, json=patch)
        stdscr.addstr(h - 2, (w // 2) - (
                len("{} wybrał [{}], {} wybrał [{}], {} traci 1 życie.".format(gracz1, wybor1, gracz2, wybor2,
                                                                               gracz2)) // 2),
                      "{} wybrał [{}], {} wybrał [{}], {} traci 1 życie.".format(gracz1, wybor1, gracz2, wybor2,
                                                                                 gracz2))
        stdscr.refresh()
        patch2 = {"gracz1_choice": "", "gracz2_choice": ""}
        requests.patch(url4, json=patch2)
        time.sleep(3)
        h, w = stdscr.getmaxyx()
        p = requests.get("http://localhost:5000/games/" + id)
        stan_zycia1 = p.json()["gracz1_lifes"]
        stan_zycia2 = p.json()["gracz2_lifes"]
        if stan_zycia1 == 0:
            stdscr.clear()
            napis_koncowy = "Zwyciężył {}, gra zakończona".format(gracz2)
            stdscr.addstr(h // 2, (w // 2) - (len(napis_koncowy) // 2), napis_koncowy)
            stdscr.refresh()
            requests.delete(url4)
            time.sleep(3)
            # powrot do menu
            main(stdscr)
        if stan_zycia2 == 0:
            stdscr.clear()
            napis_koncowy = "Zwyciężył {}, gra zakończona".format(gracz1)
            stdscr.addstr(h // 2, (w // 2) - (len(napis_koncowy) // 2), napis_koncowy)
            stdscr.refresh()
            requests.delete(url4)
            time.sleep(2)
            # powrot do menu
            main(stdscr)
        selected_row_idx2 = 0
        gierka1(p, h, w, selected_row_idx2)
    elif wybor1 == "KAMIEN" and wybor2 == "PAPIER":
        url4 = "http://localhost:5000/games/" + id
        stan_zycia1 -= 1
        patch = {"gracz1_lifes": stan_zycia1}
        requests.patch(url4, json=patch)
        stdscr.addstr(h - 2, (w // 2) - (
                len("{} wybrał [{}], {} wybrał [{}], {} traci 1 życie.".format(gracz1, wybor1, gracz2, wybor2,
                                                                               gracz1)) // 2),
                      "{} wybrał [{}], {} wybrał [{}], {} traci 1 życie.".format(gracz1, wybor1, gracz2, wybor2,
                                                                                 gracz1))
        stdscr.refresh()
        patch2 = {"gracz1_choice": "", "gracz2_choice": ""}
        requests.patch(url4, json=patch2)
        time.sleep(3)
        h, w = stdscr.getmaxyx()
        p = requests.get("http://localhost:5000/games/" + id)
        stan_zycia1 = p.json()["gracz1_lifes"]
        stan_zycia2 = p.json()["gracz2_lifes"]
        if stan_zycia1 == 0:
            stdscr.clear()
            napis_koncowy = "Zwyciężył {}, gra zakończona".format(gracz2)
            stdscr.addstr(h // 2, (w // 2) - (len(napis_koncowy) // 2), napis_koncowy)
            stdscr.refresh()
            requests.delete(url4)
            time.sleep(3)
            # powrot do menu
            main(stdscr)
        if stan_zycia2 == 0:
            stdscr.clear()
            napis_koncowy = "Zwyciężył {}, gra zakończona".format(gracz1)
            stdscr.addstr(h // 2, (w // 2) - (len(napis_koncowy) // 2), napis_koncowy)
            stdscr.refresh()
            requests.delete(url4)
            time.sleep(3)
            # powrot do menu
            main(stdscr)
        selected_row_idx2 = 0
        gierka1(p, h, w, selected_row_idx2)
    elif wybor1 == "PAPIER" and wybor2 == "NOZYCE":
        url4 = "http://localhost:5000/games/" + id
        stan_zycia1 -= 1
        patch = {"gracz1_lifes": stan_zycia1}
        requests.patch(url4, json=patch)
        stdscr.addstr(h - 2, (w // 2) - (
                len("{} wybrał [{}], {} wybrał [{}], {} traci 1 życie.".format(gracz1, wybor1, gracz2, wybor2,
                                                                               gracz1)) // 2),
                      "{} wybrał [{}], {} wybrał [{}], {} traci 1 życie.".format(gracz1, wybor1, gracz2, wybor2,
                                                                                 gracz1))
        stdscr.refresh()
        patch2 = {"gracz1_choice": "", "gracz2_choice": ""}
        requests.patch(url4, json=patch2)
        time.sleep(3)
        h, w = stdscr.getmaxyx()
        p = requests.get("http://localhost:5000/games/" + id)
        stan_zycia1 = p.json()["gracz1_lifes"]
        stan_zycia2 = p.json()["gracz2_lifes"]
        if stan_zycia1 == 0:
            stdscr.clear()
            napis_koncowy = "Zwyciężył {}, gra zakończona".format(gracz2)
            stdscr.addstr(h // 2, (w // 2) - (len(napis_koncowy) // 2), napis_koncowy)
            stdscr.refresh()
            requests.delete(url4)
            time.sleep(3)
            # powrot do menu
        if stan_zycia2 == 0:
            stdscr.clear()
            napis_koncowy = "Zwyciężył {}, gra zakończona".format(gracz1)
            stdscr.addstr(h // 2, (w // 2) - (len(napis_koncowy) // 2), napis_koncowy)
            stdscr.refresh()
            requests.delete(url4)
            time.sleep(3)
            # powrot do menu
            main(stdscr)
        selected_row_idx2 = 0
        gierka1(p, h, w, selected_row_idx2)
    elif wybor1 == "NOZYCE" and wybor2 == "PAPIER":
        url4 = "http://localhost:5000/games/" + id
        stan_zycia2 -= 1
        patch = {"gracz2_lifes": stan_zycia2}
        requests.patch(url4, json=patch)
        stdscr.addstr(h - 2, (w // 2) - (
                len("{} wybrał [{}], {} wybrał [{}], {} traci 1 życie.".format(gracz1, wybor1, gracz2, wybor2,
                                                                               gracz2)) // 2),
                      "{} wybrał [{}], {} wybrał [{}], {} traci 1 życie.".format(gracz1, wybor1, gracz2, wybor2,
                                                                                 gracz2))
        stdscr.refresh()
        patch2 = {"gracz1_choice": "", "gracz2_choice": ""}
        requests.patch(url4, json=patch2)
        time.sleep(3)
        h, w = stdscr.getmaxyx()
        p = requests.get("http://localhost:5000/games/" + id)
        stan_zycia1 = p.json()["gracz1_lifes"]
        stan_zycia2 = p.json()["gracz2_lifes"]
        if stan_zycia1 == 0:
            stdscr.clear()
            napis_koncowy = "Zwyciężył {}, gra zakończona".format(gracz2)
            stdscr.addstr(h // 2, (w // 2) - (len(napis_koncowy) // 2), napis_koncowy)
            stdscr.refresh()
            requests.delete(url4)
            time.sleep(3)
            # powrot do menu
            main(stdscr)
        if stan_zycia2 == 0:
            stdscr.clear()
            napis_koncowy = "Zwyciężył {}, gra zakończona".format(gracz1)
            stdscr.addstr(h // 2, (w // 2) - (len(napis_koncowy) // 2), napis_koncowy)
            stdscr.refresh()
            requests.delete(url4)
            time.sleep(3)
            # powrot do menu
            main(stdscr)
        selected_row_idx2 = 0
        gierka1(p, h, w, selected_row_idx2)
    elif wybor1 == "KAMIEN" and wybor2 == "NOZYCE":
        url4 = "http://localhost:5000/games/" + id
        stan_zycia2 -= 1
        patch = {"gracz2_lifes": stan_zycia2}
        requests.patch(url4, json=patch)
        stdscr.addstr(h - 2, (w // 2) - (
                len("{} wybrał [{}], {} wybrał [{}], {} traci 1 życie.".format(gracz1, wybor1, gracz2, wybor2,
                                                                               gracz2)) // 2),
                      "{} wybrał [{}], {} wybrał [{}], {} traci 1 życie.".format(gracz1, wybor1, gracz2, wybor2,
                                                                                 gracz2))
        stdscr.refresh()
        patch2 = {"gracz1_choice": "", "gracz2_choice": ""}
        requests.patch(url4, json=patch2)
        time.sleep(3)
        h, w = stdscr.getmaxyx()
        p = requests.get("http://localhost:5000/games/" + id)
        stan_zycia1 = p.json()["gracz1_lifes"]
        stan_zycia2 = p.json()["gracz2_lifes"]
        if stan_zycia1 == 0:
            stdscr.clear()
            napis_koncowy = "Zwyciężył {}, gra zakończona".format(gracz2)
            stdscr.addstr(h // 2, (w // 2) - (len(napis_koncowy) // 2), napis_koncowy)
            stdscr.refresh()
            requests.delete(url4)
            time.sleep(3)
            # powrot do menu
            main(stdscr)
        if stan_zycia2 == 0:
            stdscr.clear()
            napis_koncowy = "Zwyciężył {}, gra zakończona".format(gracz1)
            stdscr.addstr(h // 2, (w // 2) - (len(napis_koncowy) // 2), napis_koncowy)
            stdscr.refresh()
            requests.delete(url4)
            time.sleep(3)
            # powrot do menu
            main(stdscr)
        selected_row_idx2 = 0
        gierka1(p, h, w, selected_row_idx2)
    elif wybor1 == "NOZYCE" and wybor2 == "KAMIEN":
        url4 = "http://localhost:5000/games/" + id
        stan_zycia1 -= 1
        patch = {"gracz1_lifes": stan_zycia1}
        requests.patch(url4, json=patch)
        stdscr.addstr(h - 2, (w // 2) - (
                len("{} wybrał [{}], {} wybrał [{}], {} traci 1 życie.".format(gracz1, wybor1, gracz2, wybor2,
                                                                               gracz1)) // 2),
                      "{} wybrał [{}], {} wybrał [{}], {} traci 1 życie.".format(gracz1, wybor1, gracz2, wybor2,
                                                                                 gracz1))
        stdscr.refresh()
        patch2 = {"gracz1_choice": "", "gracz2_choice": ""}
        requests.patch(url4, json=patch2)
        time.sleep(3)
        h, w = stdscr.getmaxyx()
        p = requests.get("http://localhost:5000/games/" + id)
        stan_zycia1 = p.json()["gracz1_lifes"]
        stan_zycia2 = p.json()["gracz2_lifes"]
        if stan_zycia1 == 0:
            stdscr.clear()
            napis_koncowy = "Zwyciężył {}, gra zakończona".format(gracz2)
            stdscr.addstr(h // 2, (w // 2) - (len(napis_koncowy) // 2), napis_koncowy)
            stdscr.refresh()
            requests.delete(url4)
            time.sleep(3)
            # powrot do menu
            main(stdscr)
        if stan_zycia2 == 0:
            stdscr.clear()
            napis_koncowy = "Zwyciężył {}, gra zakończona".format(gracz1)
            stdscr.addstr(h // 2, (w // 2) - (len(napis_koncowy) // 2), napis_koncowy)
            stdscr.refresh()
            requests.delete(url4)
            time.sleep(3)
            # powrot do menu
            main(stdscr)
        selected_row_idx2 = 0
        gierka1(p, h, w, selected_row_idx2)
    else:
        stdscr.addstr(h - 2, (w // 2) - (
                len("{} wybrał [{}], {} wybrał [{}], mamy remis.".format(gracz1, wybor1, gracz2, wybor2,
                                                                         )) // 2),
                      "{} wybrał [{}], {} wybrał [{}], mamy remis.".format(gracz1, wybor1, gracz2, wybor2,
                                                                           ))
        patch2 = {"gracz1_choice": "", "gracz2_choice": ""}
        requests.patch(url4, json=patch2)
        stdscr.refresh()
        patch2 = {"gracz1_choice": "", "gracz2_choice": ""}
        requests.patch(url4, json=patch2)
        time.sleep(3)
        p = requests.get("http://localhost:5000/games/" + id)
        h, w = stdscr.getmaxyx()
        selected_row_idx2 = 0
        gierka1(p, h, w, selected_row_idx2)


# =================


# gracz 2 =============================

def req_patch2(id, imie2):
    url = "http://localhost:5000/games/" + id
    patch = {"gracz2_name": imie2}
    requests.patch(url, json=patch)


def print_pole2(a, selected_row_idx2):
    h, w = stdscr.getmaxyx()
    stdscr.clear()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_MAGENTA)
    stdscr.refresh()
    stdscr.addstr(0, 0, "Ilość żyć gracza [{}]: {}".format(a.json()["gracz1_name"], a.json()["gracz1_lifes"]))
    stdscr.addstr(0,
                  w - len("Ilość żyć gracza [{}]: {}".format(a.json()["gracz2_name"], a.json()["gracz2_lifes"])),
                  "Ilość żyć gracza [{}]: {}".format(a.json()["gracz2_name"], a.json()["gracz2_lifes"]))
    stdscr.addstr(0, (w // 2) - (len("Twój prywatny klucz chatu to:") // 2), "Twój prywatny klucz chatu to:")
    stdscr.addstr(1, (w // 2) - (len(a.json()["nr_chatu_priv"]) // 2), a.json()["nr_chatu_priv"])
    stdscr.addstr(2, (w // 2) - (len("Aby włączyć chat wciśnij F1") // 2), "Aby włączyć chat wciśnij F1")
    #ogladajacy2
    stdscr.addstr(4, 0, "Oglądający: ")
    for i in range(1, len(a.json()["ogladajacy"])):
        stdscr.attron(curses.color_pair(4))
        stdscr.addstr(5 + i, 0, a.json()["ogladajacy"][i])
        stdscr.attroff(curses.color_pair(4))
    menu3 = ["PAPIER", "KAMIEN", "NOZYCE"]
    for idx2, row in enumerate(menu3):
        x = w // 2 - len(row) // 2
        y = h // 2 - len(menu3) // 2 + idx2
        if idx2 == selected_row_idx2:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)
    return selected_row_idx2


def print_gra2(id, selected_row_idx2):
    czysc()
    curses.doupdate()
    stdscr.clear()
    menu3 = ["PAPIER", "KAMIEN", "NOZYCE"]
    while True:
        url = "http://localhost:5000/games/" + id
        a = requests.get(url)
        h, w = stdscr.getmaxyx()
        if a.json()["gracz1_choice"] != "":
            print_pole2(a, 0)
            while True:
                key = stdscr.getch()
                if key == curses.KEY_UP and selected_row_idx2 > 0:
                    selected_row_idx2 -= 1
                    print_pole2(a, selected_row_idx2)
                elif key == curses.KEY_DOWN and selected_row_idx2 < len(menu3) - 1:
                    selected_row_idx2 += 1
                    print_pole2(a, selected_row_idx2)
                # dolaczenie do chatu2
                elif key == curses.KEY_F1:
                    os.system(
                        f"cmd.exe /c start cmd.exe /c wsl.exe python3 mqtt/chat2.py {a.json()['gracz1_name']} {a.json()['nr_chatu_priv']}")
                    print_pole2(a, selected_row_idx2)
                elif key == curses.KEY_ENTER or key in [10, 13]:
                    if selected_row_idx2 == 0:
                        url3 = "http://localhost:5000/games/" + a.json()["_id"]
                        patch = {"gracz2_choice": menu3[0]}
                        requests.patch(url3, json=patch)
                        stdscr.addstr(h - 2, (w // 2) - (len(
                            "{} wybrał [{}], {} wybrał [{}]".format(a.json()["gracz1_name"], a.json()["gracz1_choice"],
                                                                    a.json()["gracz2_name"],
                                                                    a.json()["gracz2_choice"])) // 2),
                                      "{} wybrał [{}], {} wybrał [{}].".format(a.json()["gracz1_name"],
                                                                               a.json()["gracz1_choice"],
                                                                               a.json()["gracz2_name"],
                                                                               "PAPIER"))
                        stdscr.refresh()
                        time.sleep(2)
                        print_pole2(a, 0)
                        gracz1 = a.json()["gracz1_name"]
                        stdscr.addstr(h - 2, (w // 2) - (len("Czekaj aż {} wykona swój ruch.".format(gracz1)) // 2),
                                      "Czekaj aż {} wykona swój ruch.".format(gracz1))
                        stdscr.refresh()
                        x = requests.get(url3)
                        g1 = x.json()["gracz1_lifes"]
                        g2 = x.json()["gracz2_lifes"]
                        if g1 == 0 or g2 == 0:
                            stdscr.clear()
                            stdscr.addstr(h // 2, (w // 2) - (len("Gra Zakończona") // 2), "Gra Zakończona")
                            stdscr.refresh()
                            time.sleep(2)
                            main(stdscr)
                        else:
                            curses.doupdate()
                            print_gra2(id, selected_row_idx2)

                    elif selected_row_idx2 == 1:
                        url3 = "http://localhost:5000/games/" + a.json()["_id"]
                        patch = {"gracz2_choice": menu3[1]}
                        requests.patch(url3, json=patch)
                        stdscr.addstr(h - 2, (w // 2) - (len(
                            "{} wybrał [{}], {} wybrał [{}]".format(a.json()["gracz1_name"], a.json()["gracz1_choice"],
                                                                    a.json()["gracz2_name"],
                                                                    a.json()["gracz2_choice"])) // 2),
                                      "{} wybrał [{}], {} wybrał [{}].".format(a.json()["gracz1_name"],
                                                                               a.json()["gracz1_choice"],
                                                                               a.json()["gracz2_name"],
                                                                               "KAMIEN"))
                        stdscr.refresh()
                        time.sleep(2)
                        print_pole2(a, 0)
                        gracz1 = a.json()["gracz1_name"]
                        stdscr.addstr(h - 2, (w // 2) - (len("Czekaj aż {} wykona swój ruch.".format(gracz1)) // 2),
                                      "Czekaj aż {} wykona swój ruch.".format(gracz1))
                        stdscr.refresh()
                        x = requests.get(url3)
                        g1 = x.json()["gracz1_lifes"]
                        g2 = x.json()["gracz2_lifes"]
                        if g1 == 0 or g2 == 0:
                            stdscr.clear()
                            stdscr.addstr(h // 2, (w // 2) - (len("Gra Zakończona") // 2), "Gra Zakończona")
                            stdscr.refresh()
                            time.sleep(2)
                            main(stdscr)
                        else:
                            curses.doupdate()
                            print_gra2(id, selected_row_idx2)
                    else:
                        url3 = "http://localhost:5000/games/" + a.json()["_id"]
                        patch = {"gracz2_choice": menu3[2]}
                        requests.patch(url3, json=patch)
                        stdscr.addstr(h - 2, (w // 2) - (len(
                            "{} wybrał [{}], {} wybrał [{}]".format(a.json()["gracz1_name"], a.json()["gracz1_choice"],
                                                                    a.json()["gracz2_name"],
                                                                    a.json()["gracz2_choice"])) // 2),
                                      "{} wybrał [{}], {} wybrał [{}].".format(a.json()["gracz1_name"],
                                                                               a.json()["gracz1_choice"],
                                                                               a.json()["gracz2_name"],
                                                                               "NOZYCE"))
                        stdscr.refresh()
                        time.sleep(2)
                        print_pole2(a, 0)
                        gracz1 = a.json()["gracz1_name"]
                        stdscr.addstr(h - 2, (w // 2) - (len("Czekaj aż {} wykona swój ruch.".format(gracz1)) // 2),
                                      "Czekaj aż {} wykona swój ruch.".format(gracz1))
                        stdscr.refresh()
                        x = requests.get(url3)
                        g1 = x.json()["gracz1_lifes"]
                        g2 = x.json()["gracz2_lifes"]
                        if g1 == 0 or g2 == 0:
                            stdscr.clear()
                            stdscr.addstr(h // 2, (w // 2) - (len("Gra Zakończona") // 2), "Gra Zakończona")
                            stdscr.refresh()
                            time.sleep(2)
                            main(stdscr)
                        else:
                            curses.doupdate()
                            print_gra2(id, selected_row_idx2)
                else:
                    pass

        else:
            # a to caly request
            print_pole2(a, 0)
            gracz1 = a.json()["gracz1_name"]
            stdscr.addstr(h - 2, (w // 2) - (len("Czekaj aż {} wykona swój ruch.".format(gracz1)) // 2),
                          "Czekaj aż {} wykona swój ruch.".format(gracz1))
            stdscr.refresh()
            time.sleep(1)


def dolacz(stdscr, id):
    stdscr.clear()
    curses.curs_set(0)
    h, w = stdscr.getmaxyx()
    stdscr.addstr(h // 2, (w // 2) - len("Podaj swoje imię") // 2, "Podaj swoje imię")
    stdscr.refresh()
    time.sleep(2)
    stdscr.clear()
    curses.endwin()
    czysc()
    imie2 = input()
    czysc()
    time.sleep(0.5)
    if re.match('^[\dA-za-z]+$', imie2):
        req_patch2(id, imie2)
        czysc()
        print("test")

        selected_row_idx2 = 0
        # curses.doupdate()
        # stdscr.clear()
        # stdscr.refresh()
        print_gra2(id, selected_row_idx2)
        # print_gra2(id, selected_row_idx2)
    else:
        time.sleep(2)
        curses.doupdate()
        stdscr.clear()
        stdscr.refresh()
        curses.curs_set(0)
        h, w = stdscr.getmaxyx()
        stdscr.addstr(h // 2, (w // 2) - len("Imie może sie skladac tylko z małych i dużych liter oraz cyfr") // 2,
                      "Imie może sie skladac tylko z małych i dużych liter oraz cyfr")
        stdscr.refresh()
        time.sleep(2)
        dolacz(stdscr, id)
        # dolacz(stdscr, id)


# =============================

# stdscr = curses.initscr()

def czysc():
    os.system('cls' if os.name == 'nt' else 'clear')


def logop():
    with open('ascii_art.txt', 'r') as f:
        for line in f:
            logo.append(line.rstrip())
    return logo


def main(stdscr):
    menu = ['GRAJ', 'OGLĄDAJ', 'WYJŚCIE']
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    current_row_idx = 0
    print_menu(stdscr, current_row_idx, legend, credits1, credits2)
    while True:
        key = stdscr.getch()
        stdscr.clear()
        if key == curses.KEY_UP and current_row_idx > 0:
            current_row_idx -= 1
        elif key == curses.KEY_DOWN and current_row_idx < len(menu) - 1:
            current_row_idx += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            stdscr.clear()
            if current_row_idx == 1:
                stdscr.clear()
                curses.wrapper(main_ogladaj)
            elif current_row_idx == 0:
                stdscr.clear()
                curses.wrapper(main_graj)
            elif current_row_idx == 2:
                czysc()
                exit()
            else:
                stdscr.addstr(0, 0, "Wybrałeś {}".format(menu[current_row_idx]))

            stdscr.refresh()
            stdscr.getch()

        print_menu(stdscr, current_row_idx, legend, credits1, credits2)
        stdscr.refresh()


def print_menu(stdscr, selected_row_idx, legend, credits1, credits2):
    menu = ['GRAJ', 'OGLĄDAJ', 'WYJŚCIE']
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    for i in range(len(logo)):
        x2 = (w // 2) - 17
        stdscr.attron(curses.color_pair(4))
        stdscr.addstr(i + 5, x2, logo[i])
        stdscr.attroff(curses.color_pair(4))
    stdscr.refresh()
    for idx, row in enumerate(menu):
        x = w // 2 - len(row) // 2
        y = h // 2 - len(menu) // 2 + idx
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
            stdscr.insstr(0, 0, legend)
            stdscr.insstr(0, w - len(credits1), credits1)
            stdscr.insstr(1, w - len(credits2), credits2)
        else:
            stdscr.addstr(y, x, row)
    stdscr.refresh()


def main_ogladaj(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_RED)
    current_row_idx = 0
    print_pokoje(stdscr, current_row_idx, legend, credits1, credits2)
    menu = print_pokoje(stdscr, current_row_idx, legend, credits1, credits2)
    while True:
        key = stdscr.getch()
        stdscr.clear()
        if key == curses.KEY_UP and current_row_idx > 0:
            current_row_idx -= 1
        elif key == curses.KEY_DOWN and current_row_idx < len(menu) - 1:
            current_row_idx += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if current_row_idx == (len(menu) - 1):
                stdscr.clear()
                curses.wrapper(main)
            else:
                # ogladanie gry
                ogladanie_gry(stdscr, current_row_idx)
                pass

        print_pokoje(stdscr, current_row_idx, legend, credits1, credits2)
        stdscr.refresh()


def print_pokoje(stdscr, selected_row_idx, legend, credits1, credits2):
    x = requests.get('http://localhost:5000/games')
    menu = []
    for i in range(len(x.json())):
        if x.json()[i]["gracz1_name"] == "" or x.json()[i]["gracz2_name"] == "":
            pass
        else:
            menu.append("POKÓJ {} ".format(i) + "[{}]".format(x.json()[i]["gracz1_name"]) + " [{}]".format(
                x.json()[i]["gracz2_name"]))

    stdscr.clear()
    h, w = stdscr.getmaxyx()
    menu.append("WRÓĆ")
    for i in range(len(logo)):
        x2 = (w // 2) - 17
        stdscr.attron(curses.color_pair(4))
        stdscr.addstr(i + 5, x2, logo[i])
        stdscr.attroff(curses.color_pair(4))
    stdscr.refresh()
    for idx, row in enumerate(menu):
        x = w // 2 - len(row) // 2
        y = h // 2 - len(menu) // 2 + idx
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
            stdscr.insstr(0, 0, legend)
            stdscr.insstr(0, w - len(credits1), credits1)
            stdscr.insstr(1, w - len(credits2), credits2)
        else:
            stdscr.addstr(y, x, row)
    stdscr.refresh()

    return menu


def main_graj(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_RED)
    current_row_idx = 0
    print_pokoje_dogry(stdscr, current_row_idx, legend, credits1, credits2)
    menu = print_pokoje_dogry(stdscr, current_row_idx, legend, credits1, credits2)
    while True:
        key = stdscr.getch()
        stdscr.clear()
        if key == curses.KEY_UP and current_row_idx > 0:
            current_row_idx -= 1
        elif key == curses.KEY_DOWN and current_row_idx < len(menu) - 1:
            current_row_idx += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            x = requests.get('http://localhost:5000/games')
            if current_row_idx == (len(menu) - 1):
                stdscr.clear()
                curses.wrapper(main)
            elif current_row_idx == 0:
                # stworzenie gry
                stworz_gre(stdscr)
                pass
            elif x.json()[current_row_idx - 1]["gracz1_name"] != "" and x.json()[current_row_idx - 1][
                "gracz2_name"] != "":
                print_pokoje_dogry(stdscr, current_row_idx, legend, credits1, credits2)
                h, w = stdscr.getmaxyx()
                stdscr.insstr(h - 2, (w // 2) - 12, "Ten pokój jest już zajęty")
                stdscr.refresh()
                time.sleep(1)
            else:
                dolacz(stdscr, x.json()[current_row_idx - 1]["_id"])
                # if na sprawdzenie czy ktos sie nie wepchnal do pokoju
                # nowe_id = x.json()[current_row_idx - 1]["_id"]
                # url6 = "http://localhost/games/" + nowe_id
                # check = requests.get(url6)
                # wepchniety = check.json()[nowe_id]["gracz2_name"]
                # if wepchniety != "":
                #     # dolaczanie do gry
                #     dolacz.dolacz(nowe_id)
                # else:
                #     h, w = stdscr.getmaxyx()
                #     stdscr.addstr(h - 2, (w // 2) - len("Ktoś cię wyprzedził!") // 2, "Ktoś cię wyprzedził!")
                #     stdscr.refresh()
                #     time.sleep(2)
                #     main_graj(stdscr)

        print_pokoje_dogry(stdscr, current_row_idx, legend, credits1, credits2)
        stdscr.refresh()


def print_pokoje_dogry(stdscr, selected_row_idx, legend, credits1, credits2):
    x = requests.get('http://localhost:5000/games')
    menu = ["NOWA GRA"]
    for i in range(len(x.json())):
        menu.append("POKÓJ {} ".format(i) + "[{}]".format(x.json()[i]["gracz1_name"]) + " [{}]".format(
            x.json()[i]["gracz2_name"]))
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    menu.append("WRÓĆ")
    for i in range(len(logo)):
        x2 = (w // 2) - 17
        stdscr.attron(curses.color_pair(4))
        stdscr.addstr(i + 5, x2, logo[i])
        stdscr.attroff(curses.color_pair(4))
    stdscr.refresh()
    for idx, row in enumerate(menu):
        x = w // 2 - len(row) // 2
        y = h // 2 - len(menu) // 2 + idx
        if idx == selected_row_idx:
            if re.match("POKÓJ [\d]* \[[\w]*\] \[\]", menu[selected_row_idx]):
                stdscr.attron(curses.color_pair(2))
                stdscr.addstr(y, x, row)
                stdscr.attroff(curses.color_pair(2))
                stdscr.insstr(0, 0, legend)
                stdscr.insstr(0, w - len(credits1), credits1)
                stdscr.insstr(1, w - len(credits2), credits2)
            elif selected_row_idx == 0 or selected_row_idx == (len(menu) - 1):
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, row)
                stdscr.attroff(curses.color_pair(1))
                stdscr.insstr(0, 0, legend)
                stdscr.insstr(0, w - len(credits1), credits1)
                stdscr.insstr(1, w - len(credits2), credits2)
            else:
                stdscr.attron(curses.color_pair(3))
                stdscr.addstr(y, x, row)
                stdscr.attroff(curses.color_pair(3))
                stdscr.insstr(0, 0, legend)
                stdscr.insstr(0, w - len(credits1), credits1)
                stdscr.insstr(1, w - len(credits2), credits2)
                # x = requests.get('http://localhost:5000/games')
                # name1 = str(x.json()[selected_row_idx - 1]["gracz1_name"])
                # name2 = str(x.json()[selected_row_idx - 1]["gracz2_name"])
                # if name1 != "" or name2 != "":
                #     stdscr.attron(curses.color_pair(2))
                #     stdscr.addstr(y, x, row)
                #     stdscr.attroff(curses.color_pair(2))
                #     stdscr.insstr(0, 0, legend)
                #     stdscr.insstr(0, w - len(credits1), credits1)
                #     stdscr.insstr(1, w - len(credits2), credits2)
                # else:
                #     stdscr.attron(curses.color_pair(3))
                #     stdscr.addstr(y, x, row)
                #     stdscr.attroff(curses.color_pair(3))
                #     stdscr.insstr(0, 0, legend)
                #     stdscr.insstr(0, w - len(credits1), credits1)
                #     stdscr.insstr(1, w - len(credits2), credits2)
        else:
            stdscr.addstr(y, x, row)
    stdscr.refresh()

    return menu


# OGLADANIE =========================
def ogladanie_gry(stdscr, current_row_idx):
    #podanie imienia
    stdscr.clear()
    curses.curs_set(0)
    h, w = stdscr.getmaxyx()
    stdscr.addstr(h // 2, (w // 2) - len("Podaj swoje imię") // 2, "Podaj swoje imię")
    stdscr.refresh()
    time.sleep(2)
    stdscr.clear()
    curses.endwin()
    czysc()
    imie3 = input()
    czysc()
    time.sleep(0.5)
    if re.match('^[\dA-za-z]+$', imie3):
        #patch na ogladajacych
        url3 = f"http://localhost:5000/games/{current_row_idx}/ogladajacy"
        patch = {"nowy": imie3}
        time.sleep(0.3)
        requests.patch(url3, json=patch)
        os.system(
            f"cmd.exe /c start cmd.exe /c wsl.exe python3 mqtt/chat3.py {current_row_idx}")
        time.sleep(0.3)
        while True:
            # #wyjscie z ogladania
            # if keyboard.is_pressed('end'):
            #     stdscr.clear()
            #     curses.wrapper(main_ogladaj)
            # else:
            time.sleep(0.5)
            curses.curs_set(0)
            curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
            h, w = stdscr.getmaxyx()
            url = "http://localhost:5000/games/"
            a = requests.get(url)
            gracz1 = a.json()[current_row_idx]["gracz1_name"]
            gracz2 = a.json()[current_row_idx]["gracz2_name"]
            gracz1_lifes = a.json()[current_row_idx]["gracz1_lifes"]
            gracz2_lifes = a.json()[current_row_idx]["gracz2_lifes"]
            klucz_pub = a.json()[current_row_idx]["nr_chatu_priv"]
            wybor1 = a.json()[current_row_idx]["gracz1_choice"]
            wybor2 = a.json()[current_row_idx]["gracz2_choice"]
            stdscr.clear()
            stdscr.addstr(0, 0, "Ilość żyć gracza [{}]: {}".format(gracz1, gracz1_lifes))
            stdscr.addstr(0, w - len("Ilość żyć gracza [{}]: {}".format(gracz2, gracz2_lifes)),
                          "Ilość żyć gracza [{}]: {}".format(gracz2, gracz2_lifes))
            stdscr.addstr(0, (w // 2) - (len("Twój publiczny klucz chatu to:") // 2), "Twój publiczny klucz chatu to:")
            stdscr.addstr(1, (w // 2) - (len(klucz_pub) // 2), klucz_pub)
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(h // 2, (w // 4), wybor1)
            stdscr.addstr(h // 2, ((w // 4) * 3), wybor2)
            stdscr.attroff(curses.color_pair(1))
            stdscr.refresh()
            if wybor1 != "" and wybor2 != "":
                stdscr.addstr(h - 2, (w // 2) - (len("{} wybrał [{}], zaś {} wybrał [{}]") // 2),
                              "{} wybrał [{}], zaś {} wybrał [{}]".format(gracz1, wybor1, gracz2, wybor2))
                stdscr.refresh()
                time.sleep(2)
            elif gracz2_lifes == 0 or gracz1_lifes == 0:
                stdscr.clear()
                stdscr.addstr(h // 2, (w // 2) - len("Koniec gry"), "Koniec gry")
                stdscr.refresh()
                time.sleep(2)
                main(stdscr)
            else:
                pass
    else:
        time.sleep(2)
        curses.doupdate()
        stdscr.clear()
        stdscr.refresh()
        curses.curs_set(0)
        h, w = stdscr.getmaxyx()
        stdscr.addstr(h // 2, (w // 2) - len("Imie może sie skladac tylko z małych i dużych liter oraz cyfr") // 2,
                      "Imie może sie skladac tylko z małych i dużych liter oraz cyfr")
        stdscr.refresh()
        time.sleep(2)
        ogladanie_gry(stdscr, current_row_idx)




# =========================

logop()
curses.wrapper(main)
