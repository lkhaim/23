'''
23andMe_online_purchase_smoke_test.py

Page under test: https://store.23andme.com/en-us/cart/

Test steps:
1. Add 3 health+ancestry and 2 ancestry only kits to the cart
   and verify that the kit count was correctly updated.
2. Give unique names to the kits
   and verify that they has been successfully recorded.
3. Add shipping info and check that VT -> CA correction
   has been done during verification.
4. Continue to the payment page and verify that it was reached.
'''

import unittest
import sys, logging, re, time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

class OnlinePurchaseSmoke(unittest.TestCase):

    def setUp(self):
        ''' Set up Selenium driver and open the page to test. '''

        path_to_chromedriver = 'C:\\Users\\Leon\\AppData\\Local\\Programs' + \
          '\\Python\\Python35\\Lib\\site-packages\\selenium\\chromedriver' + \
          '\\chromedriver.exe'
        implct_timeout = 10 # seconds for implicit wait

        # create an instance of chromedriver
        self.driver = webdriver.Chrome(path_to_chromedriver)
        # set implicit wait to 'timeout' seconds
        self.driver.implicitly_wait(implct_timeout)

    def test(self):
        ''' Add kits, name them, add ship info, go to payment page. Verify. '''

        # test parameters
        explct_timeout = 10 # seconds for explicit waits
        page_to_start = 'https://store.23andme.com/en-us/cart/'
        ha_n = 3 # number of health+ancestry kits to order
        a_n = 2 # number of ancestry only kits to order
        add_bttn_xpath = "//span[@class='quantity-control-button"
        ha_add_bttn_xpath = add_bttn_xpath + " js-add-kit']"
        ha_count_id = 'text-health-kit-count'
        a_add_bttn_xpath = add_bttn_xpath + " js-add-ancestry-kit']"
        a_count_id = 'text-ancestry-kit-count'
        kit_names_xpath = "//input[@class='js-kit-name']"
        continue_bttn_xpath = "//input[@type='submit'][@value='continue']"
        addrs_sggstn_xpath = "//div[@class='verify suggestion']" + \
                             "/div[@class='address']"
        addrs_sggstn_expected = 'AntoshkaKartoshkaKolhoz6040BONNYDOONRD,' + \
                                'PECHKA-BURZHUJKASANTACRUZ,CA95060-9714US'
        cont_to_pmnt_bttn_xpath = "//input[@type='submit'][@name='verified']"
        pmnt_page_url = 'https://store.23andme.com/en-us/payment/'
        ship_info = {'id_first_name' : 'Antoshka',
                     'id_last_name' : 'Kartoshka',
                     'id_company' : 'Kolhoz',
                     'id_address' : '6040 Bonny Doon Road',
                     'id_address2' : 'pechka-burzhujka',
                     'id_city' : 'Santa Cruz',
                     'id_state' : 'v',
                     'id_postal_code' : 95060,
                     'id_country' : 'USA',
                     'id_shipping_method' : 'e',
                     'id_email' : 'lk31415926@yahoo.com',
                     'id_int_phone' : 4089106233
                     }

        # create local variable to reduce typing
        driver = self.driver
        # create explicit wait object
        explct_wait = WebDriverWait(driver, explct_timeout)
        # open the page to test
        driver.get(page_to_start)

        print('\n') # added for output formatting purposes
        logging.info("The ordering page is opened.")
        
        print_text = "Adding %d health+ancestry and %d ancestry only kits."
        logging.info(print_text %(ha_n, a_n))

        # create button objects to add health+ancestry and ancestry only kits
        ha_add_button = driver.find_element_by_xpath(ha_add_bttn_xpath)
        a_add_button = driver.find_element_by_xpath(a_add_bttn_xpath)

        # add health+ancestry kits
        for i in range(1, ha_n+1):
            ActionChains(driver).click(ha_add_button).perform()
            explct_wait.until(EC.text_to_be_present_in_element \
                              ((By.ID, ha_count_id), str(i)))

        # add ancestry only kits
        for i in range(1, a_n+1):
            ActionChains(driver).click(a_add_button).perform()
            explct_wait.until(EC.text_to_be_present_in_element \
                              ((By.ID, a_count_id), str(i)))
        
        # give unique names to kits
        kit_name_prefix = 'customer#'
        logging.info("Giving %sn names to kits." %kit_name_prefix)
        kits = driver.find_elements_by_xpath(kit_names_xpath)
        kit_names = []
        
        for i, kit in enumerate(kits, start = 1):
            kit_name = kit_name_prefix + str(i)
            kit.send_keys(kit_name)
            kit_names.append(kit_name)

        # wait for "continue" button to become clickable after names are added
        explct_wait.until(EC.element_to_be_clickable \
                          ((By.XPATH, continue_bttn_xpath)))

        # verify that correct number of kits was added
        ha_counter = driver.find_element_by_id(ha_count_id)
        a_counter = driver.find_element_by_id(a_count_id)

        ha_count = ha_counter.get_attribute('innerText')
        a_count = a_counter.get_attribute('innerText')

        self.assertEqual(ha_count, str(ha_n))
        self.assertEqual(a_count, str(a_n))

        print_text = "%s health+ancestry and " + \
                     "%s ancestry only kits have been added."
        logging.info(print_text %(ha_count, a_count))

        # verify that names were correctly assigned
        kit_names_recorded =[]
        for i, kit in enumerate(kits):
            kit_names_recorded.append(kit.get_attribute('value'))
        self.assertEqual(kit_names_recorded, kit_names)

        print_text = "Kits has been successfully assigned %sn names."
        logging.info(print_text %kit_name_prefix)

        # continuing to shipping info input page
        self._pressContinue_(continue_bttn_xpath, explct_wait)
        logging.info("Continuing to shipping info input page.")

        # entering shipping info into the fields
        keys = list(ship_info.keys())
        for key in keys:
            destination = driver.find_element_by_id(key)
            destination.send_keys(ship_info[key])

        # continuing to shipping info verification page
        self._pressContinue_(continue_bttn_xpath, explct_wait)
        logging.info("Continuing to shipping info verification page.")

        # verify that VT -> CA correction was done during address verification
        addrs_sggstn = driver.find_element_by_xpath(addrs_sggstn_xpath)
        addrs_sggstn_txt = addrs_sggstn.get_attribute('textContent')
        addrs_sggstn_cmprsd = re.sub('[\s+]', '', addrs_sggstn_txt)
        self.assertEqual(addrs_sggstn_cmprsd, addrs_sggstn_expected)

        logging.info("Correct verified address has been suggested (VT -> CA).")

        # continuing to payment page
        self._pressContinue_(cont_to_pmnt_bttn_xpath, explct_wait)
        logging.info("Continuing to payment page.")

        # verifying that the payment page has been reached
        crrnt_page_url = driver.current_url
        self.assertEqual(crrnt_page_url, pmnt_page_url)
        
        logging.info("Payment page has been reached. Testing is completed.")

        return 1

    def _pressContinue_(self, continue_bttn_xpath, explct_wait):
        ''' Presses CONTINUE button on the bottom of the page. '''

        # create local variable to reduce typing
        driver = self.driver

        # create button object
        continue_button = driver.find_element_by_xpath(continue_bttn_xpath)
        # scroll to the bottom of the page to make the button clickable
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # because explct_wait.until(EC.visibility_of(continue_button))
        # doesn't work
        time.sleep(2)
        # press the button
        continue_button.click()
        # wait until an element of the previous page becomes stale
        explct_wait.until(EC.staleness_of(continue_button))

        return 1

    def tearDown(self):
        ''' Cleaning up by closing Selenium driver. '''

        #close the Selenium driver
        self.driver.quit()
        
        return 1

if __name__ == '__main__':
    unittest.main()