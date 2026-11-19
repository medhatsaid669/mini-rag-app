from helpers.config import get_settings, Settings  # pyright: ignore[reportMissingImports]

class BaseController:
    def __init__(self):
        self.app_settings = get_settings()
        self.size_scale = 1048576  # 1 MB in bytes 1024x1024
