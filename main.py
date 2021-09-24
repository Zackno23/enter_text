import pygame
from pygame.locals import *
import sys
import random
import csv

pygame.init()
screen = pygame.display.set_mode((800, 600))
screen.fill((0, 0, 0))
# 画面サイズ関連変数
screen_w = screen.get_width()
screen_h = screen.get_height()
# 背景画面
bg_img = pygame.image.load("img/minecraft_img.jpeg")
title_img = pygame.image.load("img/MINECRAFT-TYPING.png")

# BGM
pygame.mixer.init(frequency=44100)
pygame.mixer.music.load("sound/Moog City 2.mp3")
# pygame.mixer.music.play()

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

with open("command.txt", 'r', encoding='UTF-8') as f:
    command_list = random.sample(list(csv.reader(f)), 5)

# font
answer_font = pygame.font.Font(None, 30)
command_font = pygame.font.Font(None, 40)
command_info_font = pygame.font.Font("HannariMincho-Regular.otf", 40)

answer_text = answer_font.render("enter command here", True, (0, 0, 0))

command = ""
command_info = ""
score = 100

moji = list("Enter space to start")

start_typing = False
capital_letter = False
running = True


def judge_key(key, capital, score):
    if (K_a <= key <= K_z) or (K_EXCLAIM <= key <= K_SLASH) or (K_0 <= key <= K_BACKQUOTE):
        char = pygame.key.name(key)

        # シフトが押されていたとき
        if capital:
            # 数字キーが押されていて、記号を出力したいとき
            if K_0 <= key <= K_9:
                char = special_chars[char]
            char = char.upper()
        if char == command[len(moji)]:
            moji.append(char)
        else:
            score -= 1

    if key == K_SPACE and command[len(moji)] == " ":
        moji.append(" ")
    return "".join(moji), score


while running:
    screen.blit(bg_img, (0, 0))
    screen.blit(title_img, (screen_w / 2 - title_img.get_width() / 2, 100))

    command_text = command_font.render(command, True, (0, 0, 0), (255, 255, 255))
    command_info_text = command_info_font.render(command_info, True, (0, 0, 0), (255, 255, 255))
    answer_text = answer_font.render("".join(moji), True, (0, 0, 0), (255, 255, 255))

    screen.blit(command_text, (screen_w / 2 - command_text.get_width() / 2, screen_h / 2))
    screen.blit(command_info_text,
                (screen_w / 2 - command_info_text.get_width() / 2, screen_h / 2 + command_text.get_height()))
    screen.blit(answer_text, (screen_w / 2 - answer_text.get_width() / 2,
                              screen_h / 2 + command_text.get_height() + command_info_text.get_height()))

    for event in pygame.event.get():
        # 終了処理
        if event.type == QUIT:
            running = False
            sys.exit()

        if event.type == KEYDOWN:
            if not start_typing:
                # 最初にスペースキーを押したとき
                if event.key == K_SPACE:
                    start_typing = True
                    command = command_list[0][0]
                    command_info = command_list[0][1]
                    moji.clear()
                continue
            # シフトキーを押す→大文字の処理
            if pygame.key.get_pressed()[K_LSHIFT]:
                capital_letter = True
            answer, score = judge_key(event.key, capital_letter, score)
            answer_text = answer_font.render(answer, True, (255, 0, 0))
            capital_letter = False
            if "".join(moji) == command:
                command_list.pop(0)

                if not command_list:
                    command = "game set"
                    command_info = f'スコアは{score}点です！'
                    start_typing = False

                else:
                    command = command_list[0][0]
                    command_info = command_list[0][1]
                moji.clear()
    # 画面を更新
    pygame.display.update()
