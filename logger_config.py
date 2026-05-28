# logger_config.py
import logging

# تنظیمات لاگر
logging.basicConfig(
    level=logging.INFO, # می‌توانی روی DEBUG هم بگذاری
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler("game.log"), # ذخیره در فایل
        logging.StreamHandler()           # نمایش در کنسول
    ]
)

def get_logger(name):
    return logging.getLogger(name)
