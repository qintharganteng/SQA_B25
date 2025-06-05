from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Inisialisasi WebDriver
driver = webdriver.Chrome(executable_path='path_to_chromedriver')

# Buka halaman web
driver.get("https://example.com")

# Menunggu hingga tombol muncul
button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "button_id"))
)

# Klik tombol
button.click()

# Tunggu beberapa detik untuk hasilnya (contoh: tunggu selama 5 detik)
driver.implicitly_wait(5)

# Tutup WebDriver
driver.quit()
