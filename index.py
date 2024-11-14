import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pytesseract
from PIL import Image, ImageOps, ImageEnhance, ImageFilter
import time
from io import BytesIO

def preprocess_image(image):

    gray_image = ImageOps.grayscale(image)

    contrast_image = ImageEnhance.Contrast(gray_image).enhance(3)  

    blurred_image = contrast_image.filter(ImageFilter.MedianFilter(3))  

    enhanced_image = ImageEnhance.Brightness(blurred_image).enhance(1.5)  

    enhanced_image.save("processed_image.png")

    return enhanced_image

def save_image(image, filename):
    image.save(filename)

chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--no-first-run --no-service-autorun --password-store=basic")
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging", "disable-popup-blocking", "disable-infobars"])

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def getNF(chave_acesso):
    try:

        driver.get("https://nfce.set.rn.gov.br/portalDFE/NFCe/ConsultaNFCe.aspx")
        
        time.sleep(5)

        captcha_element = driver.find_element(By.ID, 'img_captcha')
        captcha_image_url = captcha_element.get_attribute('src')

        if captcha_image_url:
            headers = {'User-Agent': 'Mozilla/5.0'}
            cookies = driver.get_cookies()
            session = requests.Session()
            for cookie in cookies:
                session.cookies.set(cookie['name'], cookie['value'])
            
            captcha_response = session.get(captcha_image_url, headers=headers, stream=True)

            captcha_image = Image.open(BytesIO(captcha_response.content))

            save_image(captcha_image, "captcha_image_original.png")

            processed_image = preprocess_image(captcha_image)

            captcha_resolvido = pytesseract.image_to_string(processed_image, config='--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789').strip()

            print(f"Texto do CAPTCHA resolvido: {captcha_resolvido}")

            if not captcha_resolvido:
                print("Tentando com a imagem original sem pré-processamento")
                captcha_resolvido = pytesseract.image_to_string(captcha_image, config='--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789').strip()
                print(f"Texto do CAPTCHA resolvido da imagem original: {captcha_resolvido}")

            chave_acesso_input = driver.find_element(By.NAME, 'ctl03$txt_chave_acesso')
            chave_acesso_input.send_keys(chave_acesso)
            captcha_input = driver.find_element(By.NAME, 'txt_cod_antirobo') 
            captcha_input.send_keys(captcha_resolvido)

            captcha_input.send_keys(Keys.RETURN)

            time.sleep(5)

        else:
            print("URL do CAPTCHA não encontrada.")

    except Exception as e:
        print(f"Erro durante a execução: {e}")

    finally:
        driver.quit()
        
        

