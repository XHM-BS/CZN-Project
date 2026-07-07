import subprocess
import os

ADB = r"C:\platform-tools\platform-tools\adb.exe"
DEVICE = "127.0.0.1:7555"


def capture(output_path: str = "czn_screenshot.png") -> str:
    """通过 ADB 从 MuMu 模拟器截取 CZN 游戏画面。

    - 从安卓系统内部截图（绕过 Windows 渲染层）
    - 拉到本地项目目录
    """

    # 1. 安卓内部截图
    subprocess.run(
        [ADB, "-s", DEVICE, "shell", "screencap", "-p", "/sdcard/czn_screenshot.png"],
        capture_output=True,
    )

    # 2. 拉到本地
    subprocess.run(
        [ADB, "-s", DEVICE, "pull", "/sdcard/czn_screenshot.png", output_path],
        capture_output=True,
    )

    print(f"截图已保存：{output_path}")
    return output_path


if __name__ == "__main__":
    # 确保 MuMu 已连接
    result = subprocess.run(
        [ADB, "devices"], capture_output=True, text=True
    )
    if DEVICE not in result.stdout:
        subprocess.run([ADB, "connect", DEVICE], capture_output=True)
        print(f"已连接 {DEVICE}")

    capture()