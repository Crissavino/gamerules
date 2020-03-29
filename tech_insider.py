# import urllib2
# from bs4 import BeautifulSoup
# from selenium.webdriver import Chrome
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.common.exceptions import StaleElementReferenceException
# from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver.support import expected_conditions as EC

# # selenium
# pathWebdriver = '/Users/cristiansavino/Desktop/Trabajo_FSWD/proyecto_blog/chromedriver'
# driver = Chrome(pathWebdriver)

# # url base apuntada
# url = 'https://www.businessinsider.com/sai?IR=T'

# driver.get(url)

# titulos = driver.find_elements_by_class_name('tout-title-link')
# notasFacebook = []
# notasGoogle = []
# hablaDeFacebook = 0
# # FUNCIONA BARBARO SOLO QUE DEBO CAMBIAR LA IP CADA VEZ Q ENTRO EN UNA NOTA PORQUE ME BLOQUEAN
# for i in range(len(titulos)):
#     titulo = driver.find_elements_by_class_name('tout-title-link')[i]
#     textoTitulo = titulo.text.encode('utf-8').strip()
#     # texto_xpath = "//a[text()="+ textoTitulo +"]"
#     link = ''
#     # reviso si en el texto del link se encuentra una palabra
#     if ('Zuckerberg' or "Zuckerberg's" or 'Facebook' or 'facebook') in textoTitulo:
#         try:
#             link = WebDriverWait(driver, 10).until(
#                 EC.visibility_of_element_located((By.LINK_TEXT, textoTitulo))
#             )
#             driver.execute_script("arguments[0].click();", link)
#             driver.get(driver.current_url)
#             articulo = WebDriverWait(driver, 20).until(
#                 EC.visibility_of_element_located((By.ID, 'piano-inline-content-wrapper'))
#             )
#             textoArticulo = articulo.text.encode('utf-8').strip()
#             notasFacebook.append({'titulo':textoTitulo, 'texto':textoArticulo})
#         finally:
#             print('Facebook')
#         driver.back()
#     # reviso si se habla de google
#     if ('Google' or "Google's" or 'google') in textoTitulo:
#         try:
#             link = WebDriverWait(driver, 10).until(
#                 EC.visibility_of_element_located((By.LINK_TEXT, textoTitulo))
#             )
#             driver.execute_script("arguments[0].click();", link)
#             driver.get(driver.current_url)
#             articulo = WebDriverWait(driver, 20).until(
#                 EC.visibility_of_element_located((By.ID, 'piano-inline-content-wrapper'))
#             )
#             textoArticulo = articulo.text.encode('utf-8').strip()
#             notasGoogle.append({'titulo':textoTitulo, 'texto':textoArticulo})
#         finally:
#             print('Google')
#         driver.back()
    
# print('Nota de Facebook ---->>' + notasFacebook)
# print('Nota de Google ---->>' + notasGoogle)

# # --------------

# PROBANDO PROXIES
from selenium import webdriver
from selenium.webdriver.chrome.options import DesiredCapabilities
from selenium.webdriver.common.proxy import Proxy, ProxyType
import urllib2
from bs4 import BeautifulSoup
# from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
import time
# import pandas as pd
import json


co = webdriver.ChromeOptions()
co.add_argument("log-level=3")
co.add_argument("--headless")
pathWebdriver = r'/Users/cristiansavino/Desktop/Trabajo_FSWD/proyecto_blog/chromedriver2'

# obtengo las proxies
def get_proxies(co=co):
    driver = webdriver.Chrome(chrome_options=co, executable_path=pathWebdriver)
    driver.get("https://free-proxy-list.net/")

    PROXIES = []
    proxies = driver.find_elements_by_css_selector("tr[role='row']")
    for p in proxies:
        result = p.text.split(" ")

        if result[-1] == "yes":
            PROXIES.append(result[0]+":"+result[1])

    driver.close()
    return PROXIES

# asigno las proxies
ALL_PROXIES = get_proxies()

def proxy_driver(PROXIES, co=co):
    prox = Proxy()

    if PROXIES:
        pxy = PROXIES[-1]
    else:
        print("--- Proxies used up (%s)" % len(PROXIES))
        PROXIES = get_proxies()

    prox.proxy_type = ProxyType.MANUAL
    prox.http_proxy = pxy
    prox.socks_proxy = pxy
    prox.ssl_proxy = pxy

    capabilities = webdriver.DesiredCapabilities.CHROME
    prox.add_to_capabilities(capabilities)

    driver = webdriver.Chrome(chrome_options=co, desired_capabilities=capabilities, executable_path=pathWebdriver)

    return driver



