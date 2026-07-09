import subprocess
import easyocr
import time

ADB = r"C:\platform-tools\platform-tools\adb.exe"
DEVICE = "127.0.0.1:7555"


# ============================================================
# 第 1 步：ADB 截图
# ============================================================
def capture_screenshot(output_path="czn_screenshot.png"):
    """通过 ADB 从 MuMu 截取当前游戏画面"""
    subprocess.run(
        [ADB, "-s", DEVICE, "shell", "screencap", "-p", "/sdcard/czn_temp.png"],
        capture_output=True,
    )
    subprocess.run(
        [ADB, "-s", DEVICE, "pull", "/sdcard/czn_temp.png", output_path],
        capture_output=True,
    )
    return output_path


# ============================================================
# 第 2 步：OCR 识别文字
# ============================================================
# 只初始化一次（全局复用，不用每次截图都重新加载模型）
reader = easyocr.Reader(["ch_sim", "en"], gpu=True)


def extract_text(image_path):
    """从截图中提取所有文字"""
    result = reader.readtext(image_path)
    texts = []
    for bbox, text_content, confidence in result:
        if confidence > 0.5:  # 只保留置信度 > 50% 的结果
            texts.append(
                {
                    "text": text_content,
                    "confidence": confidence,
                    "position": bbox,  # 文字在图片中的位置
                }
            )
    return texts


# ============================================================
# 第 3 步：主流程
# ============================================================
if __name__ == "__main__":
    # 确保 MuMu 已连接
    result = subprocess.run([ADB, "devices"], capture_output=True, text=True)
    if DEVICE not in result.stdout:
        subprocess.run([ADB, "connect", DEVICE], capture_output=True)

    print("正在截图...")
    path = capture_screenshot()

    print("正在识别文字...")
    texts = extract_text(path)

    print(f"\n识别到 {len(texts)} 条文字：\n")
    for item in texts:
        print(f"  [{item['confidence']:.2f}] {item['text']}")