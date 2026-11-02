import os
import random
import tkinter.font as tkFont
import unicodedata
from tkinter import messagebox

import pandas as pd
from PIL import Image, ImageDraw, ImageTk

try:
    import tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import pygame
except ImportError:
    pygame = None

RESAMPLE_FILTER = getattr(Image, "Resampling", Image).LANCZOS


def create_halloween_background(path):
    image = Image.new("RGB", (600, 500), (22, 11, 29))
    draw = ImageDraw.Draw(image)
    for y in range(500):
        shade = int(30 + (y / 500) * 80)
        color = (shade, 15, 30)
        draw.line((0, y, 600, y), fill=color)

    moon_x, moon_y, moon_r = 470, 90, 42
    for r in range(moon_r, 0, -1):
        alpha = max(0, 255 - (moon_r - r) * 8)
        draw.ellipse((moon_x - r, moon_y - r, moon_x + r, moon_y + r), fill=(alpha, alpha, 180))
    draw.ellipse((moon_x - 25, moon_y - 25, moon_x + 25, moon_y + 25), fill=(255, 230, 160))

    for x in range(40, 560, 60):
        y = 70 + (x % 120)
        draw.ellipse((x, y, x + 10, y + 10), fill=(255, 255, 220))

    for x in range(100, 520, 120):
        draw.polygon([(x, 420), (x + 22, 390), (x + 44, 420)], fill=(250, 120, 40))
        draw.rectangle((x + 14, 420, x + 30, 500), fill=(30, 30, 30))

    image.save(path)
    return path


def resolve_image_path(path):
    if os.path.exists(path):
        return path
    if path == 'halloween.png':
        create_halloween_background(path)
        return path
    raise FileNotFoundError(f"Missing required asset: {path}")


def normalize_text(value):
    if value is None:
        return ""
    normalized = unicodedata.normalize("NFKD", str(value))
    return normalized.encode("ascii", "ignore").decode("ascii")


def resize_image(path, size):
    return Image.open(resolve_image_path(path)).resize(size, RESAMPLE_FILTER)


def build_game_button(parent, text, command, width=None, font=None, bg="#120d17", fg="#ffd166",
                     hover_bg="#ffd166", hover_fg="#120d17", border_color="#ff9f1c",
                     active_bg="#ffb703", active_fg="#120d17", padx=20, pady=10):
    button = tk.Button(
        parent,
        text=text,
        command=command,
        width=width,
        font=font,
        fg=fg,
        bg=bg,
        activeforeground=active_fg,
        activebackground=active_bg,
        bd=0,
        relief="flat",
        highlightthickness=4,
        highlightbackground=border_color,
        highlightcolor=border_color,
        padx=padx,
        pady=pady,
        cursor="hand2",
    )
    button.configure(
        compound="center",
        justify="center",
    )
    button.bind("<Enter>", lambda event: (button.config(bg=hover_bg, fg=hover_fg, highlightbackground="#fff1a6", highlightcolor="#fff1a6"), button.update_idletasks()))
    button.bind("<Leave>", lambda event: (button.config(bg=bg, fg=fg, highlightbackground=border_color, highlightcolor=border_color), button.update_idletasks()))
    return button


