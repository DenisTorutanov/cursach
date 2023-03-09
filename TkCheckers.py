from tkinter import *
import random
import time
import copy
from tkinter import messagebox

MainWindow = Tk()
MainWindow.title('Checkers')
Square = Canvas(MainWindow, width=795, height=795, bg='#1c1c1c')
Square.pack()

n2_sp = ()
ur = 2
k_rez = 0
o_rez = 0
poz1_x = -1


HOD = 0

peshki = [PhotoImage(file="resources/P1.png"), PhotoImage(file="resources/P2.png"), PhotoImage(file="resources/K1.png"), PhotoImage(file="resources/K2.png")]


# Движение шашки
def draw_viv(x1, y1, x2, y2):
    global peshki # Картинки с фигурами
    global Board # Игровое поле
    global choosedFigure, isGoodFigure
    x = 0
    Square.delete('all')

    for i in range(0, 64):
        if i % 2 == 0:
            dy = i // 8
            dx = i % 8 + dy % 2
            Square.create_rectangle(dx * 100, dy * 100, dx * 100 + 100, dy * 100 + 100, fill="white")

    for y in range(8):
        for x in range(8):
            figura = Board[y][x]
            if figura: # Если шашка в клетке
                if (x1, y1) != (x, y): # Если шашка не та, что двигается
                    Square.create_image(x * 100 + 10, y * 100 + 10, anchor=NW, image=peshki[figura - 1])

    figura = Board[y1][x1] # Есть ли шашка в нашей клетке
    if figura:
        Square.create_image(x1 * 100 + 10, y1 * 100 + 10, anchor=NW, image=peshki[figura - 1], tag='choosed')
    isGoodFigure = Square.create_rectangle(0, 0, 0, 0, outline="#05ff69", width=5)
    choosedFigure = Square.create_rectangle(0, 0, 0, 0, outline="#ffac05", width=5)
    znak_x = 1 if x1 < x2 else -1
    znak_y = 1 if y1 < y2 else -1
    if x1 == x2:
        znak_x = 0
    if y1 == y2:
        znak_y = 0
    kletok = abs(x1 - x2)
    kletok_y = abs(y1 - y2)

    for ii in range(10):
        Square.move('choosed', 0.1 * 100 * znak_x * kletok, 0.1 * 100 * znak_y * kletok_y)
        Square.update()
        time.sleep(0.001)


def start_game():
    global Board
    Board = [
        [3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1]
    ]


# Подсветка клетки под курсором
def HighlightCell(event):
    global HOD
    cellX, cellY = (event.x) // 100, (event.y) // 100
    # Проверка на возможность выбора клетки (Если своя фигура под курсором)
    goodCell = False
    if 0 <= cellX < 8 and 0 <= cellY < 8 and HOD < 2:
        if Board[cellY][cellX] == 1:
            Square.coords(isGoodFigure, cellX * 100 + 5, cellY * 100 + 5, cellX * 100 + 95, cellY * 100 + 95)
            goodCell = True
    if not goodCell:
        Square.coords(isGoodFigure, -5, -5, -5, -5)


# Обработчик кликов
def ClickHandler(event):
    global poz1_x, poz1_y, poz2_x, poz2_y
    global HOD
    x, y = (event.x) // 100, (event.y) // 100
    if Board[y][x] == 1 or Board[y][x] == 2 and HOD == 0:
        Square.coords(choosedFigure, x * 100 + 5, y * 100 + 5, x * 100 + 95, y * 100 + 95)
        poz1_x, poz1_y = x, y
    else:
        if poz1_x != -1:
            poz2_x, poz2_y = x, y
            if HOD == 0:
                PlayerTurn()
                if HOD == 1:
                    time.sleep(0.5)
                    CompTurn()
            poz1_x = -1
            Square.coords(choosedFigure, -5, -5, -5, -5)


