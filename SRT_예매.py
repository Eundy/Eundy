#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://etk.srail.co.kr/cmc/01/selectLoginForm.do') # 이동을 원하는 페이지 주소 입력

driver.implicitly_wait(15) # 페이지 다 뜰 때 까지 기다림


# In[17]:


## 로그인 
driver.find_element(By.ID, 'srchDvNm01').send_keys('1984276892') # 회원번호
driver.find_element(By.ID, 'hmpgPwdCphd01').send_keys("hoon0221^^") # 비밀번호

driver.find_element(By.XPATH, '/html/body/div/div[4]/div/div[2]/form/fieldset/div[1]/div[1]/div[2]/div/div[2]/input').click()
driver.implicitly_wait(5)


# In[19]:


##예매
driver.get('https://etk.srail.kr/hpg/hra/01/selectScheduleList.do')
driver.implicitly_wait(5)

# 출발지 입력
dep_stn = driver.find_element(By.ID, 'dptRsStnCdNm')
dep_stn.clear() 
dep_stn.send_keys("동탄")

# 도착지 입력
arr_stn = driver.find_element(By.ID, 'arvRsStnCdNm')
arr_stn.clear()
arr_stn.send_keys("부산")


# In[20]:


# 날짜 드롭다운 리스트 보이게
elm_dptDt = driver.find_element(By.ID, "dptDt")
driver.execute_script("arguments[0].setAttribute('style','display: True;')", elm_dptDt)


# In[21]:


# 날짜입력
Select(driver.find_element(By.ID,"dptDt")).select_by_value("20220130")


# In[24]:


# 출발 시간
elm_dptTm = driver.find_element(By.ID, "dptTm")
driver.execute_script("arguments[0].setAttribute('style','display: True;')", elm_dptTm)

# 
Select(driver.find_element(By.ID, "dptTm")).select_by_visible_text("12")


# In[25]:


driver.find_element(By.XPATH,"//input[@value='조회하기']").click()


# In[26]:


## 기차 예매하기

train_list = driver.find_elements(By.CSS_SELECTOR, '#result-form > fieldset > div.tbl_wrap.th_thead > table > tbody > tr')

for i in range(1, len(train_list)+1):
    for j in range(3, 8):
        text = driver.find_element(By.CSS_SELECTOR, f"#result-form > fieldset > div.tbl_wrap.th_thead > table > tbody > tr:nth-child({i}) > td:nth-child({j})").text.replace("\n"," ")
        print(text, end="")
    print()


# In[ ]:


for i in range(1, 3):
    # td:nth-child(7)이 일반실 칸
    standard_seat = driver.find_element(By.CSS_SELECTOR, f"#result-form > fieldset > div.tbl_wrap.th_thead > table > tbody > tr:nth-child({i}) > td:nth-child(7)").text
    
    if "예약하기" in standard_seat:
        print("예약 가능")        
        driver.find_element(By.XPATH, f"/html/body/div[1]/div[4]/div/div[3]/div[1]/form/fieldset/div[6]/table/tbody/tr[{i}]/td[7]/a/span").click()
        
        # CSS Selector 사용시 예약하기 대신 좌석선택이 눌러지는 문제가 있어 XPATH로 변경
        # driver.find_element(By.CSS_SELECTOR, f"#result-form > fieldset > div.tbl_wrap.th_thead > table > tbody > tr:nth-child({i}) > td:nth-child(7) > a").click()
        
        


# In[ ]:


import time
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager

def open_brower():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    return driver


def login(driver, login_id, login_psw):
    driver.get('https://etk.srail.co.kr/cmc/01/selectLoginForm.do')
    driver.implicitly_wait(15)
    driver.find_element(By.ID, 'srchDvNm01').send_keys(str(login_id))
    driver.find_element(By.ID, 'hmpgPwdCphd01').send_keys(str(login_psw))
    driver.find_element(By.XPATH, '//*[@id="login-form"]/fieldset/div[1]/div[1]/div[2]/div/div[2]/input').click()
    driver.implicitly_wait(5)
    return driver


