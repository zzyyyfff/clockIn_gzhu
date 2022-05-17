import os
import time

import selenium.webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def launch_webdriver():
    options = Options()
    optionsList = [
        "--headless", "--enable-javascript", "start-maximized",
        "--disable-gpu", "--disable-extensions", "--no-sandbox",
        "--disable-browser-side-navigation", "--disable-dev-shm-usage"
    ]

    for option in optionsList:
        options.add_argument(option)

    options.page_load_strategy = 'eager'
    options.add_experimental_option(
        "excludeSwitches", ["ignore-certificate-errors", "enable-automation"])

    driver = selenium.webdriver.Chrome(service=Service(
        ChromeDriverManager().install()),
                                       options=options)

    return driver


def wd_login(xuhao, mima):
    driver = launch_webdriver()

    wdwait = WebDriverWait(driver, 30)

    # pageName用来表示当前页面标题
    # 0表示初始页面，Unified Identity Authentication页面，统一身份认证页面和其它页面
    pageName = 0

    # notification表示是否需要邮件通知打卡失败
    # 0表示不需要，1表示需要
    notification = 0

    for retries in range(10):
        try:
            if retries:
                print('刷新页面')

                driver.refresh()

                title = driver.title
                if title == '融合门户':
                    pageName = 1
                elif title == '学生健康状况申报':
                    pageName = 2
                elif title in ['填报健康信息 - 学生健康状况申报', '表单填写与审批::加载中']:
                    pageName = 3
                else:
                    pageName = 0

                print(f'当前页面标题为：{title}')

            if pageName == 0:
                print('正在转到统一身份认证页面')

                driver.get(
                    f'https://newcas.gzhu.edu.cn/cas/login?service=https%3A%2F%2Fnewmy.gzhu.edu.cn%2Fup%2Fview%3Fm%3Dup'
                )

                try:
                    wdwait.until(
                        EC.visibility_of_element_located(
                            (By.XPATH,
                             "//div[@class='robot-mag-win small-big-small']")))

                except TimeoutException:
                    pass

                print('正在尝试登陆融合门户')

                for script in [
                        f"document.getElementById('un').value='{xuhao}'",
                        f"document.getElementById('pd').value='{mima}'",
                        "document.getElementById('index_login_btn').click()"
                ]:
                    driver.execute_script(script)

            if pageName in [0, 1]:
                try:
                    wdwait.until(
                        EC.visibility_of_element_located(
                            (By.XPATH, '//a[@title="健康打卡"]/img')))

                except TimeoutException:
                    pass

                print('正在转到学生健康状况申报页面')

                driver.get(
                    'https://yqtb.gzhu.edu.cn/infoplus/form/XNYQSB/start')

            if pageName in [0, 1, 2]:
                try:
                    wdwait.until(
                        EC.element_attribute_to_include(
                            (By.XPATH, "//div[@id='div_loader']"),
                            "display: none;"))

                except TimeoutException:
                    pass

                wdwait.until(
                    EC.element_to_be_clickable(
                        (By.ID, "preview_start_button"))).click()

                print('正在转到填报健康信息 - 学生健康状况申报页面')

            if pageName in [0, 1, 2, 3]:
                try:
                    wdwait.until(
                        EC.element_attribute_to_include(
                            (By.XPATH, "//div[@id='div_loader']"),
                            "display: none;"))

                except TimeoutException:
                    pass

                print('开始填表')

                for xpath in [
                        "//div[@align='right']/input[@type='checkbox']",
                        "//nobr[contains(text(), '提交')]/.."
                ]:
                    driver.find_element(By.XPATH, xpath).click()

                wdwait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH,
                         "//button[@class='dialog_button default fr']"
                         ))).click()

                # 等待页面滑动
                time.sleep(10)

                formErrorContentList = driver.find_elements(
                    By.XPATH, "//div[@class='line10']")

                for formErrorContent in formErrorContentList:
                    driver.find_elements(
                        locate_with(By.XPATH, "//input[@type='radio']").below(
                            formErrorContent))[0].click()

                print('尝试提交表单')

                driver.find_element(
                    By.XPATH, "//nobr[contains(text(), '提交')]/..").click()

                time.sleep(30)

                message = driver.execute_script(
                    "return document.getElementsByClassName('form_do_action_error')[0]['textContent']"
                )
                print(message)

                if message == '打卡成功':
                    print('打卡程序运行结束')

                    break

                else:
                    print('重新进行打卡')

        except Exception as e:
            print(e)
            print(f"第{retries+1}次运行失败！\n")

            # retries == 9代表最后一次循环，如果这次循环仍然异常，则
            if retries == 9:
                notification = 1

    driver.quit()

    if notification == 1:
        print('打卡失败，尝试抛出异常，以便github邮件通知打卡失败')

        a = '12'
        a.append(a)


if __name__ == "__main__":
    xuhao = str(os.environ['XUHAO'])
    mima = str(os.environ['MIMA'])

    wd_login(xuhao, mima)
