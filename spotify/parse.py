from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import selenium.common.exceptions as ex
import time
from spotify.extendtions import db
from spotify.models import Order
from dateutil.relativedelta import relativedelta
import datetime

def get(email, password, link):

    option = webdriver.ChromeOptions()
    option.add_argument('--no-sandbox')
    #option.add_argument('--headless')
    option.add_argument('--disable-gpu')
    option.add_argument('--hide-scrollbars')
    option.add_argument('blink-settings=imagesEnabled=false')
    driver = webdriver.Chrome(chrome_options=option)
    driver.delete_all_cookies()
    order = Order(email=email, password=password, link=link)
    db.session.add(order)
    db.session.commit()

    #修改地区
    driver.get('https://www.spotify.com/us/account/profile/')
    #登录
    inputs = WebDriverWait(driver, 8, 0.5).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, 'input'))
    )
    inputs[0].send_keys(email)
    inputs[1].send_keys(password)
    log_in_btn = driver.find_element_by_id('login-button')
    log_in_btn.click()
    usa=WebDriverWait(driver,8,0.5).until(
        EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/div[4]/div/div[2]/div[2]/div[2]/div/article/section/form/section/div[5]/div[2]/select'))
    )
    Select(usa).select_by_value('US')
    save_btn=driver.find_element_by_xpath('/html/body/div[1]/div[4]/div/div[2]/div[2]/div[2]/div/article/section/form/div/button')
    save_btn.click()

    link_split = link.infos.split('/')
    token = link_split[-1]
    if len(token) < 1:
        token = link_split[-2]
    link_address = 'https://www.spotify.com/us/family/join/address/' + token + '/'
    driver.get(link_address)
    try:
        address_input = WebDriverWait(driver, 8, 0.5).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/form/main/div/section/div/div[2]/input'))
        )
    except ex.TimeoutException:
        order.status = '密码错误或已经被邀请'
        db.session.commit()
        driver.close()
        driver.quit()
        return None
    try:
        address_input.send_keys('1')
        find_adress = driver.find_element_by_xpath('/html/body/div[2]/form/main/div/div/button')
        find_adress.click()
        confirm_btn = WebDriverWait(driver, 3, 0.5).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div/footer/button[2]'))
        )
        confirm_btn.click()
    except ex.TimeoutException:
        order.status = '时间超时'
        db.session.commit()
        driver.close()
        driver.quit()
        return None

    time.sleep(3)
    if driver.current_url == link_address:
        order.status = '链接失效'
        db.session.delete(link)
        db.session.commit()
        driver.close()
        driver.quit()
        return None
    else:
        order.status = '处理成功'
        link.times -= 1
        order.expiretime = datetime.datetime.utcnow() + relativedelta(years=1)
        db.session.commit()
        driver.close()
        driver.quit()
        return None

