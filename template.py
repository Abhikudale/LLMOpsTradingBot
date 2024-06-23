import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO,format='[%(asctime)s]: %(message)s')

list_of_files = [
    "tradingbot/__init__.py",
    "tradingbot/helper.py",
    "tradingbot/prompt.py",
    ".env",
    "requirements.txt",
    "setup.py",
    "Research/test.ipynb",
    "app.py"]

for file in list_of_files:
    file_path=Path(file)
    
    file_dir, file_name=os.path.split(file_path)
    if file_dir != "":
        os.makedirs(file_dir, exist_ok=True)
        logging.info(f"Created directory {file_dir} for the files {file_name}")
    
    if (not os.path.exists(file_path) or (os.path.getsize(file_path) == 0)):
        with open(file_path, "w") as f:
            pass
            logging.info(f"Created empty file {file_path}")
    else:
        logging.info(f"{file_name} already exists")
