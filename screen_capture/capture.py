import mss
import mss.tools
import base64
from PIL import Image
import io

class ScreenEngine:
    def __init__(self):
        self.sct = mss.mss()

    def capture_screenshot_as_base64(self) -> str:
        # Capture the primary monitor
        monitor = self.sct.monitors[1]
        sct_img = self.sct.grab(monitor)
        
        # Convert raw screen capture to PNG bytes
        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
        
        # Resize to 1024x1024 max bound to prevent overloading local VRAM during vision processing
        img.thumbnail((1024, 1024))
        
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode('utf-8')