def GameOver(s, debug=""):
    global HOD
    reasons = [
        'Вы проиграли!\nНажми "Да" что бы начать заново.',
        'Вы выиграли!\nНажми "Да" что бы начать заново.',
        'Ходов больше нет. Вы проиграли\nНажми "Да" что бы начать заново.',
        'У соперника больше нет ходов. Вы выиграли\nНажми "Да" что бы начать заново.'
    ]
    isNewGame = messagebox.askyesno(title="Игра окончена", message=reasons[s - 1] + debug, icon='info')

    if isNewGame:
        start_game()
        draw_viv(-1, -1, -1, -1)
        HOD = 0


def AvailableCompTurns():
    turns_list = looking_k1([])
    if not (turns_list):
        turns_list = looking_k2([])
    return turns_list


def CheckCompTurn(tur, n_turns_list, turns_list):
    global Board
    global n2_sp
    global l_rez, k_rez, o_rez
    if not turns_list:
        turns_list = AvailableCompTurns()
    if turns_list:
        k_Board = copy.deepcopy(Board)
        for ((poz1_x, poz1_y), (poz2_x, poz2_y)) in turns_list:
            t_turns_list = Turn(0, poz1_x, poz1_y, poz2_x, poz2_y)
            if t_turns_list:
                CheckCompTurn(tur, (n_turns_list + ((poz1_x, poz1_y),)), t_turns_list)
            else:
                CheckPlayerTurn(tur, [])
                if tur == 1:
                    t_rez = o_rez / k_rez
                    if not n2_sp:
                        n2_sp = (n_turns_list + ((poz1_x, poz1_y), (poz2_x, poz2_y)),)
                        l_rez = t_rez
                    else:
                        if t_rez == l_rez:
                            n2_sp = n2_sp + (n_turns_list + ((poz1_x, poz1_y), (poz2_x, poz2_y)),)
                        if t_rez > l_rez:
                            n2_sp = (n_turns_list + ((poz1_x, poz1_y), (poz2_x, poz2_y)),)
                            l_rez = t_rez
                    o_rez = 0
                    k_rez = 0

            Board = copy.deepcopy(k_Board)
    else:
        s_k, s_i = skan()
        o_rez += (s_k - s_i)
        k_rez += 1


def AvailablePlayerTurns():
    turns_list = looking_i1()
    if not turns_list:
        turns_list = looking_i2([])
    return turns_list


def CheckPlayerTurn(tur, turns_list):
    global Board, k_rez, o_rez
    global poz1_x, poz1_y, poz2_x, poz2_y
    global ur
    if not turns_list:
        turns_list = AvailablePlayerTurns()
    if turns_list:
        k_Board = copy.deepcopy(Board)
        for ((poz1_x, poz1_y), (poz2_x, poz2_y)) in turns_list:
            t_turns_list = Turn(0, poz1_x, poz1_y, poz2_x, poz2_y)
            if t_turns_list:
                CheckPlayerTurn(tur, t_turns_list)
            else:
                if tur > ur:
                    CheckCompTurn(tur + 1, (), [])
                else:
                    s_k, s_i = skan()
                    o_rez += (s_k - s_i)
                    k_rez += 1

            Board = copy.deepcopy(k_Board)
    else:
        s_k, s_i = skan()
        o_rez += (s_k - s_i)
        k_rez += 1


def skan():
    global Board
    s_i = 0
    s_k = 0
    for x in Board:
        for y in x:
            if y == 1: s_i += 1
            if y == 2: s_i += 3
            if y == 3: s_k += 1
            if y == 4: s_k += 3

    if s_i == 0 and HOD == 0:
        GameOver(1)
    elif s_k == 0 and HOD < 1:
        GameOver(2)
    return s_k, s_i


def PlayerTurn():
    global poz1_x, poz1_y, poz2_x, poz2_y
    global HOD
    HOD = 1
    turns_list = AvailablePlayerTurns()
    if turns_list:
        if ((poz1_x, poz1_y), (poz2_x, poz2_y)) in turns_list:
            t_turns_list = Turn(1, poz1_x, poz1_y, poz2_x, poz2_y)
            if t_turns_list:
                HOD = 0
        else:
            HOD = 0
    Square.update()
    s_k, s_i = skan()
    if len(AvailableCompTurns()) == 0 and s_k != 0:
        GameOver(4)
    elif s_k == 0:
        GameOver(2)


