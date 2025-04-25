from playwright.sync_api import sync_playwright, expect, Page
from playwright_utils import *
from simple_salesforce import Salesforce  
import config
from datetime import datetime
import os
import shutil
import time
import pytest
import pytest
from playwright.sync_api import sync_playwright, Page
from salesforce_utils import *

# "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --remote-debugging-address=127.0.0.1 --no-first-run --user-data-dir="C:\Temp\ChromeDebugProfile"

# set PWDEBUG=1 && python "D:\vs code\Sculptor\current page.py"

# Авторизация в Salesforce API
sf = Salesforce(username=config.LOGIN, password=config.PASSWORD, security_token=config.SECURITY_TOKEN)

# Основная функция
def run_current_tasks(unique_number: int = 33):
    with sync_playwright() as p:
        # Подключаемся к открытому браузеру через CDP
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]  # Используем первый контекст
        page = context.pages[0]  # Берем первую открытую вкладку



# Запуск
if __name__ == "__main__":
    unique_number = 33 
    run_current_tasks(unique_number)

