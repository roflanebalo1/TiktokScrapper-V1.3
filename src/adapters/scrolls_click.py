from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import Chrome
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver


class Scrolls_Click():

    def smooth_scroll(self,elem: WebElement, driver: WebDriver):
        driver.execute_script(
            """arguments[0].scrollIntoView({block: "center", behavior: "smooth"});""", elem
        ) 

    def smooth_click(self,elem: WebElement, driver: WebDriver):
        driver.execute_script(
            """arguments[0].click({block: "center", behavior: "smooth"});""", elem
        ) 