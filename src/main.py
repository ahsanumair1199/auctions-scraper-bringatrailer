from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
from bringatrailer.settings import driver
from constants.target import URL
import time
import csv
import re
import os
# END IMPORTS


driver.get(URL)

# WAIT FOR FILTERS ELEMENT
while 1:
    try:
        banner = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located(
            (By.XPATH, "/html/body/main/div[1]")))
        break
    except TimeoutException:
        continue

# # CLICK ON AUCTION RESULTS BUTTON
view_auction_results_btn = driver.find_element(
    By.XPATH, '/html/body/main/div[1]/h2/a')
view_auction_results_btn.click()
# body = driver.find_element(By.TAG_NAME, 'body')
# body.send_keys(Keys.END)

total_auction_results = driver.find_element(
    By.XPATH, "/html/body/main/div[6]/div/div[1]/div/div[3]/div[1]/span").text
total_auction_results = total_auction_results.split(' ')[0]
print('TOTAL AUCTION RESULTS: ', total_auction_results)

# WAIT FOR AUCTIONS CARDS ELEMENTS
while 1:
    try:
        sales_page = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located(
            (By.XPATH, '/html/body/main/div[6]/div/div[2]/div[1]')))
        break
    except TimeoutException:
        continue


# LOAD ALL AUCTION CARDS
remaining_results = int(total_auction_results.replace(',', ''))
progress = 1


# CREATE CSV FILE
file_path = 'assets/data.csv'
if os.path.exists(file_path):
    os.remove(file_path)
with open(file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Year", "Make", "Model",
                    "Date of Sale", " Sold Price", "Type of Sale", "Source"])
    while remaining_results > 0:
        # ITERATE FOR 36 CARDS BEFORE SHOW MORE BUTTON
        for i in range(1, 37):
            print("REMAINING RESULTS: ", remaining_results)
            print("PROGRESS: ", progress)
            ###########################################################
            # Use ActionChains to open link in a new tab
            card = driver.find_element(
                By.XPATH, f'/html/body/main/div[6]/div/div[2]/div[1]/a[{progress}]/div[2]/div[1]/h3')
            title = card.text
            date_of_sale = ''
            date_of_sale = driver.find_element(
                By.XPATH, f'/html/body/main/div[6]/div/div[2]/div[1]/a[{progress}]/div[2]/div[1]/div[6]/span').text
            date_of_sale = date_of_sale.split(' ')[1]
            ActionChains(driver).key_down(Keys.CONTROL).click(
                card).key_up(Keys.CONTROL).perform()
            # Wait for the new tab to be opened
            driver.switch_to.window(driver.window_handles[1])
            year = ''
            year_pattern = re.compile(r'\b\d{4}\b')
            year = year_pattern.search(title)
            if year:
                year = year.group()
            else:
                year = ''

            # FILTERS
            make = ''
            model = ''
            era = ''
            origin = ''
            location = ''
            category = ''
            try:
                group_item_elements = driver.find_elements(
                    By.CLASS_NAME, "group-item-wrap")
            except WebDriverException:
                continue
            for group_item in group_item_elements:
                strong_tag = group_item.find_element(
                    By.CSS_SELECTOR, "strong.group-title-label")
                strong_text = strong_tag.text
                if strong_text == 'Make':
                    make = group_item.text.replace(strong_text, '')
                if strong_text == 'Model':
                    model = group_item.text.replace(strong_text, '')
                if strong_text == 'Era':
                    era = group_item.text.replace(strong_text, '')
                if strong_text == 'Origin':
                    origin = group_item.text.replace(strong_text, '')
                if strong_text == 'Location':
                    location = group_item.text.replace(strong_text, '')
                if strong_text == 'Category':
                    category = group_item.text.replace(strong_text, '')

            try:
                sold_price = driver.find_element(
                    By.XPATH, '/html/body/main/div[2]/div[2]/div[1]/div/div/div[1]/div[2]/div[1]/span[2]/strong').text
            except NoSuchElementException:
                sold_price = driver.find_element(
                    By.XPATH, '/html/body/main/div/div[2]/div[1]/div/div/div[1]/div[2]/div[1]/span[2]/strong').text
            try:
                type_of_sale = driver.find_element(
                    By.XPATH, '/html/body/main/div[2]/div[2]/div[1]/div/div/div[1]/div[1]/div/div/span').text
            except NoSuchElementException:

                type_of_sale = ''
            print('MAKE: ', make)
            print('MODEL: ', model)
            print('ERA: ', era)
            print('ORIGIN: ', origin)
            print('LOCATION: ', location)
            print('CATEGORY: ', category)
            print('DATE_OF_SALE: ', date_of_sale)
            print('YEAR: ', year)
            print('SOLD PRICE: ', sold_price)
            print('TYPE OF SALE: ', type_of_sale)
            print('SOURCE: ', driver.current_url)
            writer.writerow([title, year, make, model, date_of_sale,
                            sold_price, type_of_sale, driver.current_url])

            # Close the new tab
            # time.sleep(2)
            driver.close()
            # Switch back to the original tab
            driver.switch_to.window(driver.window_handles[0])
            ############################################################
            remaining_results -= 1
            progress += 1

        try:
            body = driver.find_element(By.TAG_NAME, 'body')
            body.send_keys(Keys.END)
            time.sleep(1)
            show_more_btn = driver.find_element(
                By.XPATH, '/html/body/main/div[6]/div/div[2]/div[2]/div/button')
            show_more_btn.click()
            time.sleep(3)
        except NoSuchElementException:
            if remaining_results <= 0:
                break


