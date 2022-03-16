import time

from selenium import webdriver
from selenium.webdriver import ActionChains, DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


class WSJScraper:
    def __init__(self):
        self.wait_time = 50
        op = webdriver.ChromeOptions()
        op.add_argument("--window-size=1920,1080")
        op.add_argument('--no-sandbox')
        op.add_argument('--headless')
        op.add_argument('--disable-dev-shm-usage')
        op.add_argument('--ignore-certificate-errors')
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        op.add_argument(f'user-agent={user_agent}')
        caps = DesiredCapabilities().CHROME
        # caps["pageLoadStrategy"] = "normal"  # complete
        #caps["pageLoadStrategy"] = "eager"  #  interactive
        caps["pageLoadStrategy"] = "none"
        ser = Service(ChromeDriverManager().install())
        # ser = Service(executable_path='driver/chromedriver.exe')
        self.driver = webdriver.Chrome(desired_capabilities=caps, service=ser, options=op)
        self.url = None

    def login(self, url, username, password):
        self.driver.get(url)
        self.url = url
        sign_in_xpath = "(//*[contains(text(),'Sign In')])[1]"
        time.sleep(1)
        ActionChains(self.driver).move_by_offset(10, 20)
        ActionChains(self.driver).perform()
        driver = self.__find_element_and_click(sign_in_xpath, by=By.XPATH)
        email_xpath = "//*[@id='username']"
        button = WebDriverWait(self.driver, self.wait_time).until(
            expected_conditions.visibility_of_element_located((By.XPATH, email_xpath)))
        ActionChains(self.driver).move_to_element(button).click(button).perform()
        self.__find_element_and_send_key(email_xpath, username, by=By.XPATH)

        continue_button_xpath = "(//*[contains(text(),'Continue With Password')])[1]"
        self.__find_element_and_click(continue_button_xpath, by=By.XPATH)

        time.sleep(1)
        password_xpath = "//*[@id='password-login-password']"
        button = WebDriverWait(self.driver, self.wait_time).until(
            expected_conditions.visibility_of_element_located((By.XPATH, password_xpath)))
        ActionChains(driver).move_to_element(button).click(button).perform()
        self.__find_element_and_send_key(password_xpath, password, by=By.XPATH)

        time.sleep(1)
        sign_in_button_xpath = "//*[@id='password-login']/div/form/div/div[5]/div[1]/button"
        button = WebDriverWait(self.driver, self.wait_time).until(
            expected_conditions.visibility_of_element_located((By.XPATH, sign_in_button_xpath)))
        ActionChains(driver).move_to_element(button).click(button).perform()
        time.sleep(3)

    def __find_element_and_click(self, xpath, by=By.XPATH):
        button = WebDriverWait(self.driver, self.wait_time).until(
            expected_conditions.visibility_of_element_located((by, xpath)))
        try:
            ActionChains(self.driver).move_to_element(button).click(button).perform()
            # button.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", button)
        return self.driver

    def __find_element_and_send_key(self, xpath, key, by=By.XPATH):
        WebDriverWait(self.driver, self.wait_time).until(expected_conditions.visibility_of_element_located((by, xpath)))
        field = self.driver.find_element(by, xpath)
        field.send_keys(key)
        return self.driver

    def driver_close(self):
        self.driver.close()

    def scrape_url(self, url):
        result_dict = {}
        self.driver.get(url)
        self.url = url
        result_dict["url"] = url

        try:
            title_xpath = '//*[@id="main"]/header/div[2]/div/h1'
            title = WebDriverWait(self.driver, 30).until(
                expected_conditions.visibility_of_element_located((By.XPATH, title_xpath)))
        except:
            title = None

        if not title:
            try:
                title_xpath = '//*[@id="bigTopBox"]/div/div/h1'
                title = WebDriverWait(self.driver, 10).until(
                    expected_conditions.visibility_of_element_located((By.XPATH, title_xpath)))
            except:
                title = None

        # print(title.text)  # headline
        result_dict['headline'] = title.text
        article_content_xpath = '//*[@class="article-content  "]'
        element = self.driver.find_element(By.TAG_NAME, 'body')
        # print(element.get_attribute('innerHTML'))  # html
        result_dict['html'] = element.get_attribute('innerHTML')

        ps = self.driver.find_elements(By.TAG_NAME, "p")
        text = ''
        try:
            for p in ps:
                line = p.text
                if line[:16] == 'Appeared in the ':
                    break
                text += line
                # print(line)  # content
        except:
            pass
        result_dict['article_text'] = text
        try:
            time_xpath = '//*[@id="wsj-article-wrap"]/div/time '
            time = WebDriverWait(self.driver, self.wait_time).until(
                expected_conditions.visibility_of_element_located((By.XPATH, time_xpath)))
            # print(time.text)  # time
            result_dict['date_time'] = time.text
        except:
            time = None
        if result_dict['headline'] and result_dict['article_text']:
            result_dict['status'] = 'success'
        else:
            result_dict['status'] = 'failed'
        return result_dict

    def scrape_links(self, url):
        result_dict = {}
        self.driver.get(url)
        self.url = url
        result_dict["url"] = url

        link_xpath = "//*[contains(@class,'WSJTheme--headline')]/a"
        elems = WebDriverWait(self.driver, self.wait_time).until(
            expected_conditions.visibility_of_all_elements_located((By.XPATH, link_xpath)))
        links = [elem.get_attribute('href') for elem in elems]
        return links
