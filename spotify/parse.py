from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import selenium.common.exceptions as ex
import time
from spotify.extendtions import db
from spotify.models import Order
from dateutil import relativedelta




def get(email,password,link):

    option = webdriver.ChromeOptions()
    option.add_argument('--no-sandbox')
    # option.add_argument('--headless')
    option.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
    option.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
    option.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
    driver = webdriver.Chrome(chrome_options=option)
    driver.delete_all_cookies()
    order=Order(email=email,password=password,link=link)
    db.session.add(order)
    db.session.commit()
    # 登录
    driver.get('https://accounts.spotify.com/en/login')
    inputs=driver.find_elements_by_tag_name('input')
    inputs[0].send_keys(email)
    inputs[1].send_keys(password)
    log_in_btn=driver.find_element_by_id('login-button')
    log_in_btn.click()

    driver.get('https://www.spotify.com/hk-en/account/overview/')
    driver.get('https://www.spotify.com/hk-en/account/overview/')

    # 检查地区
    try:
        usa = WebDriverWait(driver,8, 0.5).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[4]/div/div[2]/div[3]/div[2]/div/article[1]/section/table/tbody/tr[4]/td[2]"))
        )
    except ex.TimeoutException as e:

        order.status='密码错误'
        db.session.commit()
        return None
    if usa.text=='USA':
        share(driver,link,order)
    else:
        try:
            country = WebDriverWait(driver,12, 0.5).until(
                EC.presence_of_element_located(
                    (By.ID, 'country'))
            )
        except ex.TimeoutException:
            order.status = '时间超时'
            db.session.commit()
            return None
        Select(country).select_by_value('US')

        try:
            edit_profile_btn=WebDriverWait(driver,12,0.5).until(
                EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/div[4]/div/div[2]/div[2]/div[2]/div/article/section/form/div/button'))
            )
            edit_profile_btn.click()
        except ex.TimeoutException as e:
            order.status = '时间超时'
            db.session.commit()
            return None
        share(driver,link,order)



def share(driver,link,order):

    driver.get(link.infos)
    link_split = link.infos.split('/')
    token = link_split[-1]
    if len(token) < 1:
        token = link_split[-2]
    link_address = 'https://www.spotify.com/us/family/join/address/' + token + '/'

    try:
        driver.get(link_address)
        address_input = WebDriverWait(driver, 8, 0.5).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/form/main/div/section/div/div[2]/input'))
        )
        address_input.send_keys('1')
        find_adress = driver.find_element_by_xpath('/html/body/div[2]/form/main/div/div/button')
        find_adress.click()
        confirm_btn = WebDriverWait(driver, 12, 0.5).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div/footer/button[2]'))
        )
        confirm_btn.click()
        time.sleep(1)
        if driver.current_url == link_address:
            order.status = '链接失效'
            db.session.delete(link)
            db.session.commit()
            return None
        else:
            order.status = '处理成功'
            link.times-=1
            order.expiretime+=relativedelta(years=1)
            db.session.add(order)
            db.session.commit()
    except ex.TimeoutException:
        order.status='时间超时'
        db.session.commit()












