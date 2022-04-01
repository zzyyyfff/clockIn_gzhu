import os
import time

import selenium.webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def wd_login(xuhao, mima):
    options = Options()
    optionsList = [
        "--headless", "--disable-gpu", "--window-size=1920,1200",
        "--ignore-certificate-errors", "--disable-extensions", "--no-sandbox",
        "--disable-dev-shm-usage"
    ]

    for option in optionsList:
        options.add_argument(option)

    options.page_load_strategy = 'eager'
    options.add_experimental_option("excludeSwitches", ['enable-logging'])

    driver = selenium.webdriver.Chrome(service=Service(
        ChromeDriverManager().install()),
                                       options=options)

    # pageName用来表示当前页面标题
    # 0表示初始状态
    # 1表示Unified Identity Authentication或者统一身份认证
    # 2表示融合门户
    # 3表示学生健康状况申报
    # 4表示其它
    pageName = 0

    # notification表示是否需要邮件通知打卡失败
    # 0表示不需要，1表示需要
    notification = 0

    for i in range(20):
        if i != 0:
            driver.refresh()

            try:
                WebDriverWait(driver, 10, 0.5).until(
                    ec.presence_of_all_elements_located((By.XPATH, "//title")))
            except:
                pass

            title = driver.title
            if title in ['Unified Identity Authentication', '统一身份认证']:
                pageName = 1
            elif title == '融合门户':
                pageName = 2
            elif title == '学生健康状况申报':
                pageName = 3
            else:
                pageName = 4

        if pageName in [0, 1]:
            try:
                driver.get(
                    f'https://newcas.gzhu.edu.cn/cas/login?service=https%3A%2F%2Fnewmy.gzhu.edu.cn%2Fup%2Fview%3Fm%3Dup'
                )

                try:
                    # 智能等待
                    WebDriverWait(driver, 30, 0.5).until(
                        ec.visibility_of_element_located(
                            (By.XPATH,
                             "//div[@class='robot-mag-win small-big-small']")))
                except:
                    pass

                driver.find_element(By.ID, 'un').send_keys(xuhao)
                driver.find_element(By.ID, 'pd').send_keys(mima)
                driver.find_element(By.ID, 'index_login_btn').click()

                try:
                    WebDriverWait(driver, 10, 0.5).until(
                        ec.presence_of_all_elements_located(
                            (By.XPATH, "//title")))
                except:
                    pass

                title = driver.title
                if title == '融合门户':
                    print('登录融合门户成功！')
                # 如果不在融合门户，就只可能是在登陆页面
                else:
                    print('登录融合门户失败！')
                    print('请检查学号与密码是否输入正确')

                    notification = 1

                    break

            except Exception as e:
                print(e)
                print(f"第{i+1}次运行失败！")

                # i == 19代表最后一次循环，如果这次循环仍然异常，则
                if i == 19:
                    notification = 1

                continue

        if pageName in [0, 1, 2]:
            try:
                WebDriverWait(driver, 30, 0.5).until(
                    ec.visibility_of_element_located(
                        (By.XPATH, '//a[@title="健康打卡"]/img')))
            except:
                pass

            driver.get('https://yqtb.gzhu.edu.cn/infoplus/form/XNYQSB/start')

        if pageName in [0, 1, 2, 3]:
            try:
                try:
                    WebDriverWait(driver, 30, 0.5).until(
                        ec.element_attribute_to_include(
                            (By.XPATH, "//div[@id='div_loader']"),
                            "display: none;"))
                except:
                    pass

                time.sleep(5)

                startButton = driver.find_element(
                    By.XPATH, "//a[contains(text(), '开始上报')]")
                ActionChains(driver).move_to_element(
                    startButton).click().perform()

                print('正在登录打卡开始界面')

            except Exception as e:
                print(e)
                print(f"第{i+1}次运行失败！")

                # i == 19代表最后一次循环，如果这次循环仍然异常，则
                if i == 19:
                    notification = 1

                continue

        if pageName in [0, 1, 2, 3, 4]:
            try:
                try:
                    WebDriverWait(driver, 30, 0.5).until(
                        ec.element_attribute_to_include(
                            (By.XPATH, "//div[@id='div_loader']"),
                            "display: none;"))
                except:
                    pass

                lastbutton = driver.find_element(
                    By.XPATH, "//div[@align='right']/input[@type='checkbox']")
                ActionChains(driver).move_to_element(
                    lastbutton).click().perform()

                driver.find_element(
                    By.XPATH, "//nobr[contains(text(), '提交')]/..").click()

                try:
                    WebDriverWait(driver, 10, 0.5).until(
                        ec.element_to_be_clickable(
                            By.XPATH,
                            "//button[@class='dialog_button default fr']"))
                except:
                    pass

                driver.find_element(
                    By.XPATH,
                    "//button[@class='dialog_button default fr']").click()

                # 等待页面滑动
                time.sleep(10)

                formErrorContentList = driver.find_elements(
                    By.XPATH, "//div[@class='line10']")

                for formErrorContent in formErrorContentList:
                    button = driver.find_elements(
                        locate_with(By.XPATH, "//input[@type='radio']").below(
                            formErrorContent))[0]
                    ActionChains(driver).move_to_element(
                        button).click().perform()

                driver.find_element(
                    By.XPATH, "//nobr[contains(text(), '提交')]/..").click()

                print('表单提交成功')

                # 提交表单之后显示的打卡成功信息选择不了，不论是用XPATH还是js
                # 所以用了time
                time.sleep(30)

                print('打卡程序运行结束')

                break

            except Exception as e:
                print(e)
                print(f"第{i+1}次运行失败！")

                # i == 19代表最后一次循环，如果这次循环仍然异常，则
                if i == 19:
                    notification = 1

                continue

    driver.quit()

    if notification == 1:
        print('打卡失败，尝试抛出异常，以便github邮件通知打卡失败')

        a = '12'
        a.append(a)


if __name__ == "__main__":
    xuhao = str(os.environ['XUHAO'])
    mima = str(os.environ['MIMA'])

    wd_login(xuhao, mima)
