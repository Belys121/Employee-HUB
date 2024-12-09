from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from django.contrib.auth.models import User
import time

class MySeleniumTests(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Nastavení možností prohlížeče Chrome
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Spuštění bez grafického rozhraní
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        # Inicializace WebDriveru s nastavenými možnostmi
        cls.selenium = webdriver.Chrome(service=Service(), options=chrome_options)
        cls.selenium.implicitly_wait(10)

        # Vytvoření administrátorského uživatele
        cls.admin_user = User.objects.create_superuser(
            username='admin',
            password='admin',
            email='admin@example.com'
        )

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        # Přístup na URL přihlašovací stránky
        self.selenium.get(f'{self.live_server_url}/registration/login/')
        time.sleep(2)
        # Vyhledání a vyplnění polí pro uživatelské jméno a heslo
        username_input = self.selenium.find_element(By.NAME, "username")
        password_input = self.selenium.find_element(By.NAME, "password")
        username_input.send_keys('admin')
        password_input.send_keys('admin')
        time.sleep(2)
        # Odeslání formuláře
        self.selenium.find_element(By.XPATH, '//button[@type="submit"]').click()
        time.sleep(2)

        # Ověření úspěšného přihlášení (kontrola přítomnosti uvítací zprávy)
        self.assertIn("Vítejte, admin!", self.selenium.page_source)
