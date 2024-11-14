import os 
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import re
import csv
import time
from urllib.parse import urljoin
from webdriver_manager.chrome import ChromeDriverManager
from utils.get_image import get_image


class HookImage:
    base_url = "https://www.friendforpet.ru"
    
    def get_links(self, url):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        driver.get(url)
        time.sleep(5)

        existing_links = set()
        try:
            with open("pet_links.csv", mode="r", newline='') as pet_file:
                reader = csv.reader(pet_file)
                existing_links = set(row[0] for row in reader)
        except FileNotFoundError:
            pass 

        with open("pet_links.csv", mode="a", newline='') as pet_file:
            pet_writer = csv.writer(pet_file)

            pet_elements = driver.find_elements(By.XPATH, '//a[contains(@href, "/pet/")]')
            for element in pet_elements:
                pet_url = element.get_attribute('href')
                if pet_url not in existing_links: 
                    pet_writer.writerow([pet_url])
                    existing_links.add(pet_url)  
                    print(f"Pet link stored: {pet_url}")
                else:
                    print(f"Pet link already exists: {pet_url}")

        driver.quit()
        print("All links have been processed.")

    def get_link_image(self, url):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        driver.get(url)
        time.sleep(5)
        image_links = []

        try:
            current_pet_section = driver.find_element(By.CLASS_NAME, "current-pet-section")
            img_elements = current_pet_section.find_elements(By.XPATH, './/*[contains(@style, "/api/sites/default/files/")]')
            for element in img_elements:
                style = element.get_attribute('style')
                img_url_match = re.search(r'url\((.*?)\)', style)
                if img_url_match:
                    img_url = img_url_match.group(1).strip('"').strip("'")
                    full_img_url = urljoin(url, img_url)
                    if full_img_url not in image_links:
                        image_links.append(full_img_url)

            for link in image_links:
                self.save_image(link, url)

        except Exception as e:
            print(f"An error occurred: {e}")

        driver.quit()
        print("Finished processing image links.")
        return True


    def save_image(self, url_image, base_url):
        number = base_url.rstrip('/').split('/')[-1]
        return get_image(url_image, number)


    def process_and_move_first_item(self, source_file="pet_links.csv", destination_file="done_links.csv"):
        with open(source_file, mode='r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)

        if not rows:
            print("The source file is empty.")
            return

        first_item = rows[0]

        if self.get_link_image(first_item[0]):  # assuming first_item contains only one URL as the first column
            with open(destination_file, mode='a', newline='') as csv_dest:
                writer = csv.writer(csv_dest)
                writer.writerow(first_item)

            rows.pop(0)

            with open(source_file, mode='w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(rows)

            print("Item moved successfully.")
        else:
            print("Condition not met, item not moved.")

    def get_from_page_links(self, json_file="current_page.json"):
        if os.path.exists(json_file):
            with open(json_file, 'r') as f:
                data = json.load(f)
                current_page = data.get("current_page", 1)
        else:
            current_page = 1
            
        for i in range(current_page, 398):
            self.get_links(f"{self.base_url}/pets/dogs?page={i}")
            
            with open(json_file, 'w') as f:
                json.dump({"current_page": i + 1}, f)

        print("Completed processing all pages.")
        self.check_and_process_pet_links()
        


    def check_and_process_pet_links(self, file_path="pet_links.csv"):
        while True:
            try:
                with open(file_path, mode='r', newline='') as csvfile:
                    reader = csv.reader(csvfile)
                    rows = list(reader)

                if rows:
                    print(f"Found {len(rows)} links in {file_path}.")
                    self.process_and_move_first_item()
                else:
                    print("No data found in the file.")
                    return False
                
            except FileNotFoundError:
                print(f"The file {file_path} does not exist.")
                return False
            except Exception as e:
                print(f"An error occurred: {e}")
                return False

if __name__ == "__main__":
    HookImage().get_from_page_links()