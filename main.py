from selenium import webdriver
from tempfile import mkdtemp
from selenium.webdriver.common.by import By


def handler(event=None, context=None):

    url = 'https://www.asurascans.com/#'

    options = webdriver.ChromeOptions()
    options.binary_location = '/opt/chrome/chrome'
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280x1696")
    options.add_argument("--single-process")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-dev-tools")
    options.add_argument("--no-zygote")
    options.add_argument(f"--user-data-dir={mkdtemp()}")
    options.add_argument(f"--data-path={mkdtemp()}")
    options.add_argument(f"--disk-cache-dir={mkdtemp()}")
    options.add_argument("--remote-debugging-port=9222")
    browser = webdriver.Chrome("/opt/chromedriver",
                              options=options)
    browser.get(url)
    cards = browser.find_elements(By.CSS_SELECTOR, '.uta')

    print("cards: " + str(len(cards)))
    series = []

    for card in cards:
        print("beginning for loop")
        all_chaps = []

        title = card.find_element(By.CSS_SELECTOR, '.luf > a').get_attribute('title')
        series_link = card.find_element(By.CSS_SELECTOR, '.luf > a').get_attribute('href')
        img_link = card.find_element(By.CSS_SELECTOR, '.imgu > a > img').get_attribute('src')

        print("Got past basic card info: " + str(title))
        print(series_link)
        
        chap_list = None
        try:
            chap_list = card.find_element(By.CSS_SELECTOR, '.Manhwa')
        except:
            print("Wasn't a Manhwa")
        
        try:
            chap_list = card.find_element(By.CSS_SELECTOR, '.Manhua')
        except:
            print("Wasn't a Manhua")

        print("Got past try catch")

        chaps = chap_list.find_elements(By.TAG_NAME, 'li')

        for chap in chaps:
            time = chap.find_element(By.TAG_NAME, 'span').text
            chap_num = chap.find_element(By.TAG_NAME, 'a').text
            chap_link = chap.find_element(By.TAG_NAME, 'a').get_attribute('href')
            chap_obj = {
                "link": chap_link,
                "time": time,
                "chapter_number": chap_num
            }
            all_chaps.append(chap_obj)
        print("all_chaps: " + str(len(all_chaps)))
        print("Got past individual chaps")

        series_obj = {
            "scan_site": "Asura Scans",
            "title": title,
            "cover_img": img_link,
            "series_link": series_link,
            "chapters": all_chaps
        }
        series.append(series_obj)
        print("series_obj: " + series_obj)
    
    print("end: " + series)
    return series

    
