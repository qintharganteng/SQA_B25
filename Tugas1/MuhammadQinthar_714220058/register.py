from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Setup Chrome
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def safe_alert_text():
    try:
        alert = driver.switch_to.alert
        text = alert.text
        alert.accept()
        return text
    except NoAlertPresentException:
        return None

def handle_role_popup(role):
    wait = WebDriverWait(driver, 10)
    try:
        # Tunggu SweetAlert untuk memilih role muncul
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "swal2-popup")))
        select = wait.until(EC.presence_of_element_located((By.ID, "swal2-select")))

        # Pilih opsi role
        for option in select.find_elements(By.TAG_NAME, 'option'):
            if option.text.strip().lower() == role.lower():
                option.click()
                break
        else:
            print(f"[!] Role '{role}' tidak ditemukan di dropdown SweetAlert!")
            return False

        # Klik tombol OK pertama
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "swal2-confirm"))).click()

        # Tunggu popup konfirmasi "Role dipilih!" muncul
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "swal2-popup")))

        # Klik tombol OK kedua
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "swal2-confirm"))).click()

        # Tunggu SweetAlert menghilang
        wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "swal2-container")))
        return True
    except Exception as e:
        print(f"[!] Gagal memilih role atau mengkonfirmasi SweetAlert: {e}")
        return False


def test_register(fullname, hp, username, password, kategori_favorit, role):
    print(f"\n📝 MULAI TEST REGISTER dengan Username='{username}'")
    driver.get("https://nidasakinaa.github.io/KaloriKu-FE/pages/costumer/register.html")
    wait = WebDriverWait(driver, 10)
    time.sleep(2)

    try:
        # Isi input form
        wait.until(EC.presence_of_element_located((By.ID, "name"))).send_keys(fullname)
        driver.find_element(By.ID, "phone").send_keys(hp)
        driver.find_element(By.ID, "username").send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password)

        # Pilih kategori favorit (checkbox)
        kategori_labels = driver.find_elements(By.CSS_SELECTOR, "#categories label")
        selected = False
        for label in kategori_labels:
            input_element = label.find_element(By.TAG_NAME, "input")
            if input_element.get_attribute("value").lower() == kategori_favorit.lower():
                input_element.click()
                selected = True
                break
        if not selected:
            print(f"[!] Kategori '{kategori_favorit}' tidak ditemukan!")

        # Klik tombol Pilih Role
        driver.find_element(By.ID, "select-role").click()

        # Tangani SweetAlert2
        if not handle_role_popup(role):
            print(f"[✖] Gagal memilih role '{role}', test dibatalkan.")
            return

        # Klik tombol Register
        driver.find_element(By.XPATH, "//button[text()='Register']").click()

        # Cek alert
        time.sleep(2)
        alert_text = safe_alert_text()
        if alert_text:
            print(f"[✖] Register gagal: {alert_text}")
        else:
            print(f"[✔] Register berhasil: {username}")
    except Exception as e:
        print(f"[!] Error saat register dengan {username}: {e}")

# Jalankan test
test_register(
    fullname="Qinthar Ganteng",
    hp="0823232323232",
    username="qinthar_ganteng",
    password="password123",
    kategori_favorit="Salad",
    role="Customer"
)

driver.quit()
print("\n✅ Testing register selesai, browser ditutup.")