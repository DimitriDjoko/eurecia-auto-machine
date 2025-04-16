from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

import os
import time
import traceback


# Charger les identifiants depuis le .env
load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

print("📧 Email chargé :", EMAIL)
print("🔒 Mot de passe chargé :", "****" if PASSWORD else "(vide)")

print("🔐 Connexion à Eurécia...")

# Bloquer les notifications
options = Options()
options.add_argument("--disable-notifications")  # bloque popup
options.add_experimental_option("prefs", {
    "profile.default_content_setting_values.notifications": 2,
    "profile.default_content_setting_values.geolocation": 2,
    "profile.default_content_setting_values.media_stream": 2
})


try:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://preprod.eurecia.com/eurecia/logout.do")

    wait = WebDriverWait(driver, 10)

    # Étape 1 : saisir l’email
    email_field = wait.until(EC.presence_of_element_located((By.ID, "email")))
    email_field.send_keys(EMAIL)
    print("✅ Email saisi")

    # Étape 2 : cliquer sur “Suivant”
    btn_suivant = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn-raised")))
    btn_suivant.click()
    print("➡️ Suivant cliqué")

    # Étape 3 : attendre et remplir le mot de passe
    password_field = wait.until(EC.presence_of_element_located((By.ID, "password")))
    password_field.send_keys(PASSWORD)
    print("🔑 Mot de passe saisi")

    # Étape 4 : cliquer sur “Connexion” (adapté après inspection HTML)
    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Connexion')]")))
    login_button.click()
    print("🚪 Connexion envoyée")

   # Etape 5 : Après la connexion
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ea-btn-nav")))
    print("🏠 Connexion réussie, page chargée")
   
    # Étape 6 : Cliquer sur le bouton "MENU"; cliquer sur notes de frais et consultation/validation
    menu_button = wait.until(EC.element_to_be_clickable(
    (By.XPATH, "//span[contains(@class, 'icon-menu')]")
    ))
    menu_button.click()
    print("📂 Menu ouvert")

    notes_de_frais_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'NOTES DE FRAIS')]")))
    notes_de_frais_btn.click()
    
    consultation_validation_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Consultation / Validation')]")))
    consultation_validation_btn.click()
    
    # Etape 7: Attendre et entrer dans l’iframe avec l’URL partielle "expensesReport/Browse.do"
    iframe = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//iframe[contains(@src, 'expensesReport/Browse.do')]"))
    )
    driver.switch_to.frame(iframe)
    print("✅ Bascule dans l’iframe réussie")

    # Etape 8: Attendre la ligne contenant 'GERARD MATHILDE'
    row = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//tr[contains(., 'GERARD MATHILDE')]"))
    )
    print("✅ Ligne 'GERARD MATHILDE' trouvée")

    # Etape 9: Trouver la cellule d'action dans cette ligne
    action_cell = row.find_element(By.CLASS_NAME, "btn-group-multiple")

    # Etape 10: Trouver le bouton à survoler
    menu_button = action_cell.find_element(By.XPATH, ".//button[contains(@class, 'menu-button')]")

    # Etape 11: Effectuer le survol
    actions = ActionChains(driver)
    actions.move_to_element(menu_button).perform()
    driver.execute_script("arguments[0].click();", menu_button)
    print("🖱️ Survol du bouton 'menu-button' effectué avec succès")

    # 5. Attendre l’apparition du lien "Télécharger les justificatifs"
    download_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[@title='Télécharger les justificatifs']"))
    )
    print("📄 Lien de téléchargement détecté")

    # 6. Cliquer sur le lien
    driver.execute_script("arguments[0].click();", download_link)
    print("📥 Téléchargement lancé")
    time.sleep(2)
    
    # Pause pour laisser la nouvelle page charger
    time.sleep(5)
    driver.quit()

except Exception as e:
    print("❌ Une erreur est survenue :")
    traceback.print_exc()