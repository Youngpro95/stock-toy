from selenium import webdriver
import datetime,time
import json

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
    trasnfer_dic =[]
    result_dic ={}
    count = 0
    start = 1
    for i in range(len(vi_result)):
        vi_split = vi_result[i].split()
        trasnfer_dic.extend(vi_split) #11개로 나뉨
        stk_id = trasnfer_dic[0 + count]
        stk_cd = trasnfer_dic[2 + count]
        stk_nm = trasnfer_dic[3 + count]
        stk_pri = trasnfer_dic[6 + count]
        stk_inc = trasnfer_dic[7 + count]
        stk_act = trasnfer_dic[9 + count]
        stk_rel = trasnfer_dic[10 + count]
        # result_dic['stk_id'] = trasnfer_dic[0+count] #번호
        # result_dic['stk_cd'] = trasnfer_dic[2+count] #종목코드
        # result_dic['stk_nm'] = trasnfer_dic[3+count] #종목이름
        # result_dic['stk_pri'] = trasnfer_dic[6+count] #종목 기준가격
        # result_dic['stk_inc'] =  trasnfer_dic[7+count] #상승률
        # result_dic['stk_act'] = trasnfer_dic[9+count] #기준시각
        # result_dic['stk_rel'] = trasnfer_dic[10+count] #해제시각
        result_dic[start] = {'stk_id':stk_id, 'stk_cd':stk_cd, 'stk_nm':stk_nm, 'stk_pri':stk_pri, 'stk_inc':stk_inc, 'stk_act':stk_act, 'stk_rel':stk_rel}
        count += 11
        start += 1
        with open('vi_data.json', 'w', encoding="utf-8") as f: #json 파일 저장
            json.dump(result_dic, f , ensure_ascii=False, indent="\t")
    print(trasnfer_dic)

show_VI()
inner_scroll()
check_overlap()
setting_vi()


print(vi_result)
driver.quit()
print("드라이버 종료")
