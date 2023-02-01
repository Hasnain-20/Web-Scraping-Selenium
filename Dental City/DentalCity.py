import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re

class DentalCity:
    
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
        driver.implicitly_wait(10)
        self.driver.get(self.url)

    def getCategoryUrl(self):
        catNavBar = self.driver.find_element(By.XPATH,'//a[@data-toggle = "dropdown"]')
        self.driver.get(catNavBar.get_attribute('href'))
        Catagories = self.driver.find_elements(By.XPATH, '//li[contains(@class, "categoriesdesc col-md-3 col-xs-6")]/a')
        tempLinks = []
        for i in Catagories:
            tempLinks.append(i.get_attribute('href'))
        links = []
        for i in tempLinks[:1]:
            self.driver.get(i)
            chk = self.driver.find_elements(By.XPATH,'//div[@class="category-name"]/span/a')
            for j in range(len(chk)):
                links.append(chk[j].get_attribute('href'))
        print(len(links))
        return links
    
    def getProductsUrl(self, links):
        prodLinks = []
        prods = []
        for i in links:
            driver.get(i)
            myBool = True
            try:
                driver.find_element(By.XPATH, '//select[@id="perpage"]')
            except:
                print("not found")
                myBool = False
            if myBool:
                try:
                    driver.find_element(By.LINK_TEXT, 'View All').click()
                except:
                    print("didnt find")
                time.sleep(2)
                try:
                    driver.find_element(By.XPATH,'//li[@class="listname"]')
                except:
                    print("Pages not Found")
            prods = driver.find_elements(By.XPATH, '//h3[@class="prodname"]/a')
            print(len(prods))
            for j in prods:
                prodLinks.append(j.get_attribute('href'))
        print(len(prodLinks))
        return prodLinks
    
    def getScriptDivElem(self):
        self.Script = self.driver.find_element(By.XPATH,'//div[@class="skucode"]')
        
    def getName(self,iKey):
        name = iKey.get_attribute('content').replace('\t',"")
        return name
    
    def getDescription(self,iKey):
        descp = iKey.get_attribute('content').replace('\n\n'," ").replace('.\n',".").replace('\n',". ")[:-1]
        return descp
    
    def getSku(self, iKey):
        sku = iKey.get_attribute('content')
        return sku
    
    def getMfgName(self):
        mfg = self.Script.find_element(By.TAG_NAME,'meta').get_attribute('content')
        return mfg
    
    def getMfgCode(self, iKey):
        mfgCode = iKey.get_attribute('content')
        return mfgCode
    
    def getCatSubCat(self, iKey):
        catSubCat = iKey.get_attribute('content').split('/')
        return catSubCat
    
    def getProductSpecificUrl(self, iKey):
        urrl = iKey.get_attribute('content')
        return urrl
    
    def getImagesUrl(self):
        self.driver.implicitly_wait(3)
        imgsUrls = None
        imgElems = self.driver.find_elements(By.XPATH,'//div[@class="mcs-item"]/a')
        if imgElems:
            imgsUrls = []
            for i in imgElems:
                urll = i.get_attribute('href')
                if urll not in imgsUrls:
                    imgsUrls.append(urll)
        else:
            imgElem = self.driver.find_element(By.XPATH,'//div[@id="skuimage"]/a')
            imgsUrls = imgElem.get_attribute('href')
        self.driver.implicitly_wait(10)
        return imgsUrls
        
    def getAttachmentUrl(self):
        self.driver.implicitly_wait(3)
        temp = None
        try:
            temp = self.driver.find_element(By.XPATH, '//div[@class="dc-product-sheet"]/a')
        except:
            print("No Attachment")
        if temp:
            return temp.get_attribute('href')
        temp = " "
        self.driver.implicitly_wait(10)
        return temp
    
    def makeCSV(self):
        df = pd.DataFrame({"Seller Platfrom" : self.SellerPlatform, "Seller SKU" : self.Sku, 
                           "Manufacturer Name": self.ManufacturerName,"Manufacturer Code" : self.ManufacturerCode, 
                           "Product Title" : self.ProductNames, "Description" : self.Description, 
                           "Packaging" : self.Packaging, "QTY" : self.Qty, "Catagory" : self.Catagory, 
                           "Sub Catagory" : self.SubCatagory, "Product Page URL" : self.ProductPageUrl, 
                           "Attachment URL" : self.AttchmentUrl, "Images URL" : self.ImagesUrls})
        df.to_csv(f'{self.sellerPlatform}.csv',index=False)
        return df
    
    def runScrapper(self):
        self.getUrl()
        catALinks = self.getCategoryUrl()
        prodUrls = self.getProductsUrl(catALinks)
        for i in range(len(prodUrls[:50])):
            self.driver.get(prodUrls[i])
            print(i,": ",prodUrls[i])
            imgsUrls = self.getImagesUrl()
            self.getScriptDivElem()
            descp = self.getDescription(self.Script.find_elements(By.XPATH,'./div/meta')[3])
            nme = self.Script.find_element(By.TAG_NAME,'meta').get_attribute('content')
            for j in self.Script.find_elements(By.XPATH,'./div'):
                elems = j.find_elements(By.XPATH,'./meta')
                self.SellerPlatform.append(self.sellerPlatform)
                name = self.getName(elems[0])
                self.ProductNames.append(name)
                self.Sku.append(self.getSku(elems[1]))
                catSub = self.getCatSubCat(elems[2])
                self.Catagory.append(catSub[0])
                self.SubCatagory.append(catSub[1])
                elem2 = j.find_elements(By.XPATH,'./div/meta')
                self.ProductPageUrl.append(self.getProductSpecificUrl(elem2[-1]))
                self.ManufacturerCode.append(self.getMfgCode(elem2[-2]))
                self.ManufacturerName.append(nme)
                self.Description.append(descp)
                self.ImagesUrls.append(imgsUrls)
                self.AttchmentUrl.append(self.getAttachmentUrl())
                quant = re.findall('\d{1,}\/\D*', name)
                if quant:
                    qtyPkg = quant[0].split('/')
                    self.Qty.append(qtyPkg[0])
                    self.Packaging.append(qtyPkg[1])
                else:
                    self.Qty.append("")
                    self.Packaging.append("")
        return self.makeCSV()
    
    def quitScrapper(self):
        self.driver.quit()

if __name__ == "__main__":
    SPlatfrom = "Dental City"
    url = "https://www.dentalcity.com/"
    driver = webdriver.Chrome()
    scraper = DentalCity(driver,url,SPlatfrom)
    scraped = scraper.runScrapper()
    print(scraped.head())
    time.sleep(2)
    scraper.quitScrapper()