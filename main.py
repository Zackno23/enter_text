"""
マインクラフトのタイピングゲームです
同じプロジェクトにあるcommand.txtの中身を書き換えると、問題の追加・削除ができます。
問題数を変更するには、４２行目あたりの
command_list = random.sample(list(csv.reader(f)), 5)
の最後の５を変更すればできます。
その他にもいろいろコードをいじって、オリジナルのタイピングゲームを作っちゃってください
"""
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

# フォント（文字の大きさや字体など）
answer_font = pygame.font.Font(None, 30)
command_font = pygame.font.Font(None, 40)
command_jap_font = pygame.font.Font("HannariMincho-Regular.otf", 40)

answer_text = answer_font.render("enter command here", True, (0, 0, 0))

# コマンド自体
command = ""
# 日本語の説明文
command_jap = ""
# スコア初期値
score = 100

moji = list("Enter space to start")

start_typing = False
capital_letter = False
running = True

# 入力された文字を判定する関数
# 引数（入力されたキー, 大文字かどうか, 現在の点数）
# 戻り値 入力を連結した文字列, 結果の文字列
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
# 画面・画像関連
    # 背景画像
    screen.blit(bg_img, (0, 0))
    # タイトル画像
    screen.blit(title_img, (screen_w / 2 - title_img.get_width() / 2, 100))
    # 問題出力部分
    command_text = command_font.render(command, True, (0, 0, 0), (255, 255, 255))
    screen.blit(command_text, (screen_w / 2 - command_text.get_width() / 2, screen_h / 2))
    # 問題のコマンドの日本語での説明出力部分
    command_jap_text = command_jap_font.render(command_jap, True, (0, 0, 0), (255, 255, 255))
    screen.blit(command_jap_text,
                (screen_w / 2 - command_jap_text.get_width() / 2, screen_h / 2 + command_text.get_height()))
    # コマンド入力部分
    answer_text = answer_font.render("".join(moji), True, (0, 0, 0), (255, 255, 255))
    screen.blit(answer_text, (screen_w / 2 - answer_text.get_width() / 2,
                              screen_h / 2 + command_text.get_height() + command_jap_text.get_height()))

    for event in pygame.event.get():
        # 終了処理
        if event.type == QUIT:
            running = False
            sys.exit()

        # キーが押されたとき
        if event.type == KEYDOWN:
            # ゲームが始まってなければ
            if not start_typing:
                # 最初にスペースキーを押したとき
                if event.key == K_SPACE:
                    start_typing = True
                    command = command_list[0][0]
                    command_jap = command_list[0][1]
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
                    command_jap = f'スコアは{score}点です！'
                    start_typing = False

                else:
                    command = command_list[0][0]
                    command_jap = command_list[0][1]
                # mojiを空にする
                moji.clear()
    # 画面を更新
    pygame.display.update()
