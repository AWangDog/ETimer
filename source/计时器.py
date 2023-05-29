import time
import pygame
import tkinter as tk
from tkinter import ttk
import threading
import datetime
import pytz
import sys


def play_sound():
    pygame.mixer.init()
    sound = pygame.mixer.Sound("audio\electric_bell.mp3")
    sound.play()
    pygame.time.wait(5000)  # 播放5秒
    try:
        sound.stop()
    except:
        pass

def play_sound2():
    pygame.mixer.init()
    sound = pygame.mixer.Sound("audio\electric_bell.mp3")
    sound.play()
    pygame.time.wait(5000)  # 播放5秒
    try:
        sound.stop()
    except:
        pass

def check_start_time():
    try:
        while True:
            current_time = datetime.datetime.now().replace(microsecond=0)
            target_time = datetime.datetime.strptime(datetime.datetime.strftime(current_time, "%Y-%m-%d") + startText.get(), "%Y-%m-%d%H:%M:%S")
            if current_time == target_time:
                threading.Thread(target=play_sound2).start()
                time.sleep(1)
            time.sleep(0.1)
    except:
        pass
        
def set_time_text():
    class_name = classNameText.get()
    if class_name == "语文":
        TimeText.set("02:30:00")
    elif class_name == "英语":
        TimeText.set("02:00:00")
    elif class_name == "数学":
        TimeText.set("02:00:00")
    elif class_name in ["物理", "化学", "生物"]:
        TimeText.set("01:30:00")


def save_settings():
    with open("settings.txt", "w") as file:
        file.write(titleText.get() + "\n")
        file.write(classNameText.get() + "\n")
        file.write(TimeText.get() + "\n")
        file.write(startText.get() + "\n")

def load_settings():
    try:
        with open("settings.txt", "r") as file:
            lines = file.readlines()
            titleText.set(lines[0].strip())
            classNameText.set(lines[1].strip())
            TimeText.set(lines[2].strip())
    except FileNotFoundError:
        pass

    classNameText.trace_add("write", lambda *args: set_time_text())


def scale_input(input_value):
    input_min = 2
    input_max = 14
    output_min = 6.25
    output_max = 14

    input_range = input_max - input_min
    output_range = output_max - output_min

    input_scaled = (input_value - input_min) / input_range
    output_scaled = output_min + (input_scaled * output_range)

    return output_scaled

