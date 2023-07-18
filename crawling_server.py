from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.support import expected_conditions as EC
import selenium.common.exceptions as Exceptions
import time

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

    # TODO("페이지네이션 버튼 변경 (> 버튼 누르면 됨)")
    # TODO("> 버튼 활성화 되어 있을 떄: <a>클래스는 eUTV2만 비활성화시 Y89AQ도 같이")

    return 0

def analyze_address(address):
    
    address_list = address.split()

    metro = address_list[0]
    if metro == "세종":
        return analyze_sejong(address_list)
    elif metro == "제주":
        return analyze_jeju(address_list)
    elif metro in ["부산", "인천", "대구", "광주", "대전", "울산"]:
        return analyze_guangyuksi(address_list)
    elif metro in ["경기", "충북", "충남", "전북", "전남", "경북", "경남"]:
        return analyze_do(address_list)
    elif metro in "서울":
        return analyze_teugbyeolsi(address_list)

def analyze_sejong(address_list):
    address_dict = dict()
    address_dict["metro"] = address_list[0]
    address_dict["basic"] = "null"
    address_dict["city"] = "null"
    address_dict["town"] = "null"
    address_dict["road"] = "null"
    address_dict["detail"] = "null"

    for word in address_list[1:]:
        if word.endswith("읍") or word.endswith("면"):
            address_dict["town"] = word
        elif word.endswith("길") or word.endswith("리") or word.endswith("로"):
            address_dict["road"] = word
        else:
            if address_dict["detail"] == "null":
                address_dict["detail"] = word
            else:
                address_dict["detail"] += " " + word

    return address_dict

def analyze_jeju(address_list):
    address_dict = dict()
    address_dict["metro"] = address_list[0]
    address_dict["basic"] = "null"
    address_dict["city"] = "null"
    address_dict["town"] = "null"
    address_dict["road"] = "null"
    address_dict["detail"] = "null"

    for word in address_list[1:]:
        if word.endswith("시"):
            address_dict["city"] = word

        elif word.endswith("읍") or word.endswith("면"):
            address_dict["town"] = word
        elif word.endswith("길") or word.endswith("리") or word.endswith("로"):
            address_dict["road"] = word
        else:
            if address_dict["detail"] == "null":
                address_dict["detail"] = word
            else:
                address_dict["detail"] += " " + word

    return address_dict

def analyze_guangyuksi(address_list):
    address_dict = dict()
    address_dict["metro"] = address_list[0]
    address_dict["basic"] = "null"
    address_dict["city"] = "null"
    address_dict["town"] = "null"
    address_dict["road"] = "null"
    address_dict["detail"] = "null"

    for word in address_list[1:]:
        if word.endswith("구") or word.endswith("군"):
            address_dict["basic"] = word
        elif word.endswith("읍") or word.endswith("면"):
            address_dict["town"] = word
        elif word.endswith("길") or word.endswith("리") or word.endswith("로"):
            address_dict["road"] = word
        else:
            if address_dict["detail"] == "null":
                address_dict["detail"] = word
            else:
                address_dict["detail"] += " " + word

    return address_dict

def analyze_do(address_list):
    address_dict = dict()
    address_dict["metro"] = address_list[0]
    address_dict["basic"] = "null"
    address_dict["city"] = "null"
    address_dict["town"] = "null"
    address_dict["road"] = "null"
    address_dict["detail"] = "null"

    for word in address_list[1:]:
        if word.endswith("시") or word.endswith("군"):
            address_dict["basic"] = word
        elif word.endswith("구"):
            address_dict["city"] = word
        elif word.endswith("읍") or word.endswith("면"):
            address_dict["town"] = word
        elif word.endswith("길") or word.endswith("리") or word.endswith("로"):
            address_dict["road"] = word
        else:
            if address_dict["detail"] == "null":
                address_dict["detail"] = word
            else:
                address_dict["detail"] += " " + word

    return address_dict

def analyze_teugbyeolsi(address_list):
    address_dict = dict()
    address_dict["metro"] = address_list[0]
    address_dict["basic"] = "null"
    address_dict["city"] = "null"
    address_dict["town"] = "null"
    address_dict["road"] = "null"
    address_dict["detail"] = "null"

    for word in address_list[1:]:
        if word.endswith("구"):
            address_dict["basic"] = word
        elif word.endswith("길") or word.endswith("리") or word.endswith("로"):
            address_dict["road"] = word
        else:
            if address_dict["detail"] == "null":
                address_dict["detail"] = word
            else:
                address_dict["detail"] += " " + word

    return address_dict

metro_list = ['서울', '부산', '인천', '대구', '광주', '대전', '울산', '세종', '경기도', '충청북도', '충청남도', '전라북도', '전라남도', '경상북도', '경상남도', '강원', '제주']
space_dict_list = []

def main():
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
                
            space = {'name': book_store_title, 'address': analyze_address(book_store_location), 'opration_time': book_store_time, 'closed_time': book_store_closed_days, 'phone': book_store_phone}
            space_dict_list.append(space)
            print(space_dict_list[-1])

            driver.switch_to.default_content()
            switch_frame(frame_id="searchIframe")

        # TODO: 다음 페이지 있으면 이동
        # TODO: 다음 페이지 없으면 종료

    except Exceptions.NoSuchElementException:
        print("ERROR: element 검색 실패")
        
    finally:
        pass


    driver.quit()

def search(metro_list):
    # try: 
    for metro in metro_list:
        driver.find_element(By.CLASS_NAME, "link_navbar.home").click()
        sleep(3)

        input = driver.find_element(By.CLASS_NAME, "input_search")
        input.click()
        # input.send_keys(metro + " 독립서점")
        input.send_keys("서울" + " 독립서점")
        input.send_keys(Keys.RETURN)

        sleep(3)

        switch_frame(frame_id="searchIframe")

        main()

    # except Exceptions.NoSuchElementException:
        # print("ERROR: element 검색 실패")

    # for metro in metro_list:


search(metro_list)