from vision import find_template
from test_ocr import capture_screenshot
from act import tap
import time

# 1. 截屏
path = capture_screenshot()

# 2. 找"地图路线总览"按钮
matches = find_template(path, "templates/地图路线总览.png")

if matches:
    m = matches[0]
    print(f"找到按钮，坐标: ({m['x']}, {m['y']})，置信度: {m['confidence']:.2f}")

    # 3. 点它
    print("3 秒后点击...")
    time.sleep(3)
    tap(m["x"], m["y"])
else:
    print("没找到按钮。")