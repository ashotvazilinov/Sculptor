from playwright.sync_api import sync_playwright, expect, Page
from playwright_utils import *
from simple_salesforce import Salesforce  
from html_elements import *
import config
from datetime import datetime
import os
import shutil
import time
import pytest
from playwright.sync_api import sync_playwright, Page
from salesforce_utils import *

# "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --remote-debugging-address=127.0.0.1 --no-first-run --user-data-dir="C:\Temp\ChromeDebugProfile"

# set PWDEBUG=1 && python "D:\vs code\Sculptor\current page.py"

# Automation in Salesforce API
sf = Salesforce(username=config.LOGIN, password=config.PASSWORD, security_token=config.SECURITY_TOKEN, domain=config.DOMAIN)

# Main function
def run_current_tasks(unique_number: int = 33):
    with sync_playwright() as p:
                # Connect to the existing browser instance
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]  # Using the first context
        page = context.pages[0]  # Taking the first tab
        '''write here'''

        old_count = len(page.query_selector_all("//*[contains(text(), 'Пост удалён')]"))
        print(f"Начальное количество: {old_count}")
        page.wait_for_selector(f"(//button[contains(@class, 'vkuiIconButton__host')])[{4}]", timeout=5000).hover()
        page.wait_for_selector("//span[contains(text(), 'Удалить')]", timeout=5000).click()
        print("Удаление выполнено")

        x = 0
        y = 0
        while True:  # Бесконечный цикл
            print(f"=== Постов удалено {y} ===")
            y = y + 1
            if x == 7:
                print("Обновление страницы...")
                page.reload()
                time.sleep(2)
                page.wait_for_selector(f"(//button[contains(@class, 'vkuiIconButton__host')])[{4}]", timeout=5000).hover()

                print("Страница обновлена, продолжаем...")
                x = 0
                page.evaluate("window.scrollBy(0, 3)") 
                print(f'теперь x = {x}')
                old_count = len(page.query_selector_all("//*[contains(text(), 'Пост удалён')]"))

                continue
            
            while x > 0:
                new_count = len(page.query_selector_all("//*[contains(text(), 'Пост удалён')]"))
                
                if new_count == old_count + 1:
                    print(f"Новый пост обнаружен! {old_count} > {new_count}")
                    old_count = new_count
                    break
                else:
                    print(f"Ожидание... текущее: {new_count}, ожидаем: {old_count + 1}")
                    page.evaluate("window.scrollBy(0, 3)")                 

            # Выполняем удаление

            page.wait_for_selector(f"(//button[contains(@class, 'vkuiIconButton__host')])[4]", timeout=5000).hover()
            page.wait_for_selector("//span[contains(text(), 'Удалить')]", timeout=5000).click()
            print("Удаление выполнено")
            
            x += 1

# Start
if __name__ == "__main__":
    unique_number = 33 
    run_current_tasks(unique_number)