def CompTurn():
    global n2_sp
    global HOD
    HOD = 1
    CheckCompTurn(1, (), [])
    if n2_sp:
        kh = len(n2_sp)
        th = random.randint(0, kh - 1)
        dh = len(n2_sp[th])
        for h in n2_sp:
            h = h
        for i in range(dh - 1):
            turns_list = Turn(1, n2_sp[th][i][0], n2_sp[th][i][1], n2_sp[th][1 + i][0], n2_sp[th][1 + i][1])
        n2_sp = []
        HOD = 0
    Square.update()
    s_k, s_i = skan()
    if s_i != 0 and len(AvailablePlayerTurns()) == 0:
        GameOver(3)


def Turn(f, poz1_x, poz1_y, poz2_x, poz2_y):
    global Board
    if f: draw_viv(poz1_x, poz1_y, poz2_x, poz2_y)

    if poz2_y == 0 and Board[poz1_y][poz1_x] == 1:
        Board[poz1_y][poz1_x] = 2

    if poz2_y == 7 and Board[poz1_y][poz1_x] == 3:
        Board[poz1_y][poz1_x] = 4

    Board[poz2_y][poz2_x] = Board[poz1_y][poz1_x]
    Board[poz1_y][poz1_x] = 0


    kx = ky = 1
    if poz1_x < poz2_x: kx = -1
    if poz1_y < poz2_y: ky = -1
    if poz1_x == poz2_x: kx = 0
    if poz1_y == poz2_y: ky = 0

    x_poz, y_poz = poz2_x, poz2_y
    while (poz1_x != x_poz) or (poz1_y != y_poz):
        x_poz += kx
        y_poz += ky
        if Board[y_poz][x_poz] != 0:
            Board[y_poz][x_poz] = 0
            if f:
                draw_viv(-1, -1, -1, -1)
            if Board[poz2_y][poz2_x] == 3 or Board[poz2_y][poz2_x] == 4:  #
                return looking_k1p([], poz2_x, poz2_y)
            elif Board[poz2_y][poz2_x] == 1 or Board[poz2_y][poz2_x] == 2:
                return looking_i1p([], poz2_x, poz2_y)
    if f:
        draw_viv(poz1_x, poz1_y, poz2_x, poz2_y)


def looking_k1(turns_list):
    for y in range(8):
        for x in range(8):
            turns_list = looking_k1p(turns_list, x, y)
    return turns_list


def looking_k1p(turns_list, x, y):
    if Board[y][x] == 3:
        for ix, iy in (-1, 1), (1, 1), (0, 1), (1, 0), (-1, 0):
            if 0 <= y + iy + iy <= 7 and 0 <= x + ix + ix <= 7:
                if Board[y + iy][x + ix] == 1 or Board[y + iy][x + ix] == 2:
                    if Board[y + iy + iy][x + ix + ix] == 0:
                        turns_list.append(((x, y), (x + ix + ix, y + iy + iy)))
    if Board[y][x] == 4:
        for ix, iy in (-1, -1), (1, -1), (0, -1), (1, 0), (-1, 0), (-1, 1), (1, 1), (0, 1):
            if 0 <= y + iy + iy <= 7 and 0 <= x + ix + ix <= 7:
                if Board[y + iy][x + ix] == 1 or Board[y + iy][x + ix] == 2:
                    if Board[y + iy + iy][x + ix + ix] == 0:
                        turns_list.append(((x, y), (x + ix + ix, y + iy + iy)))
    return turns_list


