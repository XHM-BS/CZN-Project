import easyocr

# 初始化（中文模型，首次运行会自动下载）
ocr = easyocr.Reader(['ch_sim', 'en'], gpu=True)

# 读你最新的 ADB 截图
result = ocr.readtext("czn_screenshot.png")

# 打印识别到的所有文字
if result:
    for detection in result:
        bbox, text, confidence = detection
        print(f"[{confidence:.2f}] {text}")
else:
    print("没识别到文字。试着截一张有文字的页面。")