class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        ImagePath = 'halloween.png'
        canv = tk.Canvas(self, width=600, height=500, bg='white')
        canv.pack(side='bottom')
        self.img = ImageTk.PhotoImage(resize_image(ImagePath, (600, 500)))
        canv.create_image(0, 0, anchor="nw", image=self.img)

        labelFont = tkFont.Font(family="Arial", size=40, weight="bold", slant="italic")
        canv.create_text((600 // 2), (500 // 2) - 40, fill="white", text="Speed Game", font=labelFont)

        startBtnFont = tkFont.Font(family="Consolas", size=20, weight="bold")
        startBtn = build_game_button(
            canv,
            text="START",
            command=lambda: master.switch_frame(CategoryPage),
            width=12,
            font=startBtnFont,
            padx=18,
            pady=12,
        )
        canv.create_window((600 // 2), (500 // 2) + 100, window=startBtn)


class CategoryPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        ImagePath = 'halloween.png'
        canv = tk.Canvas(self, width=600, height=500, bg='white')
        canv.pack(side='bottom')
        self.img = ImageTk.PhotoImage(resize_image(ImagePath, (600, 500)))
        canv.create_image(0, 0, anchor="nw", image=self.img)

        labelFont = tkFont.Font(family="Arial", size=40, weight="bold", slant="italic")
        canv.create_text((600 // 2), (500 // 2) - 190, fill="white", text="Speed Game", font=labelFont)

        btnFont = tkFont.Font(family="Consolas", size=20, weight="bold")
        countryBtn = build_game_button(
            self,
            text="COUNTRY",
            command=lambda: master.switch_frame(CountryPage),
            width=15,
            font=btnFont,
            padx=18,
            pady=10,
        )
        canv.create_window((600 // 2), (500 // 2) - 100, window=countryBtn)

        prevBtn = build_game_button(
            self,
            text="BACK",
            command=lambda: master.switch_frame(StartPage),
            width=15,
            font=btnFont,
            padx=18,
            pady=10,
        )
        canv.create_window((600 // 2), (500 // 2) - 10, window=prevBtn)


class CountryPage(tk.Frame):
    def __init__(self, master):
        global pass_count, answer, country_img
        global df, pass_window
        tk.Frame.__init__(self, master)

        filename = random.choice(os.listdir("./images"))
        code = filename.split(".")[0]

        # 엑셀에 없는 이미지일 경우 예외처리
        while code.upper() not in df.index:
            filename = random.choice(os.listdir("./images"))
            code = filename.split(".")[0]

        countryPath = "./images/" + filename

        print(countryPath)
        print(normalize_text(df["country"][code.upper()]))
        print(filename)
        answer = normalize_text(df["country"][code.upper()])

        backgroundPath = 'halloween.png'
        canv = tk.Canvas(self, width=600, height=500, bg='white')
        canv.pack()
        self.img1 = ImageTk.PhotoImage(resize_image(backgroundPath, (600, 500)))
        canv.create_image(0, 0, anchor="nw", image=self.img1)

        titleFont = tkFont.Font(family="Arial", size=40, weight="bold", slant="italic")
        canv.create_text((600 // 2), (500 // 2) - 190, fill="white", text="Country", font=titleFont)

        self.img2 = ImageTk.PhotoImage(resize_image(countryPath, (180, 130)))
        country_img = canv.create_image(210, 130, anchor="nw", image=self.img2)

        labelFont = tkFont.Font(family="Arial", size=17, slant="italic")
        BtnFont = tkFont.Font(family="Consolas", size=15)

        canv.create_text((600 // 2), (500 // 2) + 40, fill="white", text="answer", font=labelFont)

        input_text = tk.Entry(self, width=30)
        canv.create_window((600 // 2), (500 // 2) + 70, window=input_text)

        check_btn = build_game_button(
            self,
            text="CHECK",
            command=lambda: self.checkBtn_click(master, input_text.get(), answer, canv, country_img),
            width=10,
            font=BtnFont,
            padx=14,
            pady=8,
        )
        canv.create_window((600 // 2) - 80, (500 // 2) + 140, window=check_btn)

        pass_btn = build_game_button(
            self,
            text="PASS: " + str(pass_count) + "/3",
            command=lambda: self.passBtn_click(tk, canv, country_img),
            width=12,
            font=BtnFont,
            padx=14,
            pady=8,
        )
        pass_window = canv.create_window((600 // 2) + 80, (500 // 2) + 140, window=pass_btn)

        self.num = 180
        mins, secs = divmod(self.num, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        TimerFont = tkFont.Font(family="Arial", size=30, weight="bold", slant="italic")
        timer_text = canv.create_text(100, 100, fill="white", text=timeformat, font=TimerFont)
        canv.after(1, self.count, canv, timer_text)

    def count(self, canv, timer_text):
        mins, secs = divmod(self.num, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        canv.delete(timer_text)
        TimerFont = tkFont.Font(family="Arial", size=30, weight="bold", slant="italic")
        timer_text = canv.create_text(100, 100, fill="white", text=timeformat, font=TimerFont)
        self.num -= 1
        if self.num < 0:
            msgBox = tk.messagebox.askretrycancel('Exit App', 'Really Quit?')
            if msgBox == True:
                self.master.switch_frame(StartPage)
            else:
                self.master.switch_frame(FinishPage)
        else:
            canv.after(1000, self.count, canv, timer_text)

    # click check button
    def checkBtn_click(self, master, user_text, check_answer, canv, check_img):
        global answer, country_img
        global correct_count, problem_count
        problem_count -= 1

        user_text = normalize_text(user_text).upper().replace(" ", "")
        check_answer = normalize_text(check_answer).replace(" ", "")

        if (user_text == check_answer):
            # correct
            print('Correct!')
            ImagePath = 'correct.png'
            self.img3 = ImageTk.PhotoImage(resize_image(ImagePath, (100, 100)))
            resultImage = canv.create_image(450, 30, anchor="nw", image=self.img3)
            correct_count += 1
        else:
            # wrong
            print('Wrong!')
            ImagePath = 'wrong.png'
            self.img4 = ImageTk.PhotoImage(resize_image(ImagePath, (100, 100)))

            resultImage = canv.create_image(450, 30, anchor="nw", image=self.img4)

        # resolve 15 problems
        if problem_count <= 0:
            master.switch_frame(FinishPage)
        canv.after(1000, self.delete_img, canv, resultImage)
        filename = random.choice(os.listdir("./images"))
        code = filename.split(".")[0]

        # 엑셀에 없는 이미지일 경우 예외처리
        while code.upper() not in df.index:
            filename = random.choice(os.listdir("./images"))
            code = filename.split(".")[0]

        countryPath = "./images/" + filename
        canv.after(1000,self.delete_img, canv, check_img)
        self.img2 = ImageTk.PhotoImage(resize_image(countryPath, (180, 130)))
        country_img = canv.create_image(210, 130, anchor="nw", image=self.img2)
        answer = normalize_text(df["country"][code.upper()])

        print(answer)

    def passBtn_click(self, tk, canv, check_img):
        global pass_count, pass_window
        global country_img, answer
        pass_count = pass_count - 1
        if (pass_count < 0):
            print("Pass limit reached")
            pass_count = 0
            tk.messagebox.showerror('Pass', 'You Don\'t have pass ticket!')
        else:
            filename = random.choice(os.listdir("./images"))
            code = filename.split(".")[0]

            # 엑셀에 없는 이미지일 경우 예외처리
            while code.upper() not in df.index:
                filename = random.choice(os.listdir("./images"))
                code = filename.split(".")[0]

            countryPath = "./images/" + filename
            canv.after(1000, self.delete_img, canv, check_img)
            self.img2 = ImageTk.PhotoImage(resize_image(countryPath, (180, 130)))
            country_img = canv.create_image(210, 130, anchor="nw", image=self.img2)
            answer = normalize_text(df["country"][code.upper()])

        self.delete_img(canv, pass_window)
        BtnFont = tkFont.Font(family="Consolas", size=15, weight="bold")
        pass_btn = build_game_button(
            self,
            text="PASS: " + str(pass_count) + "/3",
            command=lambda: self.passBtn_click(tk, canv, country_img),
            width=12,
            font=BtnFont,
            padx=14,
            pady=8,
        )
        pass_window = canv.create_window((600 // 2) + 80, (500 // 2) + 140, window=pass_btn)

    def delete_img(self, canv, dele_img_name):
        canv.delete(dele_img_name)


class FinishPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        ImagePath = 'halloween.png'
        canv = tk.Canvas(self, width=600, height=500, bg='white')
        canv.pack(side='bottom')
        self.img = ImageTk.PhotoImage(resize_image(ImagePath, (600, 500)))
        canv.create_image(0, 0, anchor="nw", image=self.img)

        labelFont = tkFont.Font(family="Arial", size=40, weight="bold")
        canv.create_text((600 // 2), (500 // 2) - 50, fill="white", text="total score : " + str(correct_count)+ "/15", font=labelFont)
        canv.create_text((600 // 2), (500 // 2) + 50, fill="white", text="Good Job!", font=labelFont)


if __name__ == "__main__":
    if pygame is not None:
        pygame.init()
        mySound = pygame.mixer.Sound("SpeedGameBgm.mp3")
        mySound.play(-1)
    pass_count = 3
    problem_count = 15
    correct_count = 0
    answer = 0
    country_img = 0
    pass_window = 0

    df = pd.read_excel("./CountryCodeData.xlsx", index_col=0, names=["code", "country"])
    print(df["country"]["KR"])

    app = SampleApp()
    app.title("Speed Game")

    app.geometry('600x500+100+100')
    app.mainloop()
