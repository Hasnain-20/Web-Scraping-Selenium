import json
import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def getCatagories(driver):
    driver.find_element(By.LINK_TEXT,"SHOP BY").click()
    Catagories = driver.find_elements(By.XPATH, '//*[@id="dropdown-desktop-menu-0-1"]/li')
    cat = []
    links = []
    for i in Catagories:
        chk = i.find_element(By.TAG_NAME,'a')
        cat.append(chk.text)
        links.append(chk.get_attribute('href'))
    return [cat, links]

def getProductURLs(driver,links):
    prodUrls = []
    for i in range(len(links)):
        driver.get(links[i])
        chk = driver.find_elements(By.XPATH,"//div[@class='product-item__info-inner']")
        for j in chk:
            chk2 = j.find_element(By.TAG_NAME,'a')
            prodUrls.append(chk2.get_attribute('href'))
        try:
            nexElem = driver.find_element(By.LINK_TEXT,"Next")
            while(True):
                driver.get(nexElem.get_attribute('href'))
                time.sleep(1)
                chk = driver.find_elements(By.XPATH,"//div[@class='product-item__info-inner']")
                for j in chk:
                    chk2 = j.find_element(By.TAG_NAME,'a')
                    prodUrls.append(chk2.get_attribute('href'))
                try:
                    nexElem = driver.find_element(By.LINK_TEXT,"Next")
                except:
                    break
        except:
            continue
    return prodUrls

def getImagesUrls(driver, prodlinks, url):
    imgsUrls = []
    Description = []
    ProductPageUrl = []
    ProductNames = []
    Catagory = []
    sku = []
    subCatagory = []
    Qty = []
    ManufacturerName = []
    ManufacturerCode = []
    SellerPlatform = []
    Packaging = []
    AttchmentUrl = []
    for i in prodlinks:
        driver.get(i)
        catElem = driver.find_elements(By.XPATH, '//a[contains(@class,"breadcrumb__link link")]')[1]
#         Catagory.append(catElem.text)
        elemDescp = driver.find_element(By.XPATH,"//div[contains(@class, 'rte text--pull')]").text
#         Description.appendpen(elemDescp.replace('  ',"").replace('\n'," "))
        chk = driver.find_elements(By.XPATH,"//div[@class='product-gallery__thumbnail-list']")
        for j in chk:
            chk2 = j.find_elements(By.TAG_NAME, 'img')
            imgs = []
            for k in chk2:
                imgs.append(k.get_attribute('src'))
#             imgsUrls.append(imgs)
        elemScript = json.loads(driver.find_element(By.XPATH,'//script[@type="application/ld+json"][1]').get_attribute('innerHTML'))
        for i in elemScript['offers']:
            try:
                sku.append(i['sku'])
                ManufacturerCode.append(i['sku'])
            except:
                sku.append("")
                ManufacturerCode.append("")
            ManufacturerName.append("")
            nme = elemScript['name'] + " - " + i['name'].replace("/","",1)
            ProductNames.append(nme)
            ProductPageUrl.append(url + "/products" +i['url'].split('/products')[-1])
            Description.append(elemDescp.replace('  ',"").replace('\n'," "))
            Catagory.append(catElem.text)
            subCatagory.append("")
            imgsUrls.append(imgs)
            x = str(re.findall(r'\(.*?\)', nme))
            if x:
                k = re.findall('\d+',x)
                if k:
                    Qty.append(k[0])
                else:
                    Qty.append("")
            else:
                Qty.append("")
            SellerPlatform.append('CX Orthodontic Supply')
            Packaging.append("")
            AttchmentUrl.append("")
#     print(len(Packaging))
#     print(len(SellerPlatform))
#     print(len(sku))
#     print(len(ManufacturerCode))
#     print(len(ManufacturerName))
#     print(len(ProductNames))
#     print(len(Description))
#     print(len(Qty))
#     print(len(Catagory))
#     print(len(subCatagory))
#     print(len(ProductPageUrl))
#     print(len(AttchmentUrl))
#     print(len(imgsUrls))
    df = pd.DataFrame({"Seller Platfrom" : SellerPlatform, "SKU" : sku, "Manufacute Name": ManufacturerName,
                       "Manufacture Code" : ManufacturerCode, "Product Title" : ProductNames, "Description" : Description,
                       "Packaging" : Packaging, "QTY" : Qty, "Catagory" : Catagory, "Sub Catagory" : subCatagory,
                       "Product Page URL" : ProductPageUrl, "Attachment URL" : AttchmentUrl, "Images URL" : imgsUrls})
    return df


if __name__ == '__main__':
    url = "https://cxorthosupply.com/"
    driver = webdriver.Chrome()
    driver.get(url)
    catLinks = getCatagories(driver)
    Catagory = catLinks[0]
    CatagoryLinks = catLinks[1]
    ProductURLs = getProductURLs(driver, CatagoryLinks)
    print(len(ProductURLs))
    Scraped_Data = getImagesUrls(driver, ProductURLs,url)
    print(Scraped_Data.head(20))
    Scraped_Data.to_csv('CX Orthodontic Supply.csv',index=False)
    time.sleep(5)
    driver.quit()