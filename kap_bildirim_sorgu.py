from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import subprocess  # Diğer betiği çalıştırmak için kullanacağız

# ChromeDriver'ı başlat
driver = webdriver.Chrome()

# KAP bildirim sorgulama sayfasına git
driver.get("https://www.kap.org.tr/tr/bildirim-sorgu")

# Sayfanın yüklenmesini bekle
time.sleep(5)

# İlk butona bas (Bildirim Tipi Seçimi)
bildirim_tipi_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="email-form"]/div[4]/div[4]/isteven-multi-select/span/button'))
)
bildirim_tipi_button.click()

# Doğru Kar Payı Dağıtımını seç (Belirttiğin XPath ile)
kar_payi_secim = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="email-form"]/div[4]/div[4]/isteven-multi-select/span/div/div[2]/div[92]/div/label/span'))
)
kar_payi_secim.click()

# Tarih seçme butonuna bas
tarih_secim_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="email-form"]/div[6]/div[1]/div[2]/a'))
)
driver.execute_script("arguments[0].click();", tarih_secim_button)

# İstenen tarih aralığını seç (Belirttiğin XPath ile)
istenen_tarih = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="mCSB_1_container"]/a[4]'))
)
istenen_tarih.click()

# JavaScript ile "Ara" butonuna tıklayalım
ara_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="email-form"]/a[1]'))
)
driver.execute_script("arguments[0].click();", ara_button)

# Bildirimlerin yüklenmesi için bekle
time.sleep(5)

# Linkleri bir dosyaya kaydetmek için listeyi toplayalım
links = []

# Notificationların XPath'ini dinamik olarak arttırarak tıklayıp linklerini alalım
i = 3  # İlk notification XPath'indeki sayıyı başlat
while True:
    try:
        # Dinamik olarak XPath'i oluştur
        dynamic_xpath = f'//*[@id="tab1"]/div/div[2]/div[2]/div/div[{i}]'
        
        # Bildirimi bul
        bildirim = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, dynamic_xpath))
        )
        
        # Bildirime tıkla
        bildirim.click()
        time.sleep(2)  # Sayfanın yüklenmesi için kısa bir bekleme süresi ekle

        # Açılan sayfanın URL'sini al
        current_url = driver.current_url
        print(current_url)
        links.append(current_url)  # Linki listeye ekle

        # Geri dön
        driver.back()
        time.sleep(2)  # Geri dönme işlemi için kısa bir bekleme süresi ekle

        # XPath'in sonundaki sayıyı artır
        i += 1

    except Exception as e:
        print(f"Tüm bildirimler işlendi veya hata oluştu: {str(e)}")
        break

# Linkleri bir dosyaya kaydet
with open("bildirim_links.txt", "w") as file:
    for link in links:
        file.write(f"{link}\n")

# Tarayıcıyı kapat
driver.quit()

# kap_bildirimpage.py dosyasını çalıştır
subprocess.run(["python", "kap_bildirimpage.py"])
