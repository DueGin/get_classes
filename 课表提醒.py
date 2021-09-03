'''   chromedriver.exe谷歌浏览器驱动必须在源文件同一目录下    '''
#死蓝鸟爬虫包
from selenium import webdriver
#时间包
from time import sleep
#Edge浏览器包
from msedge.selenium_tools import  Edge,EdgeOptions
#谷歌无头浏览器包
#from selenium.webdriver.chrome.options import Options
#死蓝鸟规避检测包
from selenium.webdriver import ChromeOptions
#死蓝鸟动作链包
from selenium.webdriver import ActionChains
#动作链键盘包
from selenium.webdriver.common.keys import Keys
#时间包
import datetime
class Spider:
    def __init__(self,username,password):
        self.u = username
        self.p = password

    #登陆
    def login(self):
        self.username.send_keys(self.u)
        self.password.send_keys(self.p)
        #回车
        ActionChains(self.bro).send_keys(Keys.ENTER).perform()

    #选择周次
    def click_week(self):
        # 获取周次标签
        week_button = self.bro.find_element_by_id('week')
        # 点击周次
        week_button.click()
        # 获取周次
        self.get_week_num()
        # 等待加载网页
        sleep(0.5)
        # 获取对应周次标签
        s_xpath = '//*[@id="week"]/option[' + str(self.week_num + 1) + ']'
        week_choice = self.bro.find_element_by_xpath(s_xpath)
        week_choice.click()
    #获取周次
    def get_week_num(self):
        # 获取周次
        self.week_num = int(datetime.datetime.now().isocalendar()[1] - datetime.datetime(2021, 8, 23).isocalendar()[1] + 1)
        print('周次：', self.week_num)
        # 获取星期
        self.week_day = datetime.datetime.now().isocalendar()[2]
        print('星期：', self.week_day)
        print('----------------------------')

    #获取所有课并保存在列表中
    def get_class_and_save_list(self):
        # 获取一周内所有课
        all_classes = []
        for i in range(1, 6):
            s_selector = '#kbLoading > table > tbody > tr:nth-child(' + str(i) + ')'
            classes = self.bro.find_element_by_css_selector(s_selector)
            all_classes.append(classes)
        # print(all_classes)

        # 遍历所有课并保存在列表中
        self.all_classes_inf = []
        for i in range(2, 9):
            everyday_class = []
            for clas in all_classes:
                s_selector = 'td:nth-child(' + str(i) + ') div'
                try:
                    class_s = clas.find_element_by_css_selector(s_selector).get_attribute("textContent")
                    everyday_class.append(class_s)
                    # print(class_s)
                except:
                    # print(None)
                    everyday_class.append(None)
            self.all_classes_inf.append(everyday_class)

        #print('    --------------------')
        # print(all_classes_inf)

    #处理数据，得出最终课表数据
    def get_end_class_list(self):
        self.end_all_classes = []
        for day in self.all_classes_inf:
            end_day_classes = []
            for clas in day:
                try:
                    classs = []
                    data = str(clas).split('学分：')
                    class_name = data[0]
                    classs.append(class_name)

                    time_data = str(clas).split('0', 1)[1].split('节')[0]
                    class_time = '0' + time_data + '节'
                    classs.append(class_time)

                    class_place = str(clas).split('节')[1].split('第')[0]
                    classs.append(class_place)

                    class_week = str(self.week_num)
                    classs.append(class_week)

                    class_day = str(clas).split(' ')[1]
                    classs.append(class_day)

                    end_day_classes.append(classs)
                except:
                    end_day_classes.append(None)
                # print(classs)
            self.end_all_classes.append(end_day_classes)
            # print(end_day_classes)

        # print(end_all_classes)

    #菜单
    def menu(self):
        while True:
            print('''
            1.上午课表
            2.下午课表
            3.晚上课表
            4.今天课表
            5.明天课表
            6.  退出
            ''')
            choise = input('请选择序号：')
            print()
            # 上午课表
            if choise == '1':
                if (self.end_all_classes[self.week_day - 1][0] == None) and (self.end_all_classes[self.week_day - 1][1] == None):
                    print('幸运的是 你早上没课!')
                    print('这不继续睡？')
                else:
                    print('上午的课表：')
                    for j in range(0, 2):
                        if self.end_all_classes[self.week_day - 1][j] == None:
                            continue
                        print('课程：' + self.end_all_classes[self.week_day - 1][j][0])
                        print('时间：' + self.end_all_classes[self.week_day - 1][j][1])
                        print('地点：' + self.end_all_classes[self.week_day - 1][j][2])
                        print('周次：' + self.end_all_classes[self.week_day - 1][j][3])
                        print('星期：' + self.end_all_classes[self.week_day - 1][j][4])
                        print('    --------------------')
                print('----------------------------')
                sleep(1)
            # 下午课表
            elif choise == '2':
                if (self.end_all_classes[self.week_day - 1][2] == None) and (self.end_all_classes[self.week_day - 1][3] == None):
                    print('下午没课!')
                else:
                    print('下午的课表：')
                    for j in range(2, 4):
                        if self.end_all_classes[self.week_day - 1][j] == None:
                            continue
                        print('课程：' + self.end_all_classes[self.week_day - 1][j][0])
                        print('时间：' + self.end_all_classes[self.week_day - 1][j][1])
                        print('地点：' + self.end_all_classes[self.week_day - 1][j][2])
                        print('周次：' + self.end_all_classes[self.week_day - 1][j][3])
                        print('星期：' + self.end_all_classes[self.week_day - 1][j][4])
                        print('    --------------------')
                print('----------------------------')
                sleep(1)
            # 晚上课表
            elif choise == '3':
                if self.end_all_classes[self.week_day - 1][4] == None:
                    print('晚上没课！')
                else:
                    print('晚上的课表：')
                    print('课程：' + self.end_all_classes[self.week_day - 1][4][0])
                    print('时间：' + self.end_all_classes[self.week_day - 1][4][1])
                    print('地点：' + self.end_all_classes[self.week_day - 1][4][2])
                    print('周次：' + self.end_all_classes[self.week_day - 1][4][3])
                    print('星期：' + self.end_all_classes[self.week_day - 1][4][4])
                print('----------------------------')
                sleep(1)
            # 今天的课表
            elif choise == '4':
                num = 0
                for i in self.end_all_classes[self.week_day - 1]:
                    if i == None:
                        num += 1
                        if num == 5:
                            print('今天没课！')
                        continue
                    print('今天的课表：')
                    print('课程：' + i[0])
                    print('时间：' + i[1])
                    print('地点：' + i[2])
                    print('周次：' + i[3])
                    print('星期：' + i[4])

                    print('    --------------------')
                print('----------------------------')
                sleep(1)
            elif choise == '5':
                t_num = 0
                for i in self.end_all_classes[self.week_day]:
                    if i == None:
                        t_num += 1
                        if t_num == 5:
                            print('明天没课！')
                        continue
                        print('明天的课表：')
                        print('课程：' + i[0])
                        print('时间：' + i[1])
                        print('地点：' + i[2])
                        print('周次：' + i[3])
                        print('星期：' + i[4])

                    print('    --------------------')
                print('----------------------------')
                sleep(1)
            elif choise == '6':
                break
            else:
                print('输入有误！')
                sleep(1)

    def main(self):
        #   创建一个对象，规避检测，并加上无头浏览器（照抄）
        #Edge规避检测
        edge_options = EdgeOptions()
        #使用谷歌内核
        edge_options.use_chromium = True
        edge_options.add_argument('--disable-blink-features=AutomationControlled')
        # 加上无头浏览器
        edge_options.add_argument("--headless")
        # 谷歌文档提到需要加上这个属性来规避bug
        edge_options.add_argument("disable-gpu")
        print('加载中...')
        self.bro = Edge(executable_path='./msedgedriver.exe',options=edge_options)

        # #谷歌浏览器规避检测
        # option = Options()
        # option.add_experimental_option('excludeSwitches', ['enable-automation'])
        # #控制chrome以无界面模式打开
        # option.add_argument('--headless')
        # option.add_argument('--disable-gpu')
        # print('加载中...')
        # #实例化一个浏览器对象(executable_path是浏览器驱动路径，options是规避检测参数+无头浏览器参数)
        # #self.bro = webdriver.Chrome(executable_path='./chromedriver.exe',options=option)
        #让浏览器发起一个指定url对应请求
        self.bro.get('http://125.216.100.10:2888/jsxsd/')#url
        print('----------------------------')
        #等待加载
        sleep(0.5)
        #获取账号密码标签
        self.username = self.bro.find_element_by_id('userAccount')
        self.password = self.bro.find_element_by_id('userPassword')
        self.login()
        # 获取名字
        print('憨批', self.bro.find_element_by_xpath('/html/body/div[1]/div[2]/ul/li[5]/span').get_attribute('textContent'))
        # 换作用域
        self.bro.switch_to.frame('Frame0')
        #选择周次
        self.click_week()
        print('处理中...')
        # 获取所有课并保存在列表中
        self.get_class_and_save_list()
        # 处理数据，得出最终课表数据
        self.get_end_class_list()
        print('----------------------------')
        # 退出浏览器
        self.bro.quit()
        #运行菜单
        self.menu()


if __name__ == '__main__':
    u = input('请输入学号：')
    p = input('请输入密码：')
    s = Spider(u,p)
    s.main()
    print('退出成功！')