def search_train(driver, dpt_stn, arr_stn, dpt_dt, dpt_tm, num_trains_to_check=2, want_reserve=False):
    is_booked = False # 예약 완료 되었는지 확인용
    cnt_refresh = 0 # 새로고침 회수 기록

    driver.get('https://etk.srail.kr/hpg/hra/01/selectScheduleList.do') # 기차 조회 페이지로 이동
    driver.implicitly_wait(5)
    # 출발지/도착지/출발날짜/출발시간 입력
    elm_dpt_stn = driver.find_element(By.ID, 'dptRsStnCdNm')
    elm_dpt_stn.clear()
    elm_dpt_stn.send_keys(dpt_stn) # 출발지
    elm_arr_stn = driver.find_element(By.ID, 'arvRsStnCdNm')
    elm_arr_stn.clear()
    elm_arr_stn.send_keys(arr_stn) # 도착지
    elm_dptDt = driver.find_element(By.ID, "dptDt")
    driver.execute_script("arguments[0].setAttribute('style','display: True;')", elm_dptDt)
    Select(driver.find_element(By.ID,"dptDt")).select_by_value(dpt_dt) # 출발날짜
    elm_dptTm = driver.find_element(By.ID, "dptTm")
    driver.execute_script("arguments[0].setAttribute('style','display: True;')", elm_dptTm)
    Select(driver.find_element(By.ID, "dptTm")).select_by_visible_text(dpt_tm) # 출발시간

    print("기차를 조회합니다")
    print(f"출발역:{dpt_stn} , 도착역:{arr_stn}\n날짜:{dpt_dt}, 시간: {dpt_tm}시 이후\n{num_trains_to_check}개의 기차 중 예약")
    print(f"예약 대기 사용: {want_reserve}")

    driver.find_element(By.XPATH, "//input[@value='조회하기']").click() # 조회하기 버튼 클릭
    #driver.implicitly_wait(5)
    time.sleep(0.1)

    while True:
        for i in range(1, num_trains_to_check+1):
            standard_seat = driver.find_element(By.CSS_SELECTOR, f"#result-form > fieldset > div.tbl_wrap.th_thead > table > tbody > tr:nth-child({i}) > td:nth-child(7)").text
            reservation = driver.find_element(By.CSS_SELECTOR, f"#result-form > fieldset > div.tbl_wrap.th_thead > table > tbody > tr:nth-child({i}) > td:nth-child(8)").text

            if "예약하기" in standard_seat:
                print("예약 가능 클릭")
                driver.find_element(By.CSS_SELECTOR, f"#result-form > fieldset > div.tbl_wrap.th_thead > table > tbody > tr:nth-child({i}) > td:nth-child(7) > a").click()
                driver.implicitly_wait(1)

                if driver.find_elements(By.ID, 'isFalseGotoMain'):
                    is_booked = True
                    print("예약 성공")
                    driver2 = webdriver.Chrome(ChromeDriverManager().install())
                    driver2.get('https://www.youtube.com/watch?v=QKPx_ZhRl9o')
                    break
                else:
                    print("잔여석 없음. 다시 검색")
                    driver.back()  # 뒤로가기

            if want_reserve:
                if "신청하기" in reservation:
                    print("예약 대기 완료")
                    driver.find_element(By.CSS_SELECTOR, f"#result-form > fieldset > div.tbl_wrap.th_thead > table > tbody > tr:nth-child({i}) > td:nth-child(8) > a").click()
                    is_booked = True
                    break

        if not is_booked:
            time.sleep(randint(1, 2)) #2~4초 랜덤으로 기다리기

            # 다시 조회하기
            submit = driver.find_element(By.XPATH, "//input[@value='조회하기']")
            driver.execute_script("arguments[0].click();", submit)
            cnt_refresh += 1
            #print(f"새로고침 {cnt_refresh}회")
            driver.implicitly_wait(1)
            time.sleep(0.5)
        else:
            break
    return driver


if __name__ == "__main__":
    driver = open_brower()
    driver = login(driver, '1984276892', 'hoon0221^^')
    search_train(driver, "동탄", "광주송정", "20230519", "16", 1, False) #기차 출발 시간은 반드시 짝수


# In[ ]:




