from datetime import datetime
from dotenv import dotenv_values
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException
from tinydb import TinyDB, Query
from urllib.parse import urlencode, urlparse, parse_qs, urlunparse


def report_scraper(link: str) -> list:
    # Open the page in the Chrome browser
    driver.get(link)

    single_page_reports_finder = ec.presence_of_all_elements_located(
        (By.CSS_SELECTOR, "div.card.catch-return")
    )

    report_list = WebDriverWait(driver=driver, timeout=10).until(method=single_page_reports_finder)

    return_report_list = list()

    # Iterate over the reports and extract relevant data
    for report in report_list:
        # Extract relevant data from the report
        angler = report.find_element(by=By.CSS_SELECTOR, value=".card.catch-return .heading p:nth-of-type(2)").text
        date_text = report.find_element(by=By.CSS_SELECTOR, value=".card.catch-return .heading .date").text

        # Modify the text to remove "(3 days ago)"
        if date_text:
            # Use split to remove everything in parentheses, keeping only the date part
            date_text = date_text.split(' (')[0].strip()

        # Parse the date text, ignoring the day name (e.g., "31 October 2024")
        try:
            date_obj = datetime.strptime(date_text, "%A %d %B %Y")
            day = date_obj.day
            month = date_obj.strftime('%B')  # Get full month name
            year = date_obj.year
            
        except ValueError:
            day = 0
            month = 0
            year = 0

        # Extract additional data from the report
        try:
            area_full_text = report.find_element(by=By.CSS_SELECTOR, value=".card.catch-return .heading p:nth-of-type(4)").text
            area_text_should_remove = report.find_element(by=By.CSS_SELECTOR, value=".card.catch-return .heading p:nth-of-type(4) span.text-muted").text
            area = area_full_text.replace(area_text_should_remove, "").strip()
        except NoSuchElementException as exception:
            print("Area Not Found")
            area = "Not Found (Please Check manually)"

        try:
            beat_full_text = report.find_element(by=By.CSS_SELECTOR, value=".card.catch-return .heading div.row p:nth-of-type(1)").text
            beat_text_should_remove = report.find_element(by=By.CSS_SELECTOR, value=".card.catch-return .heading div.row p:nth-of-type(1) span.text-muted").text
            beat = beat_full_text.replace(beat_text_should_remove, "").strip()

        except NoSuchElementException as exception:
            print("Beat Not Found")
            beat = "Not Found (Please Check manually)"

        try:
            fishing_full_text = report.find_element(by=By.CSS_SELECTOR, value=".card.catch-return .heading div.row p:nth-of-type(2)").text
            fishing_text_should_remove = report.find_element(by=By.CSS_SELECTOR, value=".card.catch-return .heading div.row p:nth-of-type(2) span.text-muted").text
            fishing = fishing_full_text.replace(fishing_text_should_remove, "").strip()
        except NoSuchElementException as exception:
            print("Fishing Not Found")
            fishing = "Not Found (Please Check manually)"

        try:
            no_of_anglers_full_text = report.find_element(by=By.CSS_SELECTOR, value=".card.catch-return .heading div.row p:nth-of-type(3)").text
            no_of_anglers_text_should_remove = report.find_element(by=By.CSS_SELECTOR, value=".card.catch-return .heading div.row p:nth-of-type(3) span.text-muted").text
            no_of_anglers = no_of_anglers_full_text.replace(no_of_anglers_text_should_remove, "").strip()
        except NoSuchElementException as exception:
            print("Number of Anglers Not Found")
            no_of_anglers = "Not Found (Please Check manually)"

        try:
            id_full_text = report.find_element(by=By.CSS_SELECTOR, value=".card.catch-return .heading p.pull-right").text
            id_text_should_remove = report.find_element(by=By.CSS_SELECTOR, value=".card.catch-return .heading p.pull-right span.text-muted").text
            id_ = id_full_text.replace(id_text_should_remove, "").strip()
        except NoSuchElementException as exception:
            print("ID Not Found")
            id_ = "Not Found (Please Check manually)"

        # Extract additional data from the report
        comment = report.find_element(by=By.CSS_SELECTOR, value=".card.catch-return > p:not(.fishing-list)").text

        # Extract additional data from the report
        _fishing_list = report.find_element(by=By.CSS_SELECTOR, value=".card.catch-return > p.fishing-list").text.strip()

        barbel = None
        chub = None
        pike = None
        trout = None
        grayling = None
        other = None

        try:
            _fishing_list = _fishing_list.split(',')

            for _fishing in _fishing_list:
                _fishing = _fishing.strip().lower()

                if _fishing.__contains__('barbel'):
                    barbel = _fishing.replace("barbel", "").strip()

                if _fishing.__contains__('chub'):
                    chub = _fishing.replace("chub", "").strip()

                if _fishing.__contains__('pike'):
                    pike = _fishing.replace("pike", "").strip()

                if _fishing.__contains__('trout'):
                    trout = _fishing.replace("trout", "").strip()

                if _fishing.__contains__('grayling'):
                    grayling = _fishing.replace("grayling", "").strip()

                if _fishing.__contains__('other'):
                    other = _fishing.replace("other", "").strip()

        except ValueError:
            _fishing_list = []

        data = {
            "Angler": angler,
            "Date": date_text,
            "Day": day,
            "Month": month,
            "Year": year,
            "Area": area,
            "Beat": beat,
            "Fishing": fishing,
            "No. of Anglers": no_of_anglers,
            "__ID": id_,
            "Comment": comment,
            "# Barbel": barbel,
            "# Chub": chub,
            "# Pike": pike,
            "# Trout": trout,
            "# Grayling": grayling,
            "# Other": other,
            "Page URL": link,
        }

        return_report_list.append(data)

    return return_report_list




if __name__ == "__main__":
    # Load environment variables from.env file
    env_vars = dotenv_values(".env")

    # Set up TinyDB database
    db = TinyDB('fishing_reports.json')
    Query = Query()

    # Set up the Chrome WebDriver
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless")
    driver = Chrome(options=chrome_options, executable_path=env_vars["CHROMEDRIVER_PATH"])

    # visit initial page 
    driver.get(env_vars['BASE_URL'])

    from_page = int(env_vars['START_PAGE'])
    to_page = int(env_vars['END_PAGE'])

    # Parse the url into componets
    url_parts = urlparse(env_vars['PAGE_URL'])


    for page_number in range(from_page, to_page + 1):
        print(f"Page number: {page_number}")

        # Convert query parameters to a dictionary and add/modify 'page'
        query_params = parse_qs(url_parts.query)
        query_params['page'] = [page_number]  # Adding or updating the 'page' parameter

        # Reconstruct the URL with updated query parameters
        new_query = urlencode(query_params, doseq=True)
        new_url = urlunparse((url_parts.scheme, url_parts.netloc, url_parts.path, url_parts.params, new_query, url_parts.fragment))

        report_list = report_scraper(new_url)

        for report in report_list:
            if not db.contains(Query.__ID == report['__ID']):
                db.insert(report)
                print("New report added")
            else:
                print("Report already exists")
