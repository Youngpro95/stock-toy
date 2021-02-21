from selenium import webdriver
import datetime,time

now = datetime.datetime.now() #시간
nowDate = now.strftime('%Y년 %m월 %d일 %H시 %M분 입니다.')
print(nowDate)

chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=chrome_options) #웹은 크롬&옵션사용
driver.maximize_window()
driver.get('http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC02021501')
time.sleep(0.5)
full = driver.find_element_by_xpath('//*[@id="jsViewSizeButton"]').click() #전체화면 vi해제시각 까지 불러오려고
driver.find_element_by_xpath('//*[@id="jsMdiContent"]/div/div[1]/div[1]/div[1]/div[1]/div/div/table/thead/tr[1]/td[9]/div/div/a').click()
driver.find_element_by_xpath('//*[@id="jsMdiContent"]/div/div[1]/div[1]/div[1]/div[1]/div/div/table/thead/tr[1]/td[9]/div/div/a').click()
vi_result = [] #결과값 담을 배열
final_vi_result=[]

def inner_scroll():
    scroll_moving = driver.find_elements_by_class_name('CI-FREEZE-SCROLLER') #여기에 scroll
    sc_test = driver.find_element_by_class_name('CI-FREEZE-SCROLLER-INNER')
    scroll_height = sc_test.size['height']
    last_index = driver.find_element_by_xpath('//*[@id="jsMdiContent"]/div/div[1]/div[1]/div[2]')
    scroll_range = 540
    while True:

        try:
            driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight=' + str(scroll_range) + '',last_index)
            scroll_range += 540
        except:
            print("실패")
        show_VI()
        if scroll_range >= scroll_height: #총 스크롤길이 넘어가면 멈춤
            break
    print("끝")
def show_VI():
    vi_body = driver.find_element_by_xpath('//*[@id="jsMdiContent"]/div/div[1]/div[1]/div[1]/div[2]/div/div/table/tbody').text
    transfer_list = vi_body.split("\n")
    vi_result.extend(transfer_list) # append 를 안한 이유는 텍스트를 리스트로 바꾸는 작업을 하기때문에 append가아닌 extend로 확장시킴

def check_overlap():
    count = 0
    for i in vi_result:
        if vi_result.count(i) == 2:
            # print("중복 발생 : "+str(vi_result.index(i)))
            count += 1
            # print(count)
            vi_result.remove(i) # 중복값 제거
def setting_vi():
    test_list =[]
    for i in range(len(vi_result)):
        test = vi_result[i].split()
        test_list.extend(test) #11개로 나뉨
    print(test_list)
show_VI()
inner_scroll()
check_overlap()
setting_vi()


print(vi_result)
driver.quit()
print("드라이버 종료")
