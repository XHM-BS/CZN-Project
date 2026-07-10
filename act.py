import subprocess
import time

ADB = r"C:\platform-tools\platform-tools\adb.exe"
DEVICE = "127.0.0.1:7555"


def tap(x, y):
    """通过 ADB 点击 MuMu 模拟器里的坐标"""
    subprocess.run(
        [ADB, "-s", DEVICE, "shell", "input", "tap", str(x), str(y)],
        capture_output=True,
    )
    print(f"点击：({x}, {y})")


def swipe(x1, y1, x2, y2, duration=500):
    """从 (x1,y1) 拖拽到 (x2,y2)，duration 是持续时间（毫秒）"""
    subprocess.run(
        [
            ADB, "-s", DEVICE, "shell", "input", "swipe",
            str(x1), str(y1), str(x2), str(y2), str(duration),
        ],
        capture_output=True,
    )
    print(f"拖拽：({x1},{y1}) → ({x2},{y2})，持续 {duration}ms")


# ============================================================
# 测试：点击 vision.py 找到的"地图路线总览"按钮
# ============================================================
if __name__ == "__main__":
    print('3 秒后点击"地图路线总览"按钮...')
    time.sleep(3)

    # 用 vision.py 找到的坐标
    tap(762, 709)

    print("点完了！看看游戏有没有反应。")