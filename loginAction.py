from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import re
import os
import requests
from pynput.keyboard import Key, Listener,Controller

downLoadPath= 'D:\\'
username='18697265816'
password='5816@smartEDU'
loginUrl='https://auth.smartedu.cn/uias/login'

#文件下载函数
def pdfDownloader(url,filenameEle):
    #删除文件名乱码
    filenameEle = re.sub(r'[^\x00-\x7F]+', '', filenameEle)
    try:
    # 发送 HTTP 请求并获取文件内容
        response = requests.get(url)

        # 检查请求是否成功
        if response.status_code == 200:
            # 获取文件名
            file_name = filenameEle+os.path.basename(url)
            # 构建文件保存路径（D 盘根目录）
            save_path = os.path.join(downLoadPath, file_name)
            # 保存文件
            with open(save_path, 'wb') as file:
                file.write(response.content)
            print(f"文件已成功下载到 {save_path}")
        else:
            print("下载失败，状态码:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("发生错误:", e)


# 创建浏览器驱动对象
driver = webdriver.Chrome()  # 请确保已安装 Chrome 浏览器和对应的 ChromeDriver

# 打开登录页面
driver.get(loginUrl)

# 输入用户名和密码
username_input = driver.find_element(By.ID, 'username')  # 根据实际的用户名输入框 ID 进行修改
username_input.send_keys(username)  # 替换为您的用户名

password_input = driver.find_element(By.ID, 'tmpPassword')  # 根据实际的密码输入框 ID 进行修改
password_input.send_keys(password)  # 替换为您的密码

# 找到 agreementCheckbox 元素并点击
agreement_checkbox = driver.find_element(By.ID, 'agreementCheckbox')  # 根据实际的元素 ID 进行修改
agreement_checkbox.click()

# 检测 Ctrl + E 快捷键
keyboard = Controller()

def on_press(key):
    if hasattr(key, 'char') and key.char == 'p':
        # 使用 active_element 属性获取当前具有焦点的元素
        driver.switch_to.window(driver.window_handles[-1])

        print("快捷键被按下，当前页面 URL: ", driver.current_url)
        #获取下载连接目标                
        try:
            element = driver.find_element(By.ID, 'pdfPlayerFirefox')
            filenameEle = driver.find_element(By.CLASS_NAME,'index-module_title_bnE9V').text
            match = re.search(r'file=(.*?\.pdf)', element.get_attribute('src'))
            if match:
                new_rul= match.group(1)
                new_url = new_rul.replace('-private', '')
                print("匹配的下载目标为：",new_url)
                pdfDownloader(new_url,filenameEle)
            else:
                print("未找到匹配的内容")
        except Exception:
            print("未找到具有 'pdfPlayerFirefox' ID 的元素")
    elif not hasattr(key, 'char'):
        # 处理非字母按键的操作
        pass

with Listener(on_press=on_press) as listener:
    listener.join()

# 登录完成，浏览器保持打开状态，程序不退出
while True:
    time.sleep(3600)  # 每小时循环一次，防止程序退出