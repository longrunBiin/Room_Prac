from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.touch_action import TouchAction
from appium.options.android import UiAutomator2Options
import time
import sys, os

class CheckHW():
    #EXECUTOR = 'http://127.0.0.1:4723/wd/hub'  # appium 버전 1.X
    EXECUTOR = 'http://127.0.0.1:4723'          # appium 버전 2.X
    def __init__(self, appLocation):
        options = UiAutomator2Options()
        options.app = appLocation
        #options.platform_name = 'Android'
        #options.automation_name = 'UiAutomator2'
        options.allow_test_packages = True
        options.enforce_app_install = True
        options.uiautomator2_server_install_timeout = 20000
        options.adb_exec_timeout = 20000
        options.language = 'en'
        options.locale = 'US'
        options.auto_grant_permissions = True
        
        self.driver = webdriver.Remote(
            self.EXECUTOR, options=options
        )
        self.driver.implicitly_wait(10)
 

    def press_home(self):
        self.driver.press_keycode(3) # keycode HOME
        
        
    def press_back(self):
        self.driver.press_keycode(4) # keycode Back
        
        
    def find_widget(self, id_str):
        try:
            w = self.driver.find_element(AppiumBy.ID, id_str)
        except:
            w = f'ID가 {id_str}인 위젯을 찾을 수 없음'
        return w
      

    def test_lab(self):
        w_ids = ['text_query_student', 'text_student_list', 'edit_student_id', 'edit_student_name', 'query_student', 'add_student', 'del_student', 'enroll']
        widgets = [self.find_widget(id_str) for id_str in w_ids]
        widgets_err = [x for x in widgets if isinstance(x, str)]
        if len(widgets_err) > 0:
            return ','.join(widgets_err)
    
        text_query_student, text_student_list, edit_student_id, edit_student_name, query_student, add_student, del_student, enroll = widgets
        
        if text_student_list.text != '1-james\n2-john\n':
            return '초기 DB 레코드 추가가 되어있지 않음'
        
        # 학생 3 추가
        edit_student_id.clear()
        edit_student_id.send_keys('3')
        edit_student_name.clear()
        edit_student_name.send_keys('adam')
        add_student.click()
        time.sleep(1)
        
        # Enroll 버튼
        edit_student_id.clear()
        edit_student_id.send_keys('2')
        enroll.click()
        time.sleep(1)
        
        edit_student_id.clear()
        edit_student_id.send_keys('2')
        query_student.click()
        time.sleep(1)
        
        if text_query_student.text != '2-john:1(c-lang),':
            return 'Enroll이 제대로 동작하지 않음'
        
        edit_student_id.clear()
        edit_student_id.send_keys('1')
        del_student.click()
        
        edit_student_id.clear()
        edit_student_id.send_keys('2')
        del_student.click()
        
        if text_student_list.text != '3-adam\n':
            return '삭제가 정상적으로 수행되지 않음'      
                     
        return 'OK'


if __name__ == '__main__':
    # 테스트할 APK 파일의 위치
    DEF_APP_LOCATION = r'C/Users/jangsubin/Desktop/Android/app/build/outputs/apk/debug/app-debug.apk/app-debug.apk'
    
    print('''
    1. Appium 서버는 실행 했나요?
    2. 에뮬레이터를 실행 했나요?
    3. 에뮬레이터는 정상적으로 동작 중인가요? 에뮬레이터가 멈춰있다면 cold boot하세요.
    4. DEF_APP_LOCATION은 본인의 app-debug.apk를 제대로 가리키고 있나요?
    ''')

    chw = CheckHW(DEF_APP_LOCATION)
    r = chw.test_lab() 
    if r == 'OK':
        score = 100
    else:
        score = 0
    print(score, r)

