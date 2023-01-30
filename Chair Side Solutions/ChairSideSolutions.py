import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class chairSideSolutions:
    
    def __init__(self, driver, url, splat):
        self.driver = driver
        self.url = url
        self.sellerPlatform = splat
        
        self.ImagesUrls = []
        self.Description = []
        self.ProductPageUrl = []
        self.ProductNames = []
        self.Catagory = []
        self.Sku = []
        self.SubCatagory = []
        self.Qty = []
        self.ManufacturerName = []
        self.ManufacturerCode = []
        self.SellerPlatform = []
        self.Packaging = []
        self.AttchmentUrl = []
        self.Script = None
        
        self.tempCat = []
        self.tempSubCat = []
        
    def getUrl(self):
        self.driver.get(self.url)

    def getCategoryUrl(self):
        Catagories = driver.find_elements(By.XPATH, '//li[@class="category-item"]')
        links = []
        cat = []
        for i in Catagories[1:]:
            chk = i.find_element(By.TAG_NAME,'a')
            cat.append(chk.text)
            links.append(chk.get_attribute('href'))
        return [cat, links]
    
    def getProductsUrl(self, links, cat):
        prodLinks = []
        for i in range(len(links)):
            self.driver.get(links[i])
            try:
                subcats = self.driver.find_elements(By.XPATH, '//a[contains(@class,"category-link child")]')
                subcatslinks = []
                subcatsnames = []
                for j in subcats:
                    subcatslinks.append(j.get_attribute('href'))
                    subcatsnames.append(j.text)
            except:
                subcats = []
            if subcats:
                for j in range(len(subcatslinks)):
                    self.driver.get(subcatslinks[j])
                    chk = self.driver.find_elements(By.XPATH, '//a[@class = "grid-item-link"]')
                    for k in chk:
                        self.tempCat.append(cat[i])
                        self.tempSubCat.append(subcatsnames[j])
                        prodLinks.append(k.get_attribute('href'))
            else: 
                chk = self.driver.find_elements(By.XPATH, '//a[@class = "grid-item-link"]')
                for j in chk:
                    self.tempCat.append(cat[i])
                    self.tempSubCat.append("")
                    prodLinks.append(j.get_attribute('href'))
        print(len(prodLinks))
        print(len(self.tempCat))
        print(len(self.tempSubCat))
        return prodLinks
    
    def getImagesUrls(self):
        imgsUrls = []
        chk = self.driver.find_elements(By.XPATH,'//div[contains(@class,"ProductItem-gallery-slides-item")]')
        for j in chk:
            chk2 = j.find_element(By.TAG_NAME, 'img')
            imgsUrls.append(chk2.get_attribute('data-src'))
        return imgsUrls
    
    def getDescription(self):
        try:
            elemDescp = self.driver.find_element(By.XPATH,'//div[@class="ProductItem-details-excerpt"]').text
            descp = elemDescp.replace('  ',"").replace('\n'," ")
        except:
            descp = ""
        return descp
    
    def getScript(self):
        temp = self.driver.find_element(By.XPATH,'//script[@data-name="static-context"]').get_attribute('innerHTML')
        script = json.loads(temp.split("SQUARESPACE_CONTEXT = ")[1].replace(";",""))
        self.Script = script
    
    def getName(self, iKey, attr, title):
        name = ""
        if attr:
            name = name + title
            for i in attr:
                name = name + " - " + iKey['attributes'][i]
        else:
            name = title
        return name
    
    def makeCSV(self):
        df = pd.DataFrame({"Seller Platfrom" : self.SellerPlatform, "SKU" : self.Sku, "Manufacute Name": self.ManufacturerName,
                           "Manufacture Code" : self.ManufacturerCode, "Product Title" : self.ProductNames, 
                           "Description" : self.Description, "Packaging" : self.Packaging, "QTY" : self.Qty, 
                           "Catagory" : self.Catagory, "Sub Catagory" : self.SubCatagory,
                           "Product Page URL" : self.ProductPageUrl, "Attachment URL" : self.AttchmentUrl,
                           "Images URL" : self.ImagesUrls})
        df.to_csv(f'{self.sellerPlatform}.csv',index=False)
        df.to_csv("abc.csv",index=False)
        return df
    
    def runScrapper(self):
        attr = None
        self.getUrl()
        catALinks = self.getCategoryUrl()
        prodUrls = self.getProductsUrl(catALinks[1], catALinks[0])
        for i in range(len(prodUrls)):
            self.driver.get(prodUrls[i])
            print(i,": ",prodUrls[i])
            imgsUrls = self.getImagesUrls()
            descp = self.getDescription()
            self.getScript()
            title = self.Script['item']['title']
            try:
                attr = self.Script['product']['variantAttributeNames']
            except:
                attr = ""
            for j in self.Script['product']['variants']:
                skk = j['sku']
                self.Sku.append(skk)
                self.ProductNames.append(self.getName(j,attr,title))
                self.ProductPageUrl.append(prodUrls[i])
                self.SellerPlatform.append(self.sellerPlatform)
                self.Description.append(descp)
                self.ImagesUrls.append(imgsUrls)
                self.Catagory.append(self.tempCat[i])
                self.SubCatagory.append(self.tempSubCat[i])
                self.ManufacturerCode.append(skk)
                self.ManufacturerName.append(self.sellerPlatform)
                self.Qty.append("")
                self.AttchmentUrl.append("")
                self.Packaging.append("")
        return self.makeCSV()
    
    def quitScrapper(self):
        self.driver.quit()

if __name__ == "__main__":
    SPlatfrom = "Chair Side Solutions"
    url = "https://www.chairsidesolutions.com/shop"
    driver = webdriver.Chrome()
    scraper = chairSideSolutions (driver,url,SPlatfrom)
    scraped = scraper.runScrapper()
    print(scraped.head(20))
    time.sleep(2)
    scraper.quitScrapper()