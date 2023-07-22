from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.support import expected_conditions as EC
import selenium.common.exceptions as Exceptions
import pandas as ps
import time

METRO_GOVERN_ADDRESS_KEY = "metro_government"
BASE_GOVERN_ADDRESS_KEY = "base_government"
CITY_ADDRESS_KEY = "city"
TOWN_ADDRESS_KEY = "town"
ROAD_ADDRESS_KEY = "road_name"
DETAIL_ADDRESS_KEY = "detail"

def sleep(second):
    time.sleep(second)
    

chrome_options = Options()
chrome_options.add_argument("--headless")
# driver = webdriver.Chrome(options=chrome_options)
driver = webdriver.Chrome()

driver.get("https://map.naver.com/v5/search")

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

def to_next_page():
    left_or_right = driver.find_elements(By.CLASS_NAME, "eUTV2")
    for button in left_or_right:
        if button.find_element(By.TAG_NAME, "span").text == "다음페이지":
            right_button = button
            if right_button.get_attribute("aria-disabled") == "false":
                right_button.click()
                return True
            
    return False

def analyze_address(address):
    
    address_list = address.split()

    address_dict = dict()
    address_dict[METRO_GOVERN_ADDRESS_KEY] = address_list[0]
    address_dict[BASE_GOVERN_ADDRESS_KEY] = None
    address_dict[CITY_ADDRESS_KEY] = None
    address_dict[TOWN_ADDRESS_KEY] = None
    address_dict[ROAD_ADDRESS_KEY] = None
    address_dict[DETAIL_ADDRESS_KEY] = None

    metro = address_list[0]
    if metro == "세종":
        return analyze_sejong(address_list, address_dict)
    elif metro in ["제주", "강원"]:
        return analyze_jeju(address_list, address_dict)
    elif metro in ["부산", "인천", "대구", "광주", "대전", "울산"]:
        return analyze_guangyuksi(address_list, address_dict)
    elif metro in ["경기", "충북", "충남", "전북", "전남", "경북", "경남"]:
        return analyze_do(address_list, address_dict)
    elif metro in "서울":
        return analyze_teugbyeolsi(address_list, address_dict)

def analyze_sejong(address_list, address_dict):

    for word in address_list[1:]:
        if word.endswith("읍") or word.endswith("면"):
            address_dict[TOWN_ADDRESS_KEY] = word
        elif word.endswith("길") or word.endswith("리") or word.endswith("로"):
            address_dict[ROAD_ADDRESS_KEY] = word
        else:
            if address_dict[DETAIL_ADDRESS_KEY] is None:
                address_dict[DETAIL_ADDRESS_KEY] = word
            else:
                address_dict[DETAIL_ADDRESS_KEY] += " " + word

    return address_dict

def analyze_jeju(address_list, address_dict):

    for word in address_list[1:]:
        if word.endswith("시"):
            address_dict[CITY_ADDRESS_KEY] = word

        elif word.endswith("읍") or word.endswith("면"):
            address_dict[TOWN_ADDRESS_KEY] = word
        elif word.endswith("길") or word.endswith("리") or word.endswith("로"):
            address_dict[ROAD_ADDRESS_KEY] = word
        else:
            if address_dict[DETAIL_ADDRESS_KEY] is None :
                address_dict[DETAIL_ADDRESS_KEY] = word
            else:
                address_dict[DETAIL_ADDRESS_KEY] += " " + word

    return address_dict

def analyze_guangyuksi(address_list, address_dict):
    for word in address_list[1:]:
        if word.endswith("구") or word.endswith("군"):
            address_dict[BASE_GOVERN_ADDRESS_KEY] = word
        elif word.endswith("읍") or word.endswith("면"):
            address_dict[TOWN_ADDRESS_KEY] = word
        elif word.endswith("길") or word.endswith("리") or word.endswith("로"):
            address_dict[ROAD_ADDRESS_KEY] = word
        else:
            if address_dict[DETAIL_ADDRESS_KEY] is None:
                address_dict[DETAIL_ADDRESS_KEY] = word
            else:
                address_dict[DETAIL_ADDRESS_KEY] += " " + word

    return address_dict

def analyze_do(address_list, address_dict):
    for word in address_list[1:]:
        if word.endswith("시") or word.endswith("군"):
            address_dict[BASE_GOVERN_ADDRESS_KEY] = word
        elif word.endswith("구"):
            address_dict[CITY_ADDRESS_KEY] = word
        elif word.endswith("읍") or word.endswith("면"):
            address_dict[TOWN_ADDRESS_KEY] = word
        elif word.endswith("길") or word.endswith("리") or word.endswith("로"):
            address_dict[ROAD_ADDRESS_KEY] = word
        else:
            if address_dict[DETAIL_ADDRESS_KEY] is None:
                address_dict[DETAIL_ADDRESS_KEY] = word
            else:
                address_dict[DETAIL_ADDRESS_KEY] += " " + word

    return address_dict

