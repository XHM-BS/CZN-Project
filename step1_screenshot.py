import pyautogui
import time

print("3 秒后截图，请切换到游戏窗口...")
time.sleep(3)

img = pyautogui.screenshot()
img.save("first_screenshot.png")

print("搞定！CZN Project 文件夹里多了一张 first_screenshot.png")
