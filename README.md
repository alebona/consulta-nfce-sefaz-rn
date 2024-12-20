# 🧾 **Projeto: Automação de Consulta de NFC-e com Web Scraping**

## 📜 **Descrição**

Este projeto automatiza o processo de consulta de uma **NFC-e** (Nota Fiscal de Consumidor Eletrônica) no site da **SEFAZ RN**. Ele faz o seguinte:

1. Acessa o site da SEFAZ RN.
2. Interpreta o **captcha** usando OCR (`pytesseract`).
3. Preenche o formulário com a **chave de acesso** e o **captcha**.
4. Faz **web scraping** da nota fiscal retornada e extrai os dados relevantes.

---

## 🛠️ **Tecnologias Utilizadas**

- **Python**: Linguagem principal do projeto.
- **Selenium**: Para automação do navegador.
- **Requests**: Para requisições HTTP.
- **pytesseract**: Para reconhecimento óptico de caracteres (OCR).
- **PIL (Pillow)**: Para manipulação e pré-processamento de imagens.
- **BeautifulSoup**: Para fazer web scraping e análise do HTML.
- **webdriver_manager**: Para gerenciar o ChromeDriver.
- **ChromeDriver**: Para automatizar o navegador Google Chrome.

---

## 📦 **Dependências**

Instale as dependências necessárias com o seguinte comando:

```bash
pip install requests selenium webdriver-manager pytesseract Pillow beautifulsoup4
```
---
## ⚙️ **Configuração do Tesseract**

Certifique-se de que o **Tesseract OCR** está instalado em sua máquina.


### 🖥️ **Windows**

1. Baixe o instalador em [Tesseract GitHub](https://github.com/UB-Mannheim/tesseract/wiki).

2. Instale o Tesseract em uma pasta, por exemplo:  
   `C:\Program Files\Tesseract-OCR`

3. Adicione o caminho ao executável no código:

   ```python
   pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
   ```

### 🐧 **Linux**

Para instalar o Tesseract no Linux, utilize o seguinte comando:

```bash
sudo apt-get install tesseract-ocr
```
---
## 🚀 **Como Executar o Projeto**

1. Clone o repositório:

   ```bash
   git clone [https://github.com/seu-usuario/nome-do-repositorio.git](https://github.com/alebona/consulta-nfce-sefaz-rn.git)
   cd consulta-nfce-sefaz-rn
    ```
2. Execute o script principal:

```bash
python index.py
```
