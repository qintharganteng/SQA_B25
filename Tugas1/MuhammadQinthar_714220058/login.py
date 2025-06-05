from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import UnexpectedAlertPresentException, NoAlertPresentException
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
import time

# Setup Chrome
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Fungsi aman untuk membaca alert
def safe_alert_text():
    try:
        alert = driver.switch_to.alert
        text = alert.text
        alert.accept()
        return text
    except NoAlertPresentException:
        return None

# Fungsi login
def test_login(username, password, role):
    print(f"\n🔐 MULAI TEST LOGIN dengan Username='{username}' Password='{password}' Role='{role}'")
    driver.get("https://nidasakinaa.github.io/KaloriKu-FE/pages/form_login.html")
    time.sleep(2)

    leftover_alert = safe_alert_text()
    if leftover_alert:
        print(f"[!] Alert sisa ditemukan: {leftover_alert}")

    try:
        # Isi form
        driver.find_element(By.ID, "username").clear()
        driver.find_element(By.ID, "username").send_keys(username)
        driver.find_element(By.ID, "password").clear()
        driver.find_element(By.ID, "password").send_keys(password)

        # Pilih role dari dropdown
        select_role = Select(driver.find_element(By.ID, "role"))
        select_role.select_by_visible_text(role)  # Harus sesuai: "Admin" atau "Customer"

        # Klik login
        driver.find_element(By.XPATH, "//button[text()='Login']").click()
        time.sleep(2)

        alert_text = safe_alert_text()
        if alert_text:
            print(f"[✖] Login gagal: {alert_text}")
        else:
            print(f"[✔] Login berhasil: {username} / {role}")

    except UnexpectedAlertPresentException:
        alert_text = safe_alert_text()
        print(f"[✖] Login gagal cepat: {alert_text}")

    except Exception as e:
        print(f"[!] Error saat login dengan {username} / {password} / {role}: {e}")

# Test case login
test_cases = [
    ("admin", "admin123", "Admin"),      # Valid
    ("admin", "salah", "Admin"),         # Salah password
    ("user", "admin123", "Admin"),       # Salah username
    ("", "", "Customer"),                # Kosong semua
    ("customer", "customer123", "Customer")  # Contoh valid lain
]

for username, password, role in test_cases:
    test_login(username, password, role)

driver.quit()
print("\n✅ Testing selesai, browser ditutup.")
