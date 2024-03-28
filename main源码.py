# -*- coding: utf-8 -*-#
import getpass
from playwright.sync_api import sync_playwright, expect
import time


# USER_DIR_PATH = f"C:\\Users\\{getpass.getuser()}\\AppData\Local\Google\Chrome\\User Data"
pwd_o = '51ChatGPT'


def get_config(user, pwd):
    # 重试三次
    i = 1
    while i <= 3:
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    # 设置 GUI 模式
                    headless=False,
                    slow_mo=500,
                )
                page = browser.new_page()
                # 清除缓存 cookie
                page.context.clear_cookies()
                page.goto("https://www.mail.com/", wait_until="domcontentloaded", timeout=60000)
                print(f'正在处理 账号：{user} 请稍等...')
                page.get_by_role("link", name="Log in").click()
                page.get_by_placeholder("Email address").click()
                page.get_by_placeholder("Email address").click(modifiers=["Control"])
                page.get_by_placeholder("Email address").fill(user)
                page.get_by_placeholder("Password").click(modifiers=["Control"])
                page.get_by_placeholder("Password").fill(pwd)
                page.get_by_role("button", name="Log in").click()
                time.sleep(10)
                page.frame_locator("[data-test=\"third-party-frame_home\"]").get_by_role("link",
                                                                                         name="Security Options").click()
                page.frame_locator("[data-test=\"third-party-frame_ciss\"]").get_by_role("link",
                                                                                         name="Change password").click()
                time.sleep(5)
                page.frame_locator("[data-test=\"third-party-frame_ciss\"]").locator(
                    'input[id="1:form:editPanel:currentPasswordPanel:topWrapper:inputWrapper:input"]').fill(
                    pwd)
                page.frame_locator("[data-test=\"third-party-frame_ciss\"]").get_by_label(
                    "Choose a new password:").fill(pwd_o)
                page.frame_locator("[data-test=\"third-party-frame_ciss\"]").get_by_label("Re-type new password:").fill(pwd_o)
                page.frame_locator("[data-test=\"third-party-frame_ciss\"]").get_by_role("button",
                                                                                         name="Save changes").click()
                time.sleep(3)
                with open('修改成功账号.txt', mode='a', encoding='utf-8') as f:
                    f.write(f'{user}----{pwd_o}\n')
                # 判断是否修改成功
                print(f'账号：{user}修改成功')
                page.close()
                return

        except:
            i += 1
    else:
        print(f'账号：{user}修改失败')
        with open('修改失败账号.txt', mode='a', encoding='utf-8') as f:
            f.write(f'{user}----{pwd}\n')
        page.close()
        return


if __name__ == '__main__':
    with open('账号.txt', mode='r', encoding='utf-8') as f:
        data = f.readlines()
        for i in data:
            i = i.strip()
            user = i.split('----')[0]
            pwd = i.split('----')[1]
            get_config(user, pwd)