def analyze_teugbyeolsi(address_list, address_dict):

    for word in address_list[1:]:
        if word.endswith("구"):
            address_dict[BASE_GOVERN_ADDRESS_KEY] = word
        elif word.endswith("길") or word.endswith("리") or word.endswith("로"):
            address_dict[ROAD_ADDRESS_KEY] = word
        else:
            if address_dict[DETAIL_ADDRESS_KEY] is None:
                address_dict[DETAIL_ADDRESS_KEY] = word
            else:
                address_dict[DETAIL_ADDRESS_KEY] += " " + word

    return address_dict

def collapse_day(operation_time_dict):
    result = ""
    for key in operation_time_dict.keys():
        result += operation_time_dict[key] + " " + key + "  "
    
    return result
    # for value in operation_time_dict.values():
        # day_list = value.split()
        
def operating_day_to_dict(book_store_time_days, book_store_time_hours, book_store_closed_days):
    operating_dict = dict()
    for i in range(len(book_store_time_days)):
        hour = book_store_time_hours[i].text
        day = book_store_time_days[i].text
        if "정기휴무" in hour or "정보없음" in hour:
            if book_store_closed_days == None:
                book_store_closed_days = day + " "
            else: book_store_closed_days += day + " "
            continue 

        if "\n" in hour:
            index = hour.index("""\n""")
            hour = hour[:index]
        else:
            if hour not in operating_dict:
                operating_dict[hour] = day
            else:
                operating_dict[hour] += " " + day

    return collapse_day(operating_dict), book_store_closed_days

def get_image():
    try:
        picture_style = driver.find_element(By.ID, "ibu_1").get_attribute("style")
        index = picture_style.index("url(\"")
        index_end = picture_style.index("\");");
        return picture_style[index+5:index_end]
    except Exception:
        return None


metro_list = ['서울', '부산', '인천', '대구', '광주', '대전', '울산', '세종', '경기도', '충청북도', '충청남도', '전라북도', '전라남도', '경상북도', '경상남도', '강원', '제주']
space_dict_list = []

def main():
    try:

        book_stores = list()

        for i in range(10):
            book_stores = driver.find_elements(By.CLASS_NAME, "place_bluelink")            last_book_store = book_stores[-1]
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
                book_store_location = None
                
            book_store_closed_days=None
            book_store_time=None
            try: # 영업 시간 토글 있을 때
                book_store_time_div = driver.find_element(By.CLASS_NAME, "O8qbU.pSavy")
                book_store_time_toggle_span = book_store_time_div.find_element(By.CLASS_NAME, "_UCia")
                book_store_time_toggle_span.find_element(By.CLASS_NAME, "DNzQ2").click()

                book_store_time_days = driver.find_elements(By.CLASS_NAME, "i8cJw")
                book_store_time_hours = driver.find_elements(By.CLASS_NAME, "H3ua4")

                book_store_time, book_store_closed_days = operating_day_to_dict(book_store_time_days, book_store_time_hours, book_store_closed_days)

            # 영업 시간 토글 없을 때
            except Exceptions.NoSuchElementException:
                try:
                    book_store_time = driver.find_element(By.CLASS_NAME, "U7pYf").text
                except Exceptions.NoSuchElementException:
                    # book_store_time = "null"
                    book_store_time = None

            try:
                book_store_phone = driver.find_element(By.CLASS_NAME, "xlx7Q").text
            except Exceptions.NoSuchElementException:
                book_store_phone = "null"
            
            space = {'name': book_store_title, 'closed_days': book_store_closed_days, 'operating_time': book_store_time, 'road_address': "삭제 예정", 'type': '독립서점', 'image_url': get_image()}
            space.update(analyze_address(book_store_location))

            space_dict_list.append(space)
            print(space_dict_list[-1])

            driver.switch_to.default_content()
            switch_frame(frame_id="searchIframe")

        if to_next_page():
            main()

    except Exceptions.NoSuchElementException:
        print("ERROR: element 검색 실패")
        
    finally:
        pass

    driver.quit()
    return space_dict_list

def search(metro_list):
    # try: 
    # for metro in metro_list:
    driver.find_element(By.CLASS_NAME, "link_navbar.home").click()
    sleep(3)

    input = driver.find_element(By.CLASS_NAME, "input_search")
    input.click()
    # input.send_keys(metro + " 독립서점")
    input.send_keys("서울" + " 독립서점")
    input.send_keys(Keys.RETURN)

    sleep(3)

    switch_frame(frame_id="searchIframe")

    space_list = main()
    df = ps.DataFrame(data=space_list)
    # df.to_excel("test.xlsx", index=False, encoding='utf8')
    df.to_csv("test.csv", index = False, encoding='utf8')
    # except Exceptions.NoSuchElementException:
        # print("ERROR: element 검색 실패")

    # for metro in metro_list:


search(metro_list)