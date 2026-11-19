from helpers.config import get_settings, Settings  # pyright: ignore[reportMissingImports]
import os  # pyright: ignore[reportMissingImports]
import random  # pyright: ignore[reportMissingImports]
import string  # pyright: ignore[reportMissingImports]  
import re  # pyright: ignore[reportMissingImports]

class BaseController:
    def __init__(self):
        self.app_settings = get_settings()
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.file_dir = os.path.join(self.base_dir, "assets", "files")


    def generate_random_string(self, length: int = 8) -> str:
        # Generate a random string of specified length
        letters = string.ascii_letters + string.digits
        return ''.join(random.choice(letters) for _ in range(length))   
    


