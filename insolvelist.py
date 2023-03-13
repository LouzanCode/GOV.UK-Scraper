from requests import head
from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import csv
from selenium.webdriver.common.by import By


class Insolvency_List_UK_Scraper:
      
      impicitlyWaitTime = 1
      sleepTime = 1
      sleep = True

      def __init__(self):
        self.options = webdriver.ChromeOptions()
        #self.options.add_argument('--headless')  # ----> Opcion de driver para ejecutarlo  sin abrir el navegador
        #options.add_argument('--no-sandbox')
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        # options.add_argument("user-data-dir=selenium")
        self.options.add_argument("--remote-debugging-port=9222")
        self.options.add_argument('--disable-dev-shm-usage')

        self.driver = webdriver.Chrome(executable_path = r"C:\\Users\\marcl\\drivers\\chromedriver110\\chromedriver.exe", options = self.options)
    
        #self.driver.maximize_window()

      def Sleep(self):
       if self.sleep == True:
        time.sleep(self.sleepTime)

      def Render(self):
        for i in range(1,22):
         ActionChains(self.driver).send_keys(Keys.SPACE).perform()
        for i in range(1,192):
         ActionChains(self.driver).send_keys(Keys.UP).perform()

      def Search_By_Surname(self):
        print("---------------------------------------")
        print("Introduce un apellido inglés:")
        print("---------------------------------------")
        surname = input()
        print("---------------------------------------")
        print("CARGANDO SCRAPER......")
        print("---------------------------------------")
        
        self.driver.get("https://www.gov.uk/government/organisations/insolvency-service")

        self.driver.implicitly_wait(self.impicitlyWaitTime)
        cookies_btn = self.driver.find_element(By.CLASS_NAME, 'gem-c-button.govuk-button')
        ActionChains(self.driver).move_to_element(cookies_btn).click().perform()
        self.Sleep()

        self.driver.implicitly_wait(self.impicitlyWaitTime)
        first_link = self.driver.find_element(By.CLASS_NAME, 'govuk-link.govuk-link--no-underline.app-c-topic-list__link.brand__color')
        ActionChains(self.driver).move_to_element(first_link).click().perform()
        self.Sleep()

        self.driver.implicitly_wait(self.impicitlyWaitTime)
        second_link = self.driver.find_element(By.XPATH, '//*[text()="search the register"]')
        ActionChains(self.driver).move_to_element(second_link).click().perform()
        self.Sleep()

        self.driver.implicitly_wait(self.impicitlyWaitTime)
        name_details = self.driver.find_element(By.ID, 'btnName')
        ActionChains(self.driver).move_to_element(name_details).click().perform()
        self.Sleep()

        self.driver.implicitly_wait(self.impicitlyWaitTime)
        input_element = self.driver.find_element(By.ID, 'surnamesearch')
        ActionChains(self.driver).move_to_element(input_element).click().send_keys(surname).perform()
        self.Sleep()

        self.driver.implicitly_wait(self.impicitlyWaitTime)
        submit = self.driver.find_element(By.ID, 'btnSubmit')
        ActionChains(self.driver).move_to_element(submit).click().perform()
        self.Sleep()

      def Extract_Results(self):

        headers = ['Title', 'Forename', 'Surname', 'Date of birth', 'Number', 'Adress', 'Start']
        with open('insolve_list.csv','w+', encoding = 'utf-8', newline='') as file:
          wr = csv.writer(file, dialect = 'excel')
          wr.writerow(headers)

          i = 1
          while i < 354:
           for a in range(1, 16):
                
            self.driver.implicitly_wait(self.impicitlyWaitTime)
            try:
              link = self.driver.find_element(By.XPATH, f'//*[@id="mainbody"]/table[1]/tbody/tr[{a}]/td[2]/a')
            except:
              continue

            link_personal = link.get_attribute('href')

            self.driver.get(link_personal)
            self.Sleep()
            
            self.Render()

            try:
              surname = self.driver.find_element(By.XPATH, f'//*[@id="mainbody"]/form/table[2]/tbody/tr[1]/td[2]').text
              print(surname)
            except:
              surname = ''
            
            try:
              forename = self.driver.find_element(By.XPATH, f'//*[@id="mainbody"]/form/table[2]/tbody/tr[2]/td[2]').text
              print(forename)
            except:
              forename = ''

            try:
              title = self.driver.find_element(By.XPATH, f'//*[@id="mainbody"]/form/table[2]/tbody/tr[3]/td[2]').text
              print(title)
            except:
              title = ''
            try:
              birth = self.driver.find_element(By.XPATH, f'//*[@id="mainbody"]/form/table[2]/tbody/tr[6]/td[2]').text
              print(birth)
            except:
              birth = ''
            try:
              a = self.driver.find_element(By.XPATH, f'//*[@id="mainbody"]/form/table[2]/tbody/tr[7]/td[2]').text.split(" ")
              number = a[0]
              adress = a[1] + " " + a[2] 
              print(number)
              print(adress)
            except:
              number = ''
              adress = ''
            
            try:
              start = self.driver.find_element(By.XPATH, f'//*[@id="mainbody"]/form/table[3]/tbody/tr[6]/td[2]').text
              print(start)
            except:
              start = ''

            #year = start[-4:-1]

            print('----------')
            
            #Adding all item fields to the csv file as a line
            line = [title, forename, surname, birth, number, adress, start]   
            self.Sleep()
            wr.writerow(line)
            
            self.Render()

            #Getting out to return to property list page

            self.driver.implicitly_wait(self.impicitlyWaitTime)
            back_btn = self.driver.find_element(By.XPATH, '//*[@id="mainbody"]/form/p/input[3]')
            ActionChains(self.driver).move_to_element(back_btn).click().perform()
            self.Sleep()

           i = i + 1
           self.driver.implicitly_wait(self.impicitlyWaitTime)
           next_page = self.driver.find_element(By.XPATH, f'//*[@id="mainbody"]/a[text()="{i}"]')
           ActionChains(self.driver).move_to_element(next_page).click().perform()
           self.Sleep()

          file.close()


if __name__ == '__main__':
  scraper = Insolvency_List_UK_Scraper()
  scraper.Search_By_Surname()
  scraper.Extract_Results()
