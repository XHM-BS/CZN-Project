import cv2
import numpy as np
from test_ocr import capture_screenshot


def _imread_unicode(path):
    """读取图片，兼容中文文件名"""
    with open(path, "rb") as f:
        data = np.frombuffer(f.read(), np.uint8)
    return cv2.imdecode(data, cv2.IMREAD_COLOR)


def find_template(screenshot_path, template_path, threshold=0.8):
    """在截图中找到模板图片的位置（多尺度匹配），返回中心坐标列表"""
    screenshot = _imread_unicode(screenshot_path)
    template = _imread_unicode(template_path)

    if screenshot is None:
        raise FileNotFoundError(f"找不到截图: {screenshot_path}")
    if template is None:
        raise FileNotFoundError(f"找不到模板: {template_path}")

    h, w = template.shape[:2]
    matches = []

    for scale in [0.5, 0.75, 1.0, 1.25, 1.5]:
        scaled_w = int(w * scale)
        scaled_h = int(h * scale)
        if scaled_w > screenshot.shape[1] or scaled_h > screenshot.shape[0]:
            continue
        scaled_t = cv2.resize(template, (scaled_w, scaled_h))
        result = cv2.matchTemplate(screenshot, scaled_t, cv2.TM_CCOEFF_NORMED)
        locations = np.where(result >= threshold)
        for pt in zip(*locations[::-1]):
            matches.append({
                "x": int(pt[0] + scaled_w / 2),
                "y": int(pt[1] + scaled_h / 2),
                "confidence": float(result[pt[1], pt[0]]),
                "scale": scale,
            })
    return matches


# ============================================================
# 测试
# ============================================================
if __name__ == "__main__":
    import os

    # 用最新的 ADB 截图
    screenshot_path = capture_screenshot()
    print(f"截图: {screenshot_path}\n")

    # 测试 templates 目录下所有模板
    template_dir = "templates"
    for filename in os.listdir(template_dir):
        template_path = os.path.join(template_dir, filename)
        print(f"模板: {filename}")
        matches = find_template(screenshot_path, template_path, threshold=0.8)

        if matches:
            # 按置信度排序，取最高
            matches.sort(key=lambda m: m["confidence"], reverse=True)
            best = matches[0]
            print(f"  找到! 坐标: ({best['x']}, {best['y']}), 置信度: {best['confidence']:.2f}, 缩放: {best['scale']:.2f}")
        else:
            print(f"  没找到匹配 (可能是按钮不在当前画面或 threshold 太高)")
        print()