import pygame
from pygame.locals import *
import sys
import random
import csv

pygame.init()
screen = pygame.display.set_mode((800, 600))
screen.fill((0, 0, 0))

# 画面サイズ関連変数
screen_w = screen.get_width() #横幅
screen_h = screen.get_height() #縦幅

# 背景画面
bg_img = pygame.image.load("img/minecraft_img.jpeg")
title_img = pygame.image.load("img/MINECRAFT-TYPING.png")

# BGM
pygame.mixer.init(frequency=44100)

# 音楽ファイルをロード
pygame.mixer.music.load("sound/5bx6m-t5las.wav") #BGM
typing_se = pygame.mixer.Sound("sound/lib2w-11x9g.wav") # タイピング音
fuseikai_se = pygame.mixer.Sound("sound/hdbws-qquo6.wav")
pygame.mixer.music.play()

# シフトが押されたときの記号:mac英字配列
special_chars = {
    '0': ')',
    '1': '!',
    '2': '@',
    '3': '#',
    '4': '$',
    '5': '%',
    '6': '^',
    '7': '&',
    '8': '*',
    '9': '(',
}

# csvファイルからデータを持ってくる
with open("command.txt", 'r', encoding='UTF-8') as f:
    reader = csv.reader(f)
    command_list = list(reader)

# font
answer_font = pygame.font.Font(None, 30)
answer_text = answer_font.render("enter command here", True, (0, 0, 0))
command_font = pygame.font.Font(None, 40)
command_info_font = pygame.font.Font("HannariMincho-Regular.otf", 40)

command = "" #コマンドの文字列
command_info = "" #コマンドの意味
score = 100

moji = list("Enter space to start")

# キー入力に関する処理
def judge_key(key, capital, score):
    if (K_a <= key <= K_z) or (K_EXCLAIM <= key <= K_SLASH) or (K_0 <= key <= K_BACKQUOTE):
        char = pygame.key.name(key)

        # シフトが押されていたとき
        if capital:
            # 数字キーが押されていて、記号を出力したいとき
            if K_0 <= key <= K_9:
                char = special_chars[char]
            char = char.upper()

        # 正解のキーが押されたとき
        if char == command[len(moji)]:
            typing_se.play()
            moji.append(char)
        else:
            fuseikai_se.play()
            score -= 1
    # スペースキーが押されたときの処理
    if key == K_SPACE and command[len(moji)] == " ":
        typing_se.play()
        moji.append(" ")
    return "".join(moji), score


# ランダムで問題を設定する
def set_question(command_list):
    q_number = random.randrange(len(command_list))
    c = command_list[q_number][0]
    c_info = command_list[q_number][1]
    return q_number, c, c_info


start_typing = False #タイピングモードかどうか
capital_letter = False #大文字かどうか
running = True

while running:
    # 画面の設定
    screen.blit(bg_img, (0, 0))
    screen.blit(title_img, (screen_w / 2 - title_img.get_width() / 2, 100))
    # 文字の表示
    command_text = command_font.render(command, True, (0, 0, 0), (255, 255, 255))
    command_info_text = command_info_font.render(command_info, True, (0, 0, 0), (255, 255, 255))
    answer_text = answer_font.render("".join(moji), True, (0, 0, 0), (255, 255, 255))

    screen.blit(command_text, (screen_w / 2 - command_text.get_width() / 2, screen_h / 2))
    screen.blit(command_info_text,
                (screen_w / 2 - command_info_text.get_width() / 2, screen_h / 2 + command_text.get_height()))
    screen.blit(answer_text, (screen_w / 2 - answer_text.get_width() / 2,
                              screen_h / 2 + command_text.get_height() + command_info_text.get_height()))

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
            sys.exit()
        if event.type == KEYDOWN:
            # まだタイピングモードじゃないとき
            if not start_typing and event.key == K_SPACE:
                start_typing = True
                question_number, command, command_info = set_question(command_list)
                moji.clear()
                continue #while文を最初から書き直す
            if pygame.key.get_pressed()[K_LSHIFT]:
                capital_letter = True

            answer, score = judge_key(event.key, capital_letter, score)
            answer_text = answer_font.render(answer, True, (255, 0, 0))
            capital_letter = False
            if "".join(moji) == command:
                command_list.pop(question_number)

                if not command_list:
                    command = "game set"
                    command_info = f'スコアは{score}点です！'
                    start_typing = False
                else:
                    question_number, command, command_info = set_question(command_list)
                moji.clear()

    pygame.display.update()