def start_pygame_window():
    global sound_played
    global sound_played2
    sound_played = False
    sound_played2 = False
    pygame.init()
    pygame.font.init()
    try:
        classTimeText = datetime.datetime.strptime(TimeText.get(), "%H:%M:%S")
        startTime = datetime.datetime.strptime(time.strftime("%Y-%m-%d ") + startText.get(), "%Y-%m-%d %H:%M:%S")
        overTime = startTime + datetime.timedelta(hours=classTimeText.hour, minutes=classTimeText.minute, seconds=classTimeText.second)
    except:
        menu.wm_deiconify()
        return
    def update():
        pTimeRect.centerx = winRect.centerx / 2.5
        pTimeRect.centery = winRect.centery / 1.06
        titleRect.centerx = winRect.centerx / 1
        titleRect.centery = winRect.centery / 3.1
        nowTimeRect.centerx = winRect.centerx / 1
        nowTimeRect.centery = winRect.centery / 1.15
        classNameRect.x = winRect.centerx / 7
        classNameRect.y = winRect.centery / 0.85
        classTimeRect.x = winRect.centerx / 7
        classTimeRect.y = winRect.centery / 0.66
        countdownRect.centerx = winRect.centerx / 0.8
        countdownRect.centery = winRect.centery / 0.77
        xRect.x = winRect.right - xRect.width
        xRect.y = winRect.y

        win.fill(white)
        win.blit(nowTime, nowTimeRect)
        win.blit(pTime, pTimeRect)
        win.blit(title, titleRect)
        win.blit(className, classNameRect)
        win.blit(classTime, classTimeRect)
        win.blit(countdown, countdownRect)
        win.blit(x, xRect)
        pygame.display.update()

    def Countdown():
        global sound_played2
        nowTime = overTime - datetime.timedelta(hours=datetime.datetime.now().hour,
                                               minutes=datetime.datetime.now().minute,
                                               seconds=datetime.datetime.now().second)
        classTime1 = datetime.datetime.strptime(
            time.strftime("%Y-%m-%d ") + str(classTimeText.hour) + ":" + str(classTimeText.minute) + ":" + str(
                classTimeText.second), "%Y-%m-%d %H:%M:%S")
        if nowTime < classTime1:
            return nowTime
        else:
            return classTimeText

    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255,0,0)

    win = pygame.display.set_mode((tk.Tk().winfo_screenwidth(), tk.Tk().winfo_screenheight()), pygame.NOFRAME)
    winRect = win.get_rect()
    titlelen = len(titleText.get())

    nowTimeSize = int(tk.Tk().winfo_screenwidth() / 8)
    nowTimeText = time.strftime("%I:%M:%S")
    nowTimeFont = pygame.font.Font("ttf\Roboto-Regular.ttf", nowTimeSize)
    nowTime = nowTimeFont.render(nowTimeText, True, black, white)
    nowTimeRect = nowTime.get_rect()
    
    titleSize = int(tk.Tk().winfo_screenwidth() / scale_input(titlelen))
    titleFont = pygame.font.Font("ttf\方正宋刻本秀楷简体.ttf", titleSize)
    title = titleFont.render(titleText.get(), True, black, white)
    titleRect = title.get_rect()

    pTimeSize = int(tk.Tk().winfo_screenwidth() / 15)
    pTimeText = time.strftime("%p")
    pTimeFont = pygame.font.Font("ttf\Roboto-BoldItalic.ttf", pTimeSize)
    pTime = pTimeFont.render(pTimeText, True, black, white)
    pTimeRect = pTime.get_rect()

    classNameSize = int(tk.Tk().winfo_screenwidth() / 15)
    classNameFont = pygame.font.Font("ttf\方正宋刻本秀楷简体.ttf", classNameSize)
    className = classNameFont.render("科目：" + classNameText.get(), True, black, white)
    classNameRect = className.get_rect()

    classTimeSize = int(tk.Tk().winfo_screenwidth() / 15)
    classTimeFont = pygame.font.Font("ttf\方正宋刻本秀楷简体.ttf", classTimeSize)
    classTime = classTimeFont.render("时间：" + classTimeText.strftime("%H:%M:%S"), True, black, white)
    classTimeRect = classTime.get_rect()

    countdownSize = int(tk.Tk().winfo_screenwidth() / 15)
    countdownText = Countdown().strftime("%H:%M:%S")
    countdownFont = pygame.font.Font("ttf\方正宋刻本秀楷简体.ttf", countdownSize)
    countdown = countdownFont.render(countdownText, True, black, white)
    countdownRect = countdown.get_rect()

    xSize = int(25)
    xText = "×"
    xFont = pygame.font.Font("ttf\方正宋刻本秀楷简体.ttf", xSize)
    x = xFont.render(xText, True, black, white)
    xRect = x.get_rect()

    update()

    pygame.display.set_caption("计时器")
    pygame.mixer.init()

    start = True
    while start:
        nowTime = nowTimeFont.render(nowTimeText, True, black, white)
        pTimeText = time.strftime("%p")
        pTime = pTimeFont.render(pTimeText, True, black, white)
        current_date = datetime.datetime.strptime(datetime.datetime.now().strftime("%Y-%m-%d"), '%Y-%m-%d')
        countdown_date = datetime.datetime.strptime(Countdown().strftime("%Y-%m-%d"), '%Y-%m-%d')
        if Countdown().strftime("%H:%M:%S") == "00:00:00":
            if not sound_played:
                threading.Thread(target=play_sound).start()
            sound_played = True
        if current_date > countdown_date and countdown_date != datetime.datetime(1900, 1, 1, 0, 0):
            countdownText = "计时：00:00:00"
            countdown = countdownFont.render(countdownText, True, red, white)
            titleSize = int(tk.Tk().winfo_screenwidth() / scale_input(4))
            titleFont = pygame.font.Font("ttf\方正宋刻本秀楷简体.ttf", titleSize)
            title = titleFont.render("  考试结束", True, black, white)
            update()
        else:
            countdownText = "计时：" + Countdown().strftime("%H:%M:%S")
            countdown = countdownFont.render(countdownText, True, black, white)
        if time.strftime("%H") == '00':
            nowTimeText = datetime.datetime.now().strftime("00:%M:%S")
        else:
            nowTimeText = datetime.datetime.now().strftime("%I:%M:%S")
        update()
        time.sleep(0.1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                start = False
                menu.wm_deiconify()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if xRect.collidepoint(event.pos):
                    pygame.quit()
                    start = False
                    menu.wm_deiconify()

def on_closing():
    save_settings()
    menu.deiconify()
    menu.destroy()
    sys.exit()

def run_pygame():
    menu.withdraw()
    start_pygame_window()

if __name__ == "__main__":
    menu = tk.Tk()
    menu.protocol("WM_DELETE_WINDOW", on_closing)

    titleText = tk.StringVar()
    titleText.set("严肃考风考纪")
    titleText.trace_add("write", lambda *args: titleText.set(titleText.get()[:14]))
    classNameText = tk.StringVar()
    classNameText.set("语文")
    TimeText = tk.StringVar()
    TimeText.set("02:30:00")
    startText = tk.StringVar()

    now = datetime.datetime.now()
    rounded_minute = (now.minute // 5 + 1) * 5
    rounded_time = now.replace(minute=0, second=0) + datetime.timedelta(minutes=rounded_minute)
    target_timezone = pytz.timezone("Asia/Shanghai")
    rounded_time = rounded_time.astimezone(target_timezone)
    rounded_time_str = rounded_time.strftime("%H:%M:%S")
    startText.set(rounded_time_str)


    menu.title('考试计时器')
    try:
        menu.iconbitmap("ico\ico.ico")
    except:
        pass
    #menu.geometry('270x150')
    menu.resizable(0, 0)
    titlel = tk.Label(menu, text='标题：')
    titlee = tk.Entry(menu, textvariable=titleText, width=25)
    classNamel = tk.Label(menu, text='科目：')
    classNamec = ttk.Combobox(menu, textvariable=classNameText, value=('语文', '数学', '英语', '物理', '化学', '生物'), width=22)
    classTimel = tk.Label(menu, text='时间：')
    classTimee = tk.Entry(menu, textvariable=TimeText, width=25)
    startTimel = tk.Label(menu, text='开始时间：')
    startTimee = tk.Entry(menu, textvariable=startText, width=25)

    titlel.grid(row=0, column=0)
    titlee.grid(row=0, column=1)
    classNamel.grid(row=1, column=0)
    classNamec.grid(row=1, column=1)
    classTimel.grid(row=2, column=0)
    classTimee.grid(row=2, column=1)
    startTimel.grid(row=3, column=0)
    startTimee.grid(row=3, column=1)

    start_button = tk.Button(menu, text="开始", command=lambda: threading.Thread(target=run_pygame).start())
    start_button.grid(row=4, columnspan=2)

    load_settings()
    threading.Thread(target=check_start_time).start()
    menu.mainloop()

