# Scraper to extract data from the MyScheme portal

import os
import json
import copy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class MySchemeDataExtractor:
    def __init__(self):
        self.base_url = "https://rules.myscheme.in/"

    def fetch_scheme_overview(self):
        browser = webdriver.Firefox()
        browser.get(self.base_url)

        WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.ID, "__next")))

        table_body = browser.find_element(By.ID, "__next").find_element(By.TAG_NAME, "tbody")
        rows = table_body.find_elements(By.TAG_NAME, "tr")

        schemes = []
        for row in rows:
            columns = row.find_elements(By.TAG_NAME, "td")
            scheme_info = {
                'sr_no': columns[0].text,
                'scheme_name': columns[1].text.replace('\nCheck Eligibility', ''),
                'scheme_link': columns[2].find_element(By.TAG_NAME, "a").get_attribute("href")
            }
            schemes.append(scheme_info)

        browser.quit()
        return schemes

    def fetch_detailed_scheme_info(self, schemes):
        for scheme in schemes:
            driver = webdriver.Firefox()
            driver.get(scheme['scheme_link'])

            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "__next")))

            try:
                tag_container = driver.find_element(By.XPATH, '/html/body/div/main/div[3]/div[1]/div/div/div[2]/div/div[1]/div[2]/div[1]/div/div[2]/div[1]')
                scheme['tags'] = [div.text for div in tag_container.find_elements(By.TAG_NAME, 'div')]
            except Exception:
                scheme['tags'] = []

            def safe_get_text(element_id):
                try:
                    return driver.find_element(By.ID, element_id).text
                except:
                    return ""

            scheme['details'] = safe_get_text('details')
            scheme['benefits'] = safe_get_text('benefits')
            scheme['eligibility'] = safe_get_text('eligibility')
            scheme['application_process'] = safe_get_text('applicationProcess')
            scheme['documents_required'] = safe_get_text('documentsRequired')

            driver.quit()

    def scrape_all(self):
        all_schemes = self.fetch_scheme_overview()
        self.fetch_detailed_scheme_info(all_schemes)
        return all_schemes

    def merge_scraped_with_existing(self, scraped_data):
        with open('myScheme-data.json', 'r') as file:
            existing_data = json.load(file)['hits']['hits']

        individual_types = ['Individual', 'Family', 'Sportsperson', 'Journalist']

        filtered_data = [
            item for item in existing_data
            if any(beneficiary in individual_types for beneficiary in item['_source'].get('targetBeneficiaries', []))
        ]

        fields_of_interest = [
            'schemeShortTitle', 'schemeCategory', 'schemeSubCategory', 'gender', 'minority',
            'beneficiaryState', 'residence', 'caste', 'disability', 'occupation',
            'maritalStatus', 'education', 'age', 'isStudent', 'isBpl'
        ]

        structured_lookup = {
            entry['_source']['schemeName'].lower().strip(): entry['_source']
            for entry in filtered_data
        }

        merged_schemes = []
        for scheme in scraped_data:
            match = structured_lookup.get(scheme['scheme_name'].lower().strip())
            if match:
                additional_info = {key: value for key, value in match.items() if key in fields_of_interest}
                scheme.update(additional_info)
            merged_schemes.append(copy.deepcopy(scheme))

        return merged_schemes

if __name__ == "__main__":
    base_path = os.path.dirname(__file__)
    raw_output = os.path.join(base_path, 'myschemes_scraped_apr26.json')

    scraper = MySchemeDataExtractor()
    scraped_data = scraper.scrape_all()

    with open(raw_output, 'w') as f:
        json.dump(scraped_data, f)

    # If you want to combine with provided structured data
    combined_output = os.path.join(base_path, 'myschemes_scraped_combined_apr26.json')
    merged_data = scraper.merge_scraped_with_existing(scraped_data)

    with open(combined_output, 'w') as f:
        json.dump(merged_data, f)