def looking_k2(turns_list):
    for y in range(8):
        for x in range(8):
            if Board[y][x] == 3:
                for ix, iy in (-1, 1), (1, 1), (0, 1), (1, 0), (-1, 0):
                    if 0 <= y + iy <= 7 and 0 <= x + ix <= 7:
                        if Board[y + iy][x + ix] == 0:
                            turns_list.append(((x, y), (x + ix, y + iy)))
                        if Board[y + iy][x + ix] == 1 or Board[y + iy][x + ix] == 2:
                            if 0 <= y + iy * 2 <= 7 and 0 <= x + ix * 2 <= 7:
                                if Board[y + iy * 2][x + ix * 2] == 0:
                                    turns_list.append(((x, y), (x + ix * 2, y + iy * 2)))
            if Board[y][x] == 4:
                for ix, iy in (-1, -1), (1, -1), (0, -1), (1, 0), (-1, 0), (-1, 1), (1, 1), (0, 1):
                    if 0 <= y + iy <= 7 and 0 <= x + ix <= 7:
                        if Board[y + iy][x + ix] == 0:
                            turns_list.append(((x, y), (x + ix, y + iy)))
                        if Board[y + iy][x + ix] == 1 or Board[y + iy][x + ix] == 2:
                            if 0 <= y + iy * 2 <= 7 and 0 <= x + ix * 2 <= 7:
                                if Board[y + iy * 2][x + ix * 2] == 0:
                                    turns_list.append(((x, y), (x + ix * 2, y + iy * 2)))
    return turns_list


def looking_i1():
    turns_list = []
    for y in range(8):
        for x in range(8):
            turns_list = looking_i1p(turns_list, x, y)
    return turns_list


def looking_i1p(turns_list, x, y):
    if Board[y][x] == 1:
        for ix, iy in (-1, -1), (1, -1), (0, -1), (1, 0), (-1, 0):
            if 0 <= y + iy + iy <= 7 and 0 <= x + ix + ix <= 7:
                if Board[y + iy][x + ix] == 3 or Board[y + iy][x + ix] == 4:
                    if Board[y + iy + iy][x + ix + ix] == 0:
                        turns_list.append(((x, y), (x + ix + ix, y + iy + iy)))
    if Board[y][x] == 2:
        for ix, iy in (-1, -1), (1, -1), (0, -1), (1, 0), (-1, 0), (-1, 1), (1, 1), (0, 1):
            if 0 <= y + iy + iy <= 7 and 0 <= x + ix + ix <= 7:
                if Board[y + iy][x + ix] == 3 or Board[y + iy][x + ix] == 4:
                    if Board[y + iy + iy][x + ix + ix] == 0:
                        turns_list.append(((x, y), (x + ix + ix, y + iy + iy)))
    return turns_list


def looking_i2(turns_list):
    for y in range(8):
        for x in range(8):
            if Board[y][x] == 1: #НВ       ПВ     Вверх   Направо  Налево
                for ix, iy in (-1, -1), (1, -1), (0, -1), (1, 0), (-1, 0):
                    if 0 <= y + iy <= 7 and 0 <= x + ix <= 7:
                        if Board[y + iy][x + ix] == 0:
                            turns_list.append(((x, y), (x + ix, y + iy)))
                        if Board[y + iy][x + ix] == 3 or Board[y + iy][x + ix] == 4:
                            if 0 <= y + iy * 2 <= 7 and 0 <= x + ix * 2 <= 7:
                                if Board[y + iy * 2][x + ix * 2] == 0:
                                    turns_list.append(((x, y), (x + ix * 2, y + iy * 2)))
            if Board[y][x] == 2:
                for ix, iy in (-1, -1), (1, -1), (0, -1), (1, 0), (-1, 0), (-1, 1), (1, 1), (0, 1):
                    if 0 <= y + iy <= 7 and 0 <= x + ix <= 7:
                        if Board[y + iy][x + ix] == 0:
                            turns_list.append(((x, y), (x + ix, y + iy)))
                        if Board[y + iy][x + ix] == 3 or Board[y + iy][x + ix] == 4:
                            if 0 <= y + iy * 2 <= 7 and 0 <= x + ix * 2 <= 7:
                                if Board[y + iy * 2][x + ix * 2] == 0:
                                    turns_list.append(((x, y), (x + ix * 2, y + iy * 2)))
    return turns_list


def run():
    start_game()
    draw_viv(-1, -1, -1, -1)
    Square.bind("<Motion>", HighlightCell)
    Square.bind("<Button-1>", ClickHandler)
    mainloop()