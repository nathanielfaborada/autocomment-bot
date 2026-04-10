import asyncio
import os
import random

from dotenv import load_dotenv
from pyppeteer import launch

load_dotenv()


class Account:
    def __init__(self, email, password, media_platform) -> None:
        self.email = email
        self.password = password
        self.media_platform = media_platform

class Application(Account):
    def __init__(self, email, password, media_platform):
        super().__init__(email, password, media_platform)

class Bot(Account):
    def __init__(self, email, password, media_platform) -> None:
        super().__init__(email, password, media_platform)
        self.automation_accounts = []
        self.messages = ["Hi, Goodmorning", "Good day!", "Hello"]

    def add_automation_account(self, account):
        self.automation_accounts.append(account)

    async def run(self):
        browser = await launch(executablePath=executable_chromium, headless=False)
        page = await browser.newPage()
        await page.goto(self.media_platform, timeout=60000)

        await page.type('#email', self.email)
        await page.type('#pass', self.password)
        await page.click('button[name="login"]')
        await page.waitForNavigation(timeout=60000)
        await page.goto('https://www.facebook.com/61561184012011/posts/122116752578372800/')

        for _ in range(1):
            try:
                self.first_message = ['Hi', 'Hello', 'Good']
                self.second_message = ['Musta', 'Galing', 'Ikaw']

                fi_message = random.choice(self.first_message)
                sec_message = random.choice(self.second_message)
                combine = [fi_message, sec_message]
                generated_message = ', '.join(combine)

                await page.waitForSelector('div[aria-label="Leave a comment"]')
                await page.click('div[aria-label="Leave a comment"]')
                await page.type('div[aria-placeholder="Write a comment…"]', f"{generated_message} Have a great day, and don't forget to trust yourself.")
                await page.keyboard.press('Enter')
                await asyncio.sleep(5)
                await page.reload()
            except Exception as e:
                print(f"Error: {e}")
                break
        await browser.close()

if __name__ == "__main__":
    executable_chromium = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
    media_platform = 'https://www.facebook.com/'

    account1 = Bot(os.getenv('ACCOUNT1_EMAIL'), os.getenv('ACCOUNT1_PASSWORD'), media_platform)
    account1.add_automation_account(account1)

    account2 = Bot(os.getenv('ACCOUNT2_EMAIL'), os.getenv('ACCOUNT2_PASSWORD'), media_platform)
    account2.add_automation_account(account2)

    account3 = Bot(os.getenv('ACCOUNT3_EMAIL'), os.getenv('ACCOUNT3_PASSWORD'), media_platform)
    account3.add_automation_account(account3)

    account4 = Bot(os.getenv('ACCOUNT4_EMAIL'), os.getenv('ACCOUNT4_PASSWORD'), media_platform)
    account4.add_automation_account(account4)

    # Run the bot for each account
    loop = asyncio.get_event_loop()
    loop.run_until_complete(account1.run())
    loop.run_until_complete(account2.run())
    loop.run_until_complete(account3.run())
    loop.run_until_complete(account4.run())