# # SCROLL UNTILL ALL AUCTION CARDS BECOME VISIBLE
# remaining_scrolls = int(total_live_auctions)
# body = driver.find_element(By.TAG_NAME, 'body')
# while 1:
#     body.send_keys(Keys.END)
#     remaining_scrolls -= 50
#     if remaining_scrolls < 0:
#         break
# body.send_keys(Keys.END)
# time.sleep(3)

# # CREATE CSV FILE
# file_path = 'assets/data.csv'
# if os.path.exists(file_path):
#     os.remove(file_path)
# with open(file_path, mode='w', newline='', encoding='utf-8') as file:
#     writer = csv.writer(file)
#     writer.writerow(["Title", "Description",
#                     "Bidding", "Time_Remaining", "Image_URL"])

#     # AUCTION CARD ELEMENTS
#     parent_container = driver.find_element(
#         By.CLASS_NAME, "listings-container.auctions-grid")
#     child_elements = parent_container.find_elements(
#         By.CLASS_NAME, "listing-card.bg-white-transparent")
#     # ITERATE THROUGH EACH AUCTION CARD ELEMENT
#     for i, child_element in enumerate(child_elements):
#         # THUMBNAIL
#         thumbnail = child_element.find_element(By.CLASS_NAME, 'thumbnail')
#         img_tag = thumbnail.find_element(By.TAG_NAME, "img")
#         img_src = img_tag.get_attribute("src")
#         # CONTENT
#         content = child_element.find_element(By.CLASS_NAME, 'content')
#         # CONTENT MAIN INSIDE CONTENT
#         content_main = content.find_element(By.CLASS_NAME, 'content-main')
#         heading3 = content_main.find_element(By.TAG_NAME, 'h3').text
#         # ITEM EXCERPT INSIDE CONTENT MAIN
#         item_exerpt = content_main.find_element(
#             By.CLASS_NAME, 'item-excerpt').text
#         # CONTENT SECONDARY INSIDE CONTENT
#         content_secondary = content.find_element(
#             By.CLASS_NAME, 'content-secondary')
#         # ITEM BIDDING INSIDE CONTENT SECONDARY
#         item_bidding = content_secondary.find_element(
#             By.CLASS_NAME, 'item-bidding')
#         # BIDDING BID INSIDE ITEM BIDDING
#         bidding_bid = item_bidding.find_element(
#             By.CLASS_NAME, 'bidding-bid').text
#         # BIDDING COUNTDOWN INSIDE ITEM BIDDING
#         bidding_countdown = item_bidding.find_element(
#             By.CLASS_NAME, 'bidding-countdown').text
#         # WRITE THE INFORMATION INTO CSV FILE
# writer.writerow([heading3, item_exerpt,
#                 bidding_bid, bidding_countdown, img_src])
#         print(i)


time.sleep(3)
driver.quit()
