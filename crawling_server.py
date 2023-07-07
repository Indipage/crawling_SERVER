from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import selenium.common.exceptions as Exceptions
import time

def sleep(second):
    time.sleep(second)
    
chrome_options = Options()
chrome_options.add_argument("--headless")
# driver = webdriver.Chrome(options=chrome_options)
driver = webdriver.Chrome()

driver.get("https://map.naver.com/v5/search/독립서점")

sleep(5)

    
def switch_frame(frame_id):
    try:
        search_iframe = driver.find_element(By.ID, value=frame_id)
        driver.switch_to.frame(search_iframe)

    except Exceptions.NoSuchElementException:
        print("ERROR: 프레임 검색 실패")
    except Exceptions.NoSuchFrameException:
        print("ERROR: 프레임 전환 실패")

def scroll_down(height):
    try:
        last_height=driver.execute_script("return document.body.scrollHeight")

        driver.execute_script(f"window.scrollTo(0, {height});")
        new_height=driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            return -1
    except Exception:
        pass

switch_frame(frame_id="searchIframe")

try:
    book_stores = list()

    for i in range(10):
        book_stores = driver.find_elements(By.CLASS_NAME, "place_bluelink")

        last_book_store = book_stores[-1]
        action = ActionChains(driver)
        action.move_to_element(last_book_store).perform()
        
    print(len(book_stores))
    
    for book_store in book_stores:

        book_store.click()
        sleep(5)

        driver.switch_to.default_content()
        switch_frame(frame_id="entryIframe")

        book_store_title = driver.find_element(By.CLASS_NAME, "Fc1rA").text

        try:
            book_store_location = driver.find_element(By.CLASS_NAME, "LDgIH").text
        except Exceptions.NoSuchElementException:
            book_store_location = "null"
            
        book_store_closed_days=""
        book_store_time=""
        try: # 영업 시간 토글 있을 때
            book_store_time_div = driver.find_element(By.CLASS_NAME, "O8qbU.pSavy")
            book_store_time_toggle_span = book_store_time_div.find_element(By.CLASS_NAME, "_UCia")
            book_store_time_toggle_span.find_element(By.CLASS_NAME, "DNzQ2").click()

            book_store_time_days = driver.find_elements(By.CLASS_NAME, "i8cJw")
            book_store_time_hours = driver.find_elements(By.CLASS_NAME, "H3ua4")

            for i in range(len(book_store_time_days)):
                if "정기휴무" in book_store_time_hours[i].text:
                    book_store_closed_days += book_store_time_days[i].text + " "
                else:
                    book_store_time += book_store_time_days[i].text + "-> " + book_store_time_hours[i].text + " "

        # 영업 시간 토글 없을 때
        except Exceptions.NoSuchElementException:
            try:
                book_store_time = driver.find_element(By.CLASS_NAME, "U7pYf").text
            except Exceptions.NoSuchElementException:
                book_store_time = "null"
                    

        try:
            book_store_phone = driver.find_element(By.CLASS_NAME, "xlx7Q").text
        except Exceptions.NoSuchElementException:
            book_store_phone = "null"

        if not book_store_closed_days:
            book_store_closed_days = "null"
            
        print(f"서점 이름: {book_store_title}, 주소: {book_store_location}, 운영시간: {book_store_time}, 휴무일: {book_store_closed_days}, 번호: {book_store_phone}")

        driver.switch_to.default_content()
        switch_frame(frame_id="searchIframe")


except Exceptions.NoSuchElementException:
    print("ERROR: element 검색 실패")
    
finally:
    pass


driver.quit()