# --- YOU ONLY NEED TO CARE FROM THIS LINE ---
# creating new driver to use proxy
pd = proxy_driver(ALL_PROXIES)

# code must be in a while loop with a try to keep trying with different proxies
running = True

notasFacebook = []
notasGoogle = []
while running:
    try:
        # url base apuntada
        url = 'https://www.businessinsider.com/sai?IR=T'

        pd.get(url)
        print('entra')

        # las noticias en el inicio estan asi
        # TITULO
        # <h2 class="tout-title three-column top-vertical-trio item-3">
        #     <a class="tout-title-link" data-analytics-position="3" data-analytics-module="featured_post" href="/why-tiktok-is-successful-explained-by-advantage-over-facebook-instagram-2019-12">A tech investor whose firm made early bets on Facebook and Instagram explains TikTok's superpower</a>
        # </h2>
        # PARRAFO DEBAJO DEL TITULO
        # <div class="tout-copy three-column">
        #     TikTok's algorithms curate content in such a way that "everything you see generally makes you happy," said Andreessen Horowitz investor Connie Chan.
        # </div>

        # ver tambien la posibilidad de buscar en los parrafos al pie del titulo => son divs con las clases .tout-copy.river
        # parrafosTitulos = pd.find_elements_by_class_name('.tout-copy.river')
        titulos = pd.find_elements_by_class_name('tout-title-link')
        # notasFacebook = []
        # notasGoogle = []
        hablaDeFacebook = 0
        # FUNCIONA BARBARO SOLO QUE DEBO CAMBIAR LA IP CADA VEZ Q ENTRO EN UNA NOTA PORQUE ME BLOQUEAN
        for i in range(len(titulos)):
            titulo = pd.find_elements_by_class_name('tout-title-link')[i]
            textoTitulo = titulo.text.encode('utf-8').strip()
            # texto_xpath = "//a[text()="+ textoTitulo +"]"
            link = ''
            # reviso si en el texto del link se encuentra una palabra
            if ('Zuckerberg' or "Zuckerberg's" or 'Facebook' or 'facebook') in textoTitulo:
                try:
                    link = WebDriverWait(pd, 10).until(
                        EC.visibility_of_element_located((By.LINK_TEXT, textoTitulo))
                    )
                    pd.execute_script("arguments[0].click();", link)
                    pd.get(pd.current_url)
                    articulo = WebDriverWait(pd, 20).until(
                        EC.visibility_of_element_located((By.ID, 'piano-inline-content-wrapper'))
                    )
                    textoArticulo = articulo.text.encode('utf-8').strip()
                    notasFacebook.append({'titulo':textoTitulo, 'texto':textoArticulo})
                finally:
                    print('Facebook')
                pd.back()
            # reviso si se habla de google
            if ('Google' or "Google's" or 'google') in textoTitulo:
                try:
                    link = WebDriverWait(pd, 10).until(
                        EC.visibility_of_element_located((By.LINK_TEXT, textoTitulo))
                    )
                    pd.execute_script("arguments[0].click();", link)
                    pd.get(pd.current_url)
                    articulo = WebDriverWait(pd, 20).until(
                        EC.visibility_of_element_located((By.ID, 'piano-inline-content-wrapper'))
                    )
                    textoArticulo = articulo.text.encode('utf-8').strip()
                    notasGoogle.append({'titulo':textoTitulo, 'texto':textoArticulo})
                finally:
                    print('Google')
                pd.back()
            
        print('Facebook notes')
        print(notasFacebook)
        print('Google notes')
        print(notasGoogle)

        running = False
    except Exception as e:
        print(e)
        new = ALL_PROXIES.pop()
        
        # reassign driver if fail to switch proxy
        pd = proxy_driver(ALL_PROXIES)
        print("--- Switched proxy to: %s" % new)
        time.sleep(1)

with open('notasFacebook.json', 'w') as outfile:
    json.dump(notasFacebook, outfile, indent=4)

with open('notasGoogle.json', 'w') as outfile:
    json.dump(notasGoogle, outfile, indent=4)