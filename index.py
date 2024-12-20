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
from bs4 import BeautifulSoup
import os
'''
def preprocess_image(image):

    gray_image = ImageOps.grayscale(image)

    contrast_image = ImageEnhance.Contrast(gray_image).enhance(3)  

    blurred_image = contrast_image.filter(ImageFilter.MedianFilter(3))  

    enhanced_image = ImageEnhance.Brightness(blurred_image).enhance(1.5)  

    enhanced_image.save("processed_image.png")

    return enhanced_image
'''

def delete_images():
    try:
        os.remove("captcha_image_original.png")
        os.remove("processed_image.png")
        print("Imagens deletadas com sucesso.")
    except FileNotFoundError as e:
        print(f"Arquivo não encontrado: {e}")
    except Exception as e:
        print(f"Erro ao deletar imagens: {e}")

def preprocess_image(image):
    # Converter a imagem para escala de cinza
    gray_image = ImageOps.grayscale(image)

    # Aumentar o contraste
    contrast_image = ImageEnhance.Contrast(gray_image).enhance(3)

    # Aplicar um filtro de mediana para reduzir ruídos
    blurred_image = contrast_image.filter(ImageFilter.MedianFilter(3))

    # Reduzir o brilho para deixar a imagem mais escura
    darker_image = ImageEnhance.Brightness(blurred_image).enhance(0.6)  # Ajuste para escurecer (0.6 = 60% do brilho original)

    # Salvar a imagem processada
    darker_image.save("processed_image.png")

    return darker_image

def save_image(image, filename):
    image.save(filename)


def getNF(chave_acesso):
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--no-first-run --no-service-autorun --password-store=basic")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging", "disable-popup-blocking", "disable-infobars"])

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    tentativas = True
    while tentativas :
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

                captcha_resolvido = pytesseract.image_to_string(
                    processed_image,
                    config='--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789'
                ).strip()

                print(f"Tentativa {tentativas + 1} - CAPTCHA resolvido: {captcha_resolvido}")

                if not captcha_resolvido:
                    print("Tentando com a imagem original sem pré-processamento")
                    captcha_resolvido = pytesseract.image_to_string(
                        captcha_image,
                        config='--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789'
                    ).strip()
                    print(f"CAPTCHA resolvido da imagem original: {captcha_resolvido}")

                # Inserir a chave de acesso e o CAPTCHA
                chave_acesso_input = driver.find_element(By.NAME, 'ctl03$txt_chave_acesso')
                captcha_input = driver.find_element(By.NAME, 'txt_cod_antirobo')

                chave_acesso_input.clear()
                chave_acesso_input.send_keys(chave_acesso)
                captcha_input.send_keys(captcha_resolvido)
                captcha_input.send_keys(Keys.RETURN)

                time.sleep(5)

                # Verificar se a mensagem de erro está presente
                page_html = driver.page_source
                if "Código verificador inválido" in page_html:
                    print("Código verificador inválido. Tentando novamente...")
                    continue  # Tenta novamente
                else:
                    tentativas = False
                    # Se não houver erro, extrair os dados
                    #extraiDadosHTML(page_html)
                    #break  # Sai do loop se bem-sucedido
                
                with open("nfce_page.html", "w", encoding="utf-8") as file:
                    file.write(page_html)
                    print("Página HTML salva em 'nfce_page.html'")    
                

            else:
                print("URL do CAPTCHA não encontrada.")
                break

        except Exception as e:
            print(f"Erro durante a execução: {e}")
            break
        finally:
            delete_images()

    driver.quit()

        
        
def extraiDadosHTML(page_html):
    soup = BeautifulSoup(page_html, 'html.parser')
    
    #pesquisar os dados que eu quero pela tag/id
    nfce_data = soup.find('div', id='id_da_div_com_dados_nfce') 

    if nfce_data:
        nfce_text = nfce_data.get_text(strip=True)
        print("Dados da NFCe extraídos:")
        print(nfce_text)
        return nfce_text
    else:
        print("Dados da NFCe não encontrados.")
        return None
        
        
getNF('')
