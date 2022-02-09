#coding=utf-8
import sys
import time
import random
from datetime import datetime

import serial
import serial.tools.list_ports
import win32api
import win32con
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QApplication
from PyQt5.QtCore import QTimer, Qt, QThread, QCoreApplication
from PyQt5.uic.properties import QtCore

from ui_demo_1 import Ui_Form
from agree_dis import arg_code
import tools
from tools import as_num
import hashlib
import qdarkstyle
import PyQt5_stylesheets
import xlrd
from xlrd import xldate_as_tuple
############################全局变量#########################
sensortry = 0
save_path = ''
path = ''
filequire_handle = ''
offset=''
num_0b = 0
size_hex_com=''
filename=''
bit0b = 0
tar_add = ''

last_num=''
logfile_lisrt=[]
smal_filename = ''
offect_0b =''   #最大支持长度
file_size = ''    #文件大小
last_offerst = ''
my_offect_0b = ''
save_name=''   #保存文件名
numi = 0

##############################################################

class WorkThread(QThread):
    # 初始化线程
    def __int__(self):
        super(WorkThread, self).__init__()

    # 线程运行函数
    def run(self):
        while True:
            global sensortry
            sensortry = Pyqt5_Serial.sensordata(self)
            print(sensortry)
            time.sleep(0.1)


class Pyqt5_Serial(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super(Pyqt5_Serial, self).__init__()
        self.setupUi(self)
        self.init()
        self.setWindowTitle("wine-host-V0.70")
        self.ser = serial.Serial()
        self.port_check()
        self.logfile_lisrt=[]

        # 接收数据和发送数据数目置零
        # self.data_num_received = 0
        # self.lineEdit.setText(str(self.data_num_received))
        # self.data_num_sended = 0
        # self.lineEdit_2.setText(str(self.data_num_sended))
        self.label_11.setText('')
        self.label_13.setText('')
        self.label_15.setText('')

    #按钮初始化
    def init(self):
        # 所有按钮可点击性初始化

        self.close_button.setEnabled(False)  # 关闭串口按钮不可点击
        self.openfilebt.setEnabled(False)  # 浏览文件按钮不可点击
        self.upbut.setEnabled(False)  # 升级按钮不可点击
        self.lineEdit_4.setEnabled(False)  # 升级文件路径显示
        self.get_logbt.setEnabled(False)
        self.log_listWidget.setEnabled(False)
        self.download_logbt.setEnabled(False)
        # self.verticalGroupBox.setVisible(False)
        # self.formGroupBox1.setVisible(False)
        self.sn_show.setText('')
        self.sn_show.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.label_11.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.log_listWidget.addItem('文件名                创建时间                         最后修改时间')
        self.num = 1
        self.offset_num = 0
        self.confignum = 0
        self.fig = 0
        self.groupBox.setVisible(False)
        self.groupBox_3.setVisible(False)
        self.verticalGroupBox_2.setVisible(False)
############################################################配置项tableview设置######################################
        self.up_butt.setEnabled(False), self.mid_butt.setEnabled(False), self.dow_butt.setEnabled(False)
        self.setWindowIcon(QIcon('jc100.ico'))  # 设置窗体标题图标
        self.lineEdit_38.setVisible(False)
        self.label_49.setVisible(False)
        self.label.setText('正常模式')
        self.modeswitchnum =0
        self.pushButton_2.setEnabled(False)
        self.checksordata = 0
        self.groupBox_4.setTitle('传感器数据检测')
        self.comboBox.setVisible(False)
        self.pushButton_7.setVisible(False)
        # self.model = QStandardItemModel(0, 3)
        # self.tableView.setModel(self.model)
        # self.verticalLayout_3.addWidget(self.tableView)
        # 设置表头标签
        # self.model.setHorizontalHeaderLabels(['配置项', '说明', '值'])
        # self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.tableView.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        # self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.tableView.horizontalHeader().setSectionResizeMode(0, QHeaderView.Interactive)
        # self.tableView.setColumnWidth(0, 120)
        # self.tableView.setColumnWidth(1, 50)
        # self.tableView.setColumnWidth(2, 250)
        # self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 所有列自动拉伸，充满界面
        # item1 = QStandardItem('%s' % 'sys.sn')
        # item2 = QStandardItem('%s' % 'sys.run.mode')
        # item3 = QStandardItem('%s' % 'sys.sample.period')
        # item4 = QStandardItem('%s' % 'sys.lora.app.eui')
        # item5 = QStandardItem('%s' % 'sys.lora.app.key')
        # print('b')
        # self.model.appendRow([item1])
        # self.model.appendRow([item2])
        # self.model.appendRow([item3])
        # self.model.appendRow([item4])
        # self.model.appendRow([item5])
        # self.model.appendRow([
        #     QStandardItem('%s' % item1),
        #     QStandardItem('%s' % item2),
        #     QStandardItem('%s' % item3),
        # ])
        self.comboBox_2.addItems(['上层','中层','下层'])
###################################################################################################################
        # 串口检测按钮
        self.s1__box_1.clicked.connect(self.port_check)

        # 串口信息显示
        # self.s1__box_2.currentTextChanged.connect(self.port_imf)

        # 打开串口按钮
        self.open_button.clicked.connect(self.port_open)

        # 关闭串口按钮
        self.close_button.clicked.connect(self.port_close)


        # 定时发送数据
        # self.timer_send = QTimer()
        # self.timer_send.timeout.connect(self.read_sn)
        # self.timer_send_cb.stateChanged.connect(self.data_send_timer)

        # 定时器接收数据
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.data_receive)

        self.timer_get_sn = QTimer(self)
        self.timer_get_sn.timeout.connect(self.read_sn)

        self.timer_send_0b = QTimer(self)
        self.timer_send_0b.timeout.connect(self.read_0b)

        self.timer_get_log = QTimer()
        self.timer_get_log.timeout.connect(self.read_0f)

        self.timer_send_0f_0b = QTimer(self)
        self.timer_send_0f_0b.timeout.connect(self.read_0f_0b)

        # 打开浏览文件按钮
        self.openfilebt.clicked.connect(self.open_event)

        #保存log按钮
        self.download_logbt.clicked.connect(self.dewnload_log_event)

        # 获取log 按钮
        self.get_logbt.clicked.connect(self.get_log_list)

        #升级按钮
        self.upbut.clicked.connect(self.updata_event)

        #0x11按钮选择

###############################----窖池新增功能####################################
        # self.progressBar.setVisible(False)
        # self.progressBar_2.setVisible(False)
        self.tabWidget.setCurrentIndex(1)
        self.pushButton_3.clicked.connect(self.get_jc_config) #获取配置信息
        self.pushButton_2.clicked.connect(self.rating_data) #写入标定值
        self.pushButton_6.clicked.connect(self.reading_data) #读取标定值
        self.pushButton_7.clicked.connect(self.test)  # 读取传感器数据值
        self.up_butt.clicked.connect(self.test_up)  # 读取传感器数据值 上层
        self.mid_butt.clicked.connect(self.test_mid)  # 读取传感器数据值 中层
        self.dow_butt.clicked.connect(self.test_dow)  # 读取传感器数据值 下层
        self.pushButton_5.clicked.connect(self.reboot) #重启设备
        self.pushButton_4.clicked.connect(self.modeswitch_normal) #模式切换为2标定
        self.pushButton_8.clicked.connect(self.modeswitch_inquire)#模式切换为1检测
        self.pushButton.clicked.connect(self.getparam)
        self.tabWidget.currentChanged['int'].connect(self.tabfun)  # 绑定标签点击时的信号与槽函数
        self.lineEdit_33.returnPressed.connect(self.tableView_del1)
        self.lineEdit_34.returnPressed.connect(self.tableView_del2)
        self.lineEdit_32.returnPressed.connect(self.tableView_del3)
        self.lineEdit_35.returnPressed.connect(self.tableView_del4)
        self.lineEdit_36.returnPressed.connect(self.tableView_del5)
        self.comboBox.currentIndexChanged.connect(lambda: self.comboboxNote(self.comboBox.currentIndex()))

        self.lineEdit_37.returnPressed.connect(self.tableView_del6)
        self.pushButton_9.clicked.connect(self.clearup)  # 清空上层
        self.pushButton_10.clicked.connect(self.clearmid)  # 清空中层
        self.pushButton_11.clicked.connect(self.cleardow)  # 清空下层
        # self.tab_2.clicked.connect(self.get_jc_data)
        self.timer_getconfig = QTimer(self)
        self.timer_getconfig.timeout.connect(self.get_jc_config) #获取窖池配置信息表

        self.timer_getlinedata = QTimer(self)
        self.timer_getlinedata.timeout.connect(self.linedata)  # 获取窖池配置信息表

        self.timer_getsensordata = QTimer(self)
        self.timer_getsensordata.timeout.connect(self.sensordata)  # 获取窖池传感器信息表

    def clearup(self):
        self.water_content_4.setText(''),self.hum_4.setText(''),self.carbon_4.setText('')
        self.temp_4.setText(''),self.airpressure_4.setText(''),self.oxygen_3.setText('')
    def clearmid(self):
        self.water_content_5.setText(''),self.hum_5.setText(''),self.carbon_5.setText('')
        self.temp_5.setText(''),self.airpressure_5.setText(''),self.oxygen_4.setText('')
    def cleardow(self):
        self.water_content_6.setText(''),self.hum_6.setText(''),self.carbon_6.setText('')
        self.temp_6.setText(''),self.airpressure_6.setText(''),self.oxygen_5.setText('')

    def test(self):
        self.timer_getsensordata.start()
    def test_up(self):
        self.checksordata = 1
        code_11 = arg_code.encode(self, tar_add, 'FE', '00', '0200')
        self.data_send(str(code_11))
        print('fe读传感器发送包：', code_11)
        time.sleep(0.3)
        self.timer_getsensordata.start(2000)
    def test_mid(self):
        # if self.checksordata != 0:
        #     self.timer_getsensordata.stop()
        #     time.sleep(1000)
        self.checksordata = 2
        code_11 = arg_code.encode(self, tar_add, 'FE', '00', '0201')
        self.data_send(str(code_11))
        print('fe读传感器发送包：', code_11)
        time.sleep(0.3)
        self.timer_getsensordata.start(2000)
    def test_dow(self):
        self.checksordata = 3
        code_11 = arg_code.encode(self, tar_add, 'FE', '00', '0202')
        self.data_send(str(code_11))
        print('fe读传感器发送包：', code_11)
        time.sleep(0.3)
        self.timer_getsensordata.start(2000)
    def sensordata(self):
        self.comboboxNote(self.checksordata)
        print('当前checksordata的数值为：', self.checksordata)
        time.sleep(0.3)
        # self.get_jc_data()
    def comboboxNote(self, tag):
        self.water_content_4.setText('-'), self.water_content_5.setText('-'), self.water_content_6.setText('-')
        self.hum_4.setText('-'), self.hum_5.setText('-'), self.hum_6.setText('-')
        self.carbon_4.setText('-'), self.carbon_5.setText('-'), self.carbon_6.setText('-')
        self.temp_4.setText('-'), self.temp_5.setText('-'), self.temp_6.setText('-')
        self.airpressure_4.setText('-'), self.airpressure_5.setText('-'), self.airpressure_6.setText('-')
        self.oxygen_3.setText('-'), self.oxygen_5.setText('-'), self.oxygen_4.setText('-')
        self.get_jc_data()
        # if tag == 0:
        #     self.get_jc_data()
        # if tag == 1:
        #     code_11 = arg_code.encode(self, tar_add, 'FE', '00', '0200')
        #     self.data_send(str(code_11))
        #     print('fe读传感器发送包：', code_11)
        #     time.sleep(0.3)
        # if tag == 2:
        #     code_11 = arg_code.encode(self, tar_add, 'FE', '00', '0201')
        #     self.data_send(str(code_11))
        #     print('fe读传感器发送包：', code_11)
        #     time.sleep(0.3)
        # if tag == 3:
        #     code_11 = arg_code.encode(self, tar_add, 'FE', '00', '0202')
        #     self.data_send(str(code_11))
        #     print('fe读传感器发送包：', code_11)
        #     time.sleep(0.3)

    def getparam(self):
        #####################excel表格获取内容##################################
        # 导入需要读取的第一个Excel表格的路径
        data1 = xlrd.open_workbook('param.xlsx')
        table = data1.sheets()[0]
        # 创建一个空列表，存储Excel的数据
        tables = []
        # 将excel表格内容导入到tables列表中
        for line in range(1,8):
            for rown in range(1,5):
                array = table.cell_value(line, rown)
                tables.append(array)
        print(tables)
        self.lineEdit_7.setText(as_num(tables[0])), self.lineEdit_5.setText(as_num(tables[1])), self.lineEdit_6.setText(as_num(tables[2])), self.lineEdit_3.setText(as_num(tables[3]))
        self.lineEdit_9.setText(as_num(tables[4])), self.lineEdit_10.setText(as_num(tables[5])), self.lineEdit_11.setText(as_num(tables[6])), self.lineEdit_12.setText(as_num(tables[7]))
        self.lineEdit_13.setText(as_num(tables[8])), self.lineEdit_14.setText(as_num(tables[9])), self.lineEdit_15.setText(as_num(tables[10])), self.lineEdit_16.setText(as_num(tables[11]))
        self.lineEdit_17.setText(as_num(tables[12])), self.lineEdit_18.setText(as_num(tables[13])), self.lineEdit_19.setText(as_num(tables[14])), self.lineEdit_20.setText(as_num(tables[15]))
        self.lineEdit_8.setText(as_num(tables[16])), self.lineEdit_21.setText(as_num(tables[17])), self.lineEdit_22.setText(as_num(tables[18])), self.lineEdit_23.setText(as_num(tables[19]))
        self.lineEdit_24.setText(as_num(tables[20])), self.lineEdit_25.setText(as_num(tables[21])), self.lineEdit_26.setText(as_num(tables[22])), self.lineEdit_27.setText(as_num(tables[23]))
        self.lineEdit_28.setText(as_num(tables[24])), self.lineEdit_29.setText(as_num(tables[25])), self.lineEdit_30.setText(as_num(tables[26])), self.lineEdit_31.setText(as_num(tables[27]))
        ########################################################################
        # f = open('param.txt')
        # filedata = f.readlines()
        # test = ''
        # for i in range(1,5):
        #     test =test + filedata[i]
        # res = list(filter(None, test.split()))
        # print("获取值ABCD",res[0],res[1],res[2])
        # self.lineEdit_18.setText(res[0])
        # self.lineEdit_19.setText(res[1])
        # self.lineEdit_20.setText(res[2])
        # self.lineEdit_21.setText(res[3])
        # self.lineEdit_22.setText(res[4])
        # self.lineEdit_23.setText(res[5])
        # print("获取文件信息",filedata[1],filedata[2],filedata[3],res)
        # self.lineEdit_18.setText(filedata)
        # f.close()
    def tableView_del1(self): #05协议 修改配置项值，uid从0，1，2，3，4
        self.timer_heart.stop()
        index = tools.ascill_to_hex(self.lineEdit_33.text())
        global tar_add  # 目标地址
        code_11 = arg_code.encode(self, tar_add, '05', '00', '00' + '01' + index + '00')
        # print('code_of_02 发送的协议为：', code_0f)
        self.data_send(str(code_11))
        print('0501发送包：', code_11)
        time.sleep(0.08)

    def tableView_del2(self):  # 05协议 修改配置项值，uid从0，1，2，3，4
        self.timer_heart.stop()
        index = tools.ascill_to_hex(self.lineEdit_34.text())
        global tar_add  # 目标地址
        code_11 = arg_code.encode(self, tar_add, '05', '00', '00' + '02' + index + '00')
        # print('code_of_02 发送的协议为：', code_0f)
        self.data_send(str(code_11))
        print('0502发送包：', code_11)
        time.sleep(0.08)

    def tableView_del3(self):  # 05协议 修改配置项值，uid从0，1，2，3，4
        self.timer_heart.stop()
        index = tools.ascill_to_hex(self.lineEdit_32.text())
        global tar_add  # 目标地址
        code_11 = arg_code.encode(self, tar_add, '05', '00', '00' + '00' + index + '00')
        # print('code_of_02 发送的协议为：', code_0f)
        self.data_send(str(code_11))
        print('0500发送包：', code_11)
        time.sleep(0.08)

    def tableView_del4(self):  # 05协议 修改配置项值，uid从0，1，2，3，4
        self.timer_heart.stop()
        index = tools.ascill_to_hex(self.lineEdit_35.text())
        global tar_add  # 目标地址
        code_11 = arg_code.encode(self, tar_add, '05', '00', '00' + '03' + index + '00')
        # print('code_of_02 发送的协议为：', code_0f)
        self.data_send(str(code_11))
        print('0503发送包：', code_11)
        time.sleep(0.08)
    def tableView_del5(self):  # 05协议 修改配置项值，uid从0，1，2，3，4
        self.timer_heart.stop()
        index = tools.ascill_to_hex(self.lineEdit_36.text())
        global tar_add  # 目标地址
        code_11 = arg_code.encode(self, tar_add, '05', '00', '00' + '04' + index + '00')
        # print('code_of_02 发送的协议为：', code_0f)
        self.data_send(str(code_11))
        print('0504发送包：', code_11)
        time.sleep(0.08)

    def tableView_del6(self):  # 05协议 修改配置项值，uid从0，1，2，3，4
        self.timer_heart.stop()
        index = tools.ascill_to_hex(self.lineEdit_37.text())
        global tar_add  # 目标地址
        code_11 = arg_code.encode(self, tar_add, '05', '00', '00' + '05' + index + '00')
        # print('code_of_02 发送的协议为：', code_0f)
        self.data_send(str(code_11))
        print('0505发送包：', code_11)
        time.sleep(0.08)

    def linedata(self):
        dataa = self.lineEdit_7.text()
        datab = self.lineEdit_5.text()
        datac = self.lineEdit_6.text()
        datad = self.lineEdit_3.text()
        if dataa != '' and datab != '' and datac != '' and datad != '':
            # a = tools.small_to_big1(tools.floattostr(self.lineEdit_7.text()))
            # b = tools.small_to_big1(tools.floattostr(self.lineEdit_5.text()))
            # c = tools.small_to_big1(tools.floattostr(self.lineEdit_6.text()))
            # d = tools.small_to_big1(tools.floattostr(self.lineEdit_3.text()))
            # print('获取值为多大：    ',len(a+b+c+d))
            # if len(a+b+c+d) == 32:
            self.pushButton_2.setEnabled(True)
            self.timer_getlinedata.stop()

    def textcopy(self):
        self.sn_show.copy()
        command = QApplication.clipboard().text().upper()
        print(command)

    def tabfun(self, index):
        print("tabfun click" + "  " + str(index))
        if len(self.sn_show.text()) > 2:
            if (index == 0):
                print("本地升级")
            elif (index == 1):
                self.timer_heart.stop()
                time.sleep(0.5)
                self.modequery()
                self.timer_getlinedata.start(1)
                # if self.label_41 != '标定模式':
                #     print("传感器数据获取")
                #     self.timer_heart.stop()
                #     # self.modeswitch_dem()
                #     time.sleep(0.5)
                    # self.reboot()

    def reading_data(self):     #读取传感器内的原先标定值
        global tar_add  # 目标地址
        self.timer_heart.stop()
        diffdata = self.comboBox_2.currentText()
        if diffdata == '上层':
            number = '00'
        elif diffdata == '中层':
            number = '01'
        elif diffdata == '下层':
            number = '02'
        code_11 = arg_code.encode(self, tar_add, 'FE', '00', '0000' + number + '01')  #number代表上中下层选中情况
        # print('code_of_02 发送的协议为：', code_0f)
        self.data_send(str(code_11))
        print('fe读标定发送包：', code_11)
        time.sleep(0.15)

    def rating_data(self):
        global tar_add  # 目标地址
        tempa = tools.floattostr(self.lineEdit_13.text())
        tempb = tools.floattostr(self.lineEdit_14.text())
        tempc = tools.floattostr(self.lineEdit_15.text())
        tempd = tools.floattostr(self.lineEdit_16.text())
        tempdata = tempa + tempb + tempc + tempd
        alcoa = tools.floattostr(self.lineEdit_17.text())
        alcob = tools.floattostr(self.lineEdit_18.text())
        alcoc = tools.floattostr(self.lineEdit_19.text())
        alcod = tools.floattostr(self.lineEdit_20.text())
        alcodata = alcoa + alcob + alcoc + alcod
        carbona = tools.floattostr(self.lineEdit_8.text())
        carbonb = tools.floattostr(self.lineEdit_21.text())
        carbonc = tools.floattostr(self.lineEdit_22.text())
        carbond = tools.floattostr(self.lineEdit_23.text())
        carbondata = carbona + carbonb + carbonc + carbond
        airpressa = tools.floattostr(self.lineEdit_24.text())
        airpressb = tools.floattostr(self.lineEdit_25.text())
        airpressc = tools.floattostr(self.lineEdit_26.text())
        airpressd = tools.floattostr(self.lineEdit_27.text())
        airpressdata = airpressa + airpressb + airpressc + airpressd
        oxygana = tools.floattostr(self.lineEdit_28.text())
        oxyganb = tools.floattostr(self.lineEdit_29.text())
        oxyganc = tools.floattostr(self.lineEdit_30.text())
        oxygand = tools.floattostr(self.lineEdit_31.text())
        oxygandata = oxygana + oxyganb + oxyganc + oxygand
        cropdataa = tools.floattostr(float(self.lineEdit_9.text()) / 10000)
        cropdatab = tools.floattostr(float(self.lineEdit_10.text()) / 10000)
        cropdatac = tools.floattostr(float(self.lineEdit_11.text()) / 10000)
        cropdatad = tools.floattostr(float(self.lineEdit_12.text()) / 10000)
        hanshuiliang = cropdataa + cropdatab + cropdatac + cropdatad
        dataa = tools.floattostr(self.lineEdit_7.text())
        datab = tools.floattostr(self.lineEdit_5.text())
        datac = tools.floattostr(self.lineEdit_6.text())
        datad = tools.floattostr(self.lineEdit_3.text())
        waterdata01 = dataa + datab +datac + datad
        diffdata = self.comboBox_2.currentText()
        if diffdata == '上层':
            number = '00'
        elif diffdata == '中层':
            number = '01'
        elif diffdata == '下层':
            number = '02'
        code_11 = arg_code.encode(self, tar_add, 'FE', '00', '0001' + number + '01' +\
                                  tempdata + airpressdata + oxygandata + carbondata + alcodata + waterdata01 + hanshuiliang)
        # print('code_of_02 发送的协议为：', code_0f)
        self.data_send(str(code_11))
        print('fe标定发送包：', code_11)
        time.sleep(0.08)
    def modeswitch_inquire(self):
        global tar_add  # 目标地址
        if self.label.text() == '正常模式':
            self.modeswitchnum = 3
            code_11 = arg_code.encode(self, tar_add, 'FE', '00', '010101')
            # print('code_of_02 发送的协议为：', code_0f)
            self.data_send(str(code_11))
            print('fe检测模式发送包：', code_11)
            time.sleep(0.08)
        if self.label.text() == '检测模式':
            self.modeswitchnum = 2
            code_11 = arg_code.encode(self, tar_add, 'FE', '00', '010100')
            # print('code_of_02 发送的协议为：', code_0f)
            self.data_send(str(code_11))
            print('fe正常模式发送包：', code_11)
            time.sleep(0.08)
    def modeswitch_normal(self):
        global tar_add  # 目标地址
        if self.label_41.text()== '正常模式':
            self.modeswitchnum = 1
            code_11 = arg_code.encode(self, tar_add, 'FE', '00', '010102')
            # print('code_of_02 发送的协议为：', code_0f)
            self.data_send(str(code_11))
            print('fe标定模式发送包：', code_11)
            time.sleep(0.08)
        if self.label_41.text()== '标定模式':
            self.modeswitchnum = 2
            code_11 = arg_code.encode(self, tar_add, 'FE', '00', '010100')
            # print('code_of_02 发送的协议为：', code_0f)
            self.data_send(str(code_11))
            print('fe正常模式发送包：', code_11)
            time.sleep(0.08)
    def modeswitch_dem(self):
        global tar_add  # 目标地址
        code_11 = arg_code.encode(self, tar_add, 'FE', '00', '020101')
        # print('code_of_02 发送的协议为：', code_0f)
        self.data_send(str(code_11))
        print('fe标定模式发送包：',code_11)
        time.sleep(0.08)
    def reboot(self):
        global tar_add  # 目标地址
        code_11 = arg_code.encode(self, tar_add, '0E', '00', '0103')
        self.data_send(str(code_11))
        print('0E发送包：', code_11)
        time.sleep(0.08)

    def modequery(self):
        global tar_add  # 目标地址
        code_11 = arg_code.encode(self, tar_add, 'FE', '00', '0100')
        # print('code_of_02 发送的协议为：', code_0f)
        self.data_send(str(code_11))
        print('fe查询模式发送包：', code_11)
        time.sleep(0.08)

    def sensorquery(self):
        global tar_add  # 目标地址
        datea = tools.floattostr(self.lineEdit_7.text())
        dateb = tools.floattostr(self.lineEdit_5.text())
        datec = tools.floattostr(self.lineEdit_6.text())
        dated = tools.floattostr(self.lineEdit_3.text())

        code_11 = arg_code.encode(self, tar_add, 'FE', '01', '00')
        # print('code_of_02 发送的协议为：', code_0f)
        self.data_send(str(code_11))
        print('fe发送包：', code_11)
        time.sleep(0.08)

#########################################################传感器解析处理##########################################################

    def get_jc_data(self):
        global tar_add  # 目标地址
        self.timer_heart.stop()
        code_11 = arg_code.encode(self, tar_add, '11', '00', 9999)
        print('code_11 发送的协议为：', code_11)
        self.data_send(str(code_11))
        time.sleep(0.08)

    def decode_11(self,payload):
        # print(payload)
        self.Sensor_data(payload)

    def Sensor_data(self, payload):
        Sensor_int = payload[0]
        first = Sensor_int[0]
        self.second = Sensor_int[1]
        if first == '0':  # 该传感器连接在主机接口x上
            Sonsor_mode = self.Encode_Sonsor_mode(payload[1])
            print('主机接口' + self.second + '上的:   ' + Sonsor_mode, end='')
            # if self.second == '0':
            #     self.checksordata = 2
            # elif self.second == '1':
            #     self.checksordata = 3
            # elif self.second == '2':
            #     self.checksordata = 1
        elif first == '1':  # 该传感器连接在主机接口0上连接的扩展盒上的接口x上
            Sonsor_mode = self.Encode_Sonsor_mode(payload[1])
            print('主机接口' + str(int(first) - 1) + '上扩展盒的接口' + self.second + '上的:   ' + Sonsor_mode, end='')

        elif first == '2':  # 该传感器连接在主机接口1上连接的扩展盒上的接口x上
            Sonsor_mode = self.Encode_Sonsor_mode(payload[1])
            print('主机接口' + str(int(first) - 1) + '上扩展盒的接口' + self.second + '上的:   ' + Sonsor_mode, end='')

        else:
            Sonsor_mode = self.Encode_Sonsor_mode(payload[1])
            print('主机接口' + str(int(first) - 1) + '上扩展盒的接口' + self.second + '上的:   ' + Sonsor_mode, end='')

        # 传感器状态
        Sensor_status = payload[2]
        # print(Sensor_status)

        if Sensor_status == '80':
            print('     传感器未连接')
            if payload[3] == '00':
                llastdata = payload[4:]
                if len(llastdata) != 0:
                    self.decode_11(llastdata)
            else:
                print('^_^^_^^_^^_^^_^^_^^_^^_^^_^解析完成！^_^^_^^_^^_^^_^^_^^_^^_^', '\n')


        elif Sensor_status == '40':
            print('     传感器无响应')
            if payload[3] == '00':
                llastdata = payload[4:]
                if len(llastdata) != 0:
                    self.decode_11(llastdata)
                else:
                    print('^_^^_^^_^^_^^_^^_^^_^^_^^_^解析完成！^_^^_^^_^^_^^_^^_^^_^^_^', '\n')

        elif Sensor_status == '20':
            print('     传感器数据溢出')
            llastdata = payload[4:]
            # print('剩余长度', len(llastdata))
            if len(llastdata) != 0:
                # print(len(llastdata))
                # print(llastdata)
                self.decode_11(llastdata)

            else:
                print('^_^^_^^_^^_^^_^^_^^_^^_^^_^解析完成！^_^^_^^_^^_^^_^^_^^_^^_^', '\n')

        elif Sensor_status == '00':
            Sensor_data_num = payload[3]  # 传感器数据数量
            if Sensor_data_num == '01':
                print('\n有1组数据')
                last = self.endata(payload[4:])

            elif Sensor_data_num == '02':
                print('\n有' + tools.hex_dec(Sensor_data_num) + '组数据')
                last = self.endata(payload[4:])
                for i in range(int(tools.hex_dec(Sensor_data_num)) - 1):
                    last = self.endata(last)

            else:
                print('\n有' + tools.hex_dec(Sensor_data_num) + '组数据')
                # print(payload[4:])   #************************************************
                last = self.endata(payload[4:])
                for i in range(int(tools.hex_dec(Sensor_data_num)) - 1):
                    last = self.endata(last)
            print(last)
            # print(len(last))
            if len(last) != 0:
                print('剩余长度：', len(last))
                # print(last)
                # self.decode_11(last)
            else:
                print('^_^^_^^_^^_^^_^^_^^_^^_^^_^解析完成！^_^^_^^_^^_^^_^^_^^_^^_^', '\n')

        # 获取传感器型号

    def Encode_Sonsor_mode(self, payload):
        # Sonsor_mode=payload[0]
        Sonsor_mode = payload
        Sonsor_mode = Sonsor_mode.upper()  # 将小写转换成大写

        if Sonsor_mode == '01':
            Sonsor_mode = 'NBI土壤温度传感器'
            return Sonsor_mode

        elif Sonsor_mode == '02':
            Sonsor_mode = 'NBI土壤EC传感器'

        elif Sonsor_mode == '03':
            Sonsor_mode = 'NBI空气温湿度光照度传感器'

        elif Sonsor_mode == '04':
            Sonsor_mode = 'NBI WS100气象站'

        elif Sonsor_mode == '05':
            Sonsor_mode = 'NBI 郎酒100检测节点'

        elif Sonsor_mode == '20':
            Sonsor_mode = '雷神电子 土壤PH传感器'

        elif Sonsor_mode == '21':
            Sonsor_mode = '雷神电子 土壤温湿度传感器'

        elif Sonsor_mode == '22':
            Sonsor_mode = '雷神电子 土壤EC传感器'

        elif Sonsor_mode == '23':
            Sonsor_mode = '雷神电子 光合有效传感器'

        elif Sonsor_mode == '24':
            Sonsor_mode = '雷神电子 叶面温度传感器'

        elif Sonsor_mode == '25':
            Sonsor_mode = '雷神电子 叶面湿度传感器'

        elif Sonsor_mode == '26':
            Sonsor_mode = '雷神电子 二氧化碳传感器'

        elif Sonsor_mode == '27':
            Sonsor_mode = '新普惠 雨量传感器'

        elif Sonsor_mode == '28':
            Sonsor_mode = '新普惠 风速传感器'

        elif Sonsor_mode == '29':
            Sonsor_mode = '新普惠 风向传感器'

        elif Sonsor_mode == '2A':
            Sonsor_mode = '新普惠 气象站传感器'

        elif Sonsor_mode == '2B':
            Sonsor_mode = '渤海 土壤EC传感器'

        elif Sonsor_mode == '2C':
            Sonsor_mode = '威海 土壤EC传感器'

        elif Sonsor_mode == '2D':
            Sonsor_mode = '威海 土壤EC传感器'

        elif Sonsor_mode == '2E':
            Sonsor_mode = '大气压力传感器'

        elif Sonsor_mode == '2F':
            Sonsor_mode = '	西安仕乐克 水压水温传感器'

        elif Sonsor_mode == '30':
            Sonsor_mode = '凯米斯 水质（荧光）溶解氧传感器'

        elif Sonsor_mode == '31':
            Sonsor_mode = '雷神电子 水质（电极）溶解氧传感器'

        elif Sonsor_mode == '32':
            Sonsor_mode = '凯米斯 水质氨氮传感器'

        elif Sonsor_mode == '33':
            Sonsor_mode = '威海 水质EC传感器'

        elif Sonsor_mode == '34':
            Sonsor_mode = '凯米斯 水质PH传感器'

        elif Sonsor_mode == '35':
            Sonsor_mode = '凯米斯 水质ORP传感器'

        elif Sonsor_mode == '36':
            Sonsor_mode = '凯米斯 水质浊度传感器'

        elif Sonsor_mode == '37':
            Sonsor_mode = '凯米斯 水质EC传感器'

        elif Sonsor_mode == '38':
            Sonsor_mode = '凯米斯 水质盐度传感器'

        elif Sonsor_mode == '39':
            Sonsor_mode = '水压水流传感器'

        elif Sonsor_mode == '3A':
            Sonsor_mode = '双锐 水流传感器'

        elif Sonsor_mode == '3B':
            Sonsor_mode = '苏州轩胜 水压传感器'

        elif Sonsor_mode == '3C':
            Sonsor_mode = '控制设备从板'

        elif Sonsor_mode == '3D':
            Sonsor_mode = '介可视 含水量传感器'

        elif Sonsor_mode == '3E':
            Sonsor_mode = '凯米斯 海水EC传感器'

        elif Sonsor_mode == '3F':
            Sonsor_mode = '西安仕乐克 水压水温传感器'

        elif Sonsor_mode == '40':
            Sonsor_mode = '华聚科仪 雷达水位传感器'

        elif Sonsor_mode == '41':
            Sonsor_mode = 'CG-62 压电式雨量传感器'


        elif Sonsor_mode == '70':
            Sonsor_mode = '凯米斯 电刷'

        elif Sonsor_mode == 'FF':
            Sonsor_mode = 'NBI 5口拓展盒'

        else:
            Sonsor_mode = '其他传感器'

        return Sonsor_mode

        # 传感器数据类型分类和数据的类型

    def endata(self, payload):
        # print(payload)
        Sensor_data_mode = payload[0]

        Sensor_data_mode = Sensor_data_mode.upper()  # 将小写转换成大写

        # print(Sensor_data_mode)
        if Sensor_data_mode == '01':
            last, Sensor_data_last = self.Son_data_type(payload)
            print('         电量:', Sensor_data_last + " %")
            return last

        elif Sensor_data_mode == '02':
            last, Sensor_data_last = self.Son_data_type(payload)
            print('         电压:', Sensor_data_last + " mV")
            return last

        elif Sensor_data_mode == '03':
            last, Sensor_data_last = self.Son_data_type(payload)
            print('         温度0:', Sensor_data_last + " ℃")
            if self.second == '0':
                self.label_21.setText('温度上')
                self.water_content_4.setText(Sensor_data_last + ' ℃')
            if self.second == '1':
                self.label_29.setText('温度中')
                self.water_content_5.setText(Sensor_data_last + ' ℃')
            if self.second == '2':
                self.label_35.setText('温度下')
                self.water_content_6.setText(Sensor_data_last + ' ℃')
            return last

        elif Sensor_data_mode == '04':
            last, Sensor_data_last = self.Son_data_type(payload)
            print('         湿度:', Sensor_data_last + " %RH")
            return last

        elif Sensor_data_mode == '05':
            last, Sensor_data_last = self.Son_data_type(payload)
            print('         降雨量:', Sensor_data_last + " mm")
            return last

        elif Sensor_data_mode == '06':
            last, Sensor_data_last = self.Son_data_type(payload)
            print('         方向:', Sensor_data_last + " °")
            return last

        elif Sensor_data_mode == '07':
            last, Sensor_data_last = self.Son_data_type(payload)
            print('         速度:', Sensor_data_last + " m/s")
            return last

        elif Sensor_data_mode == '08':
            last, Sensor_data_last = self.Son_data_type(payload)
            print('         EC值:', Sensor_data_last + " ds/m")
            return last

        elif Sensor_data_mode == '09':
            last, Sensor_data_last = self.Son_data_type(payload)
            print('         二氧化碳:', Sensor_data_last + " ppm")
            if self.second == '0':
                self.label_23.setText('二氧化碳上')
                self.airpressure_4.setText(Sensor_data_last + ' ppm')
            if self.second == '1':
                self.label_26.setText('二氧化碳中')
                self.airpressure_5.setText(Sensor_data_last + ' ppm')
            if self.second == '2':
                self.label_32.setText('二氧化碳下')
                self.airpressure_6.setText(Sensor_data_last + ' ppm')
            return last

        elif Sensor_data_mode == '0A':
            last, Sensor_data_last = self.Son_data_type(payload)
            print('         光照度:', Sensor_data_last + " lux")
            return last

        elif Sensor_data_mode == '0B':
            last, Sensor_data_last = self.Son_data_type(payload)
            print('         太阳辐射:', Sensor_data_last + " W/平方米")
            return last

        elif Sensor_data_mode == '0C':
            last, Sensor_data_last = self.Son_data_type(payload)
            print('         PH值:', Sensor_data_last + " pH")
            return last

        elif Sensor_data_mode == '0D':
            last, Sensor_data_last = self.Son_data_type(payload)
            print('         压强:', Sensor_data_last + " pa")
            if self.second == '0':
                self.label_19.setText('压强上')
                self.carbon_4.setText(Sensor_data_last + ' Pa')
            if self.second == '1':
                self.label_28.setText('压强中')
                self.carbon_5.setText(Sensor_data_last + ' Pa')
            if self.second == '2':
                self.label_34.setText('压强下')
                self.carbon_6.setText(Sensor_data_last + ' Pa')
            return last

        elif Sensor_data_mode == '0E':
            last, Sensor_data_last = self.Son_data_type(payload)
            print('         水溶氧:', Sensor_data_last + " mg/L")
            return last

        elif Sensor_data_mode == '0F':
            last, Sensor_data_last = self.Son_data_type(payload)
            print('         水流量:', Sensor_data_last + " 立方米/小时")
            return last

        elif Sensor_data_mode == '10':
            last, Sensor_data_last = self.Son_data_type(payload)
            print('         水浊度:', Sensor_data_last + " NTU")
            return last

        elif Sensor_data_mode == '11':
            last, Sensor_data_last = self.Son_data_type(payload)
            print('         ORP:', Sensor_data_last + " mv")
            return last

        elif Sensor_data_mode == '12':
            last, Sensor_data_last = self.Son_data_type(payload)
            print('         水位:', Sensor_data_last + " m")
            return last

        elif Sensor_data_mode == '13':
            last, Sensor_data_last = self.Son_data_type(payload)
            print('         盐度值:', Sensor_data_last + " ppt")
            return last

        elif Sensor_data_mode == '14':
            last, Sensor_data_last = self.Son_data_type(payload)
            print('         降雨强度:', Sensor_data_last + " mm/min")
            return last

        elif Sensor_data_mode == '15':
            last, Sensor_data_last = self.Son_data_type(payload)
            print('         太阳辐射:', Sensor_data_last + " MJ/平方米")
            return last

        elif Sensor_data_mode == '16':
            last, Sensor_data_last = self.Son_data_type(payload)
            print('         氨氮:', Sensor_data_last + " mg/L")
            return last

        elif Sensor_data_mode == '17':
            last, Sensor_data_last = self.Son_data_type(payload)
            print('         有效光合辐射:', Sensor_data_last + " umol/平方米*s")
            return last

        elif Sensor_data_mode == '18':
            last, Sensor_data_last = self.Son_data_type(payload)
            print('         含水量:', Sensor_data_last + " %")
            if self.second == '0':
                self.label_20.setText('含水量上')
                self.oxygen_3.setText(Sensor_data_last)
            if self.second == '1':
                self.label_25.setText('含水量中')
                self.oxygen_4.setText(Sensor_data_last)
            if self.second == '2':
                self.label_31.setText('含水量下')
                self.oxygen_5.setText(Sensor_data_last)
            return last

        elif Sensor_data_mode == '19':
            last, Sensor_data_last = self.Son_data_type(payload)
            print('         PM2.5:', Sensor_data_last + " ug/立方米")
            return last

        elif Sensor_data_mode == '1A':
            last, Sensor_data_last = self.Son_data_type(payload)
            print('         PM 10:', Sensor_data_last + " ug/立方米")
            return last

        elif Sensor_data_mode == '1B':
            last, Sensor_data_last = self.Son_data_type(payload)
            print('         氧气:', Sensor_data_last + " %")
            if self.second == '0':
                self.label_22.setText('氧气上')
                self.temp_4.setText(Sensor_data_last)
            if self.second == '1':
                self.label_24.setText('氧气中')
                self.temp_5.setText(Sensor_data_last)
            if self.second == '2':
                self.label_30.setText('氧气下')
                self.temp_6.setText(Sensor_data_last)
            return last

        elif Sensor_data_mode == '1C':
            last, Sensor_data_last = self.Son_data_type(payload)
            print('         酒精浓度:', Sensor_data_last + " %")
            if self.second == '0':
                self.label_18.setText('酒精浓度上')
                self.hum_4.setText(Sensor_data_last + ' %')
            if self.second == '1':
                self.label_27.setText('酒精浓度中')
                self.hum_5.setText(Sensor_data_last + ' %')
            if self.second == '2':
                self.label_33.setText('酒精浓度下')
                self.hum_6.setText(Sensor_data_last + ' %')
            return last
        elif Sensor_data_mode == '1D':
            last, Sensor_data_last = self.Son_data_type(payload)
            print('         空高:', Sensor_data_last + " m")
            return last
        elif Sensor_data_mode == '1E':
            last, Sensor_data_last = self.Son_data_type(payload)
            print('         含水量:', Sensor_data_last + " %RH")
            return last
        else:
            # print(Sensor_data_mode)
            last, Sensor_data_last = self.Son_data_type(payload)
            print('         未知(' + Sensor_data_mode + '):', Sensor_data_last + " m")
            return last

    def Son_data_type(self, payload):
        # 数据类型
        Sensor_data_type7_4, Sensor_data_type3_0 = tools.hex_bin3(payload[1])
        # print(Sensor_data_type7_4)
        # print(Sensor_data_type3_0)

        if Sensor_data_type7_4 == '0000':
            Sensor_data_last = payload[2]
            Sensor_data_last = (tools.hex_dec(Sensor_data_last))
            if Sensor_data_type3_0 == '0001':
                Sensor_data_last = int(Sensor_data_last) / 10
            elif Sensor_data_type3_0 == '0010':
                Sensor_data_last = int(Sensor_data_last) / 100
            elif Sensor_data_type3_0 == '0011':
                Sensor_data_last = int(Sensor_data_last) / 1000
            else:
                pass
            last = payload[3:]



        elif Sensor_data_type7_4 == '0001':
            # print(payload[2:4])
            Sensor_data_last = payload[2:4]
            Sensor_data_last = (tools.hex_dec(tools.unsize(Sensor_data_last)))
            if Sensor_data_type3_0 == '0001':
                Sensor_data_last = int(Sensor_data_last) / 10
            elif Sensor_data_type3_0 == '0010':
                Sensor_data_last = int(Sensor_data_last) / 100
            elif Sensor_data_type3_0 == '0011':
                Sensor_data_last = int(Sensor_data_last) / 1000
            else:
                pass
            last = payload[4:]


        elif Sensor_data_type7_4 == '0010':
            Sensor_data_last = payload[2:6]
            Sensor_data_last = (tools.hex_dec(tools.unsize(Sensor_data_last)))
            if Sensor_data_type3_0 == '0001':
                Sensor_data_last = int(Sensor_data_last) / 10
            elif Sensor_data_type3_0 == '0010':
                Sensor_data_last = int(Sensor_data_last) / 100
            elif Sensor_data_type3_0 == '0011':
                Sensor_data_last = int(Sensor_data_last) / 1000
            else:
                pass
            last = payload[6:]


        elif Sensor_data_type7_4 == '0011':
            Sensor_data_last = payload[2]
            Sensor_data_last = (tools.hex_dec(Sensor_data_last))
            if Sensor_data_type3_0 == '0001':
                Sensor_data_last = int(Sensor_data_last) / 10
            elif Sensor_data_type3_0 == '0010':
                Sensor_data_last = int(Sensor_data_last) / 100
            elif Sensor_data_type3_0 == '0011':
                Sensor_data_last = int(Sensor_data_last) / 1000
            else:
                pass
            last = payload[3:]


        elif Sensor_data_type7_4 == '0100':
            Sensor_data_last = payload[2:4]
            Sensor_data_last = tools.hex_dec(tools.unsize(Sensor_data_last))
            if Sensor_data_type3_0 == '0001':
                Sensor_data_last = int(Sensor_data_last) / 10
            elif Sensor_data_type3_0 == '0010':
                Sensor_data_last = int(Sensor_data_last) / 100
            elif Sensor_data_type3_0 == '0011':
                Sensor_data_last = int(Sensor_data_last) / 1000
            else:
                pass
            last = payload[4:]
            # print(last)
        elif Sensor_data_type7_4 == '0101':
            Sensor_data_last = payload[2:6]
            Sensor_data_last = (tools.hex_dec(tools.unsize(Sensor_data_last)))
            if Sensor_data_type3_0 == '0001':
                Sensor_data_last = int(Sensor_data_last) / 10
            elif Sensor_data_type3_0 == '0010':
                Sensor_data_last = int(Sensor_data_last) / 100
            elif Sensor_data_type3_0 == '0011':
                Sensor_data_last = int(Sensor_data_last) / 1000
            else:
                pass
            last = payload[6:]


        elif Sensor_data_type7_4 == '0110':
            Sensor_data_last = payload[2:6]
            Sensor_data_last = (tools.size_to_float(Sensor_data_last))
            if Sensor_data_type3_0 == '0001':
                Sensor_data_last = int(Sensor_data_last) / 10
            elif Sensor_data_type3_0 == '0010':
                Sensor_data_last = int(Sensor_data_last) / 100
            elif Sensor_data_type3_0 == '0110':
                Sensor_data_last = int(Sensor_data_last) / 1000
            else:
                pass
            last = payload[6:]


        elif Sensor_data_type7_4 == '0111':
            Sensor_data_last = payload[2:10]
            Sensor_data_last = (tools.size_to_double(Sensor_data_last))
            if Sensor_data_type3_0 == '0001':
                Sensor_data_last = int(Sensor_data_last) / 10
            elif Sensor_data_type3_0 == '0010':
                Sensor_data_last = int(Sensor_data_last) / 100
            else:
                pass
            last = payload[10:]


        elif Sensor_data_type7_4 == '1000':
            count = payload[2:].index('00')
            data = payload[2:count]
            Sensor_data_last = (tools.size_to_float(data))
            if Sensor_data_type3_0 == '0001':
                Sensor_data_last = int(Sensor_data_last) / 10
            elif Sensor_data_type3_0 == '0010':
                Sensor_data_last = int(Sensor_data_last) / 100
            else:
                pass
            last = payload[count + 1:]
            # print(len(last))

        return last, str(Sensor_data_last)

    def port1_data(self, data):
        newdata = []
        getdata = data.find('110100')
        cutdata = data[getdata + 6:len(data) - 4]
        for i in range(0, len(cutdata), 2):
            newdata.append(cutdata[i * 1:i + 2])
        print('截取的部分： ', newdata)
        self.Sensor_data(newdata)


#################################################################################

################################获取配置列表########################################
    def get_jc_config(self):   #06协议获取配置值，配置项uid从0开始
        # self.model.setHorizontalHeaderLabels(['配置项', '说明', '值'])
        # self.tableView.setColumnWidth(0, 120)
        # self.tableView.setColumnWidth(1, 50)
        # self.tableView.setColumnWidth(2, 250)
        # if self.fig == 1:
        #     self.model.clear()
        self.timer_heart.stop()
        global tar_add  # 目标地址
        code_03 = arg_code.encode(self, tar_add, '06', '00', '000'+str(self.confignum))
        self.data_send(str(code_03))
        time.sleep(0.11)
        print('code_03 发送的协议为：', code_03)
        self.timer_getconfig.start(1)


#################################################################################

    # def open_read0a(self):
    #     self.timer_aa.start(5)
    # 获取所有log文件列表
    def get_log_list(self):
        self.log_listWidget.clear()
        self.log_listWidget.addItem('文件名                创建时间                         最后修改时间')
        # self.get_logbt.setEnabled(False)
        global tar_add  # 目标地址
        if tar_add!='':
            code_0f = arg_code.encode(self, tar_add, '0f', '00', '28' + '00000000')
            print('code_of_01 发送的协议为：', code_0f)
            self.data_send(str(code_0f))
            # time.sleep(0.04)
            self.timer_get_log.start()
            # self.timer_heart.stop()
        else:return

    def read_0f(self):
        global tar_add  # 目标地址
        global last_num  # 偏移量，每次加一
        code_0f = arg_code.encode(self, tar_add, '0f', '00', '28' + str(last_num))
        # print('code_of_02 发送的协议为：', code_0f)
        self.data_send(str(code_0f))
        time.sleep(0.08)

        # 0F-0A协议
    def read_0f_0a(self):
        global tar_add
        global smal_filename
        myfilename = smal_filename
        code_0a = arg_code.encode(self, tar_add, '0a', '00', 'A8' + myfilename + '00', )
        # self.s3__send_text.setText(str(code_0a))
        # print('发送的0f_0a协议为：', code_0a)
        # self.upbut.setText('请求中')
        self.data_send(str(code_0a))
        time.sleep(1)

        # 保存log事件
    def dewnload_log_event(self):
        self.timer_heart.stop()
        print('开始下载log')
        self.read_0f_0a()
        # self.log_pr_Bar.reset()    #每次下载前，都需要将他重置一遍
        global save_path
        global save_name
        try:
            fileName2, ok2 = QFileDialog.getSaveFileName(None, "文件保存", self.sn_show.text() +'_' + save_name +\
                '_' + self.createtime + '.txt')
        except:
            fileName2, ok2 = QFileDialog.getSaveFileName(None, "文件保存", '无SN'+save_name + '.txt')
        save_path = fileName2
        if save_path != '':
            # print(save_path)
            self.openfilebt.setEnabled(False)
            self.download_logbt.setEnabled(False)
            self.openfilebt.setEnabled(False)
            global tar_add
            global filequire_handle
            global offect_0b
            size_0b = offect_0b
            handle = filequire_handle
            code_0f_0b = arg_code.encode(self, tar_add, '0b', '00', handle + '00000000' + size_0b)
            # print('0f_0b发送的协议为:' + str(code_0f_0b))
            self.data_send(str(code_0f_0b))
            time.sleep(0.5)
            self.timer_send_0f_0b.start()
            self.upbut.setEnabled(False)
            self.log_textview.setVisible(True)
        else:
            pass
        # 0f_0B协议
    def read_0f_0b(self):
        global tar_add
        global filequire_handle
        global offect_0b
        global offset   # 偏移量
        global last_offerst  # 文件大小减去偏移量的值
        global my_offect_0b
        my_offse = offset
        size_0b = offect_0b
        handle = filequire_handle
        if self.offset_num == self.num:
            # try:
            # except
            if last_offerst > int(my_offect_0b):
                # time.sleep(0.1)
                code_0f_0b = arg_code.encode(self, tar_add, '0b', '00', handle + my_offse + size_0b)
                print('0f_0b发送的协议为:' + str(code_0f_0b))
                self.log_textview.setText(str(last_offerst))
                # self.log_textview.setText(my_offect_0b)
                self.data_send(str(code_0f_0b))
                # time.sleep(0.01)

            elif last_offerst==int(my_offect_0b):
                # time.sleep(1)
                code_0f_0b = arg_code.encode(self, tar_add, '0b', '00', handle + my_offse + size_0b)
                print('0f_0b_03发送的协议为:' + str(code_0f_0b))
                # self.log_textview.setText(str(last_offerst))
                self.log_textview.setText('---')
                self.data_send(str(code_0f_0b))
                self.timer_send_0f_0b.stop()
                self.timer_heart.start()

            elif 0<last_offerst<int(my_offect_0b):
                last_offerst1 = hex(last_offerst)[2:]  # 加1 后继续转换成十六进制
                last_offerst2 = '0' * (8 - len(last_offerst1)) + str(last_offerst1)  # 转换成十六进制后，补全8个0
                last_offerst3 = tools.small_to_big1(last_offerst2)
                # time.sleep(1)
                code_0f_0b = arg_code.encode(self, tar_add, '0b', '00', handle + my_offse + last_offerst3)
                print('0f_0b发送的协议为:' + str(code_0f_0b))
                self.log_textview.setText('---')
                self.data_send(str(code_0f_0b))
                self.timer_send_0f_0b.stop()
                self.timer_heart.start()

            elif last_offerst <0:
                self.timer_send_0f_0b.stop()
                self.timer_heart.start(1000)
                self.openfilebt.setEnabled(True)
                self.log_textview.setText('---')
            time.sleep(0.06)
            self.num += 1
        else:
            time.sleep(2)
            self.num = self.num - 1


    # 串口检测
    def port_check(self):
        # 检测所有存在的串口，将信息存储在字典中
        self.Com_Dict = {}
        port_list = list(serial.tools.list_ports.comports())
        self.s1__box_2.clear()
        for port in port_list:
            self.Com_Dict["%s" % port[0]] = "%s" % port[1]
            self.s1__box_2.addItem(port[0])
        if len(self.Com_Dict) == 0:
            self.state_label.setText(" 无串口")

    # 串口信息
    def port_imf(self):
        # 显示选定的串口的详细信息
        imf_s = self.s1__box_2.currentText()
        if imf_s != "":
            self.state_label.setText(self.Com_Dict[self.s1__box_2.currentText()])

    # 打开串口
    def port_open(self):
        self.ser.port = self.s1__box_2.currentText()
        self.ser.baudrate = int(230400)
        self.ser.bytesize = int(8)
        self.ser.stopbits = int(1)
        self.ser.parity = 'N'

        try:
            self.ser.open()
        except:
            QMessageBox.critical(self, "Port Error", "此串口被占用！")
            return None

        # 打开串口接收定时器，周期为2ms
        self.timer.start()
        if self.ser.isOpen():
            self.open_button.setEnabled(False)
            self.close_button.setEnabled(True)
            # self.formGroupBox1.setTitle("串口状态（已开启）")
            time.sleep(0.5)
            self.timer_get_sn.start(1)
            self.timerheart()

    # 关闭串口
    def port_close(self):
        self.timer.stop()
        self.timer_get_sn.stop()
        self.timer_send_0b.stop()
        self.timer_send_0f_0b.stop()
        self.timer_get_log.stop()
        self.timer_heart.stop()
        self.timer_getsensordata.stop()
        try:
            self.ser.close()
        except:
            pass
        self.open_button.setEnabled(True)
        self.close_button.setEnabled(False)
        self.get_logbt.setEnabled(False)
        self.openfilebt.setEnabled(False)
        self.log_listWidget.setEnabled(False)
        self.groupBox.setVisible(False)
        self.groupBox_3.setVisible(False)
        self.verticalGroupBox_2.setVisible(False)
        self.upbut.setEnabled(False)
        # self.label.setText('')
        self.num = 1
        self.offset_num = 0
        self.checksordata = 0
        #####################################检测传感器
        self.water_content_4.setText('-'),self.water_content_5.setText('-'),self.water_content_6.setText('-')
        self.hum_4.setText('-'),self.hum_5.setText('-'),self.hum_6.setText('-')
        self.carbon_4.setText('-'),self.carbon_5.setText('-'),self.carbon_6.setText('-')
        self.temp_4.setText('-'),self.temp_5.setText('-'),self.temp_6.setText('-')
        self.airpressure_4.setText('-'),self.airpressure_5.setText('-'),self.airpressure_6.setText('-')
        self.oxygen_3.setText('-'),self.oxygen_5.setText('-'),self.oxygen_4.setText('-')
        self.label.setText('正常模式')
        self.label_41.setText('正常模式')
        self.pushButton_2.setEnabled(False)
        self.label_11.setText('')
        self.label_13.setText('')
        self.label_15.setText('')
        self.sn_show.setText('')
        self.lineEdit_7.setText('0')
        self.lineEdit_5.setText('0')
        self.lineEdit_6.setText('1')
        self.lineEdit_3.setText('0')
        self.lineEdit_9.setText('0')
        self.lineEdit_10.setText('0')
        self.lineEdit_11.setText('1')
        self.lineEdit_12.setText('0')
        self.confignum = 0
        self.textEdit.setStyleSheet('background:white')
        self.textEdit_2.setStyleSheet('background:white')
        self.textEdit_3.setStyleSheet('background:white')

    #demarcate标定
    def demarcate(self):
        timer_dem = QTimer(self)
        timer_dem.timeout.connect(self.dem_water)
        timer_dem.start(100)
    # def dem_water(self):
    #     self.water_content_3.setText(str(random.randint(150, 225)))
    #0x11按钮事件
    # def sensordata(self):
    #     test = random.randint(200, 225)
    #     return test
    #定时获取
    def timerheart(self):
        self.timer_heart = QTimer(self)
        self.timer_heart.timeout.connect(self.sensorhandle)
        self.timer_heart.start(1000)

    #获取值传输给文本
    def sensorhandle(self):
        if self.ser.isOpen():
            self.read_heart00()
    def read_heart00(self):
        code_00 = arg_code.encode(self, '00000000', '00', '00', 9999)
        print('00发送:             ', code_00)
        time.sleep(0.5)
        self.data_send(str(code_00))

    #获取SN号
    def read_sn(self):
        if self.label_11.text() == '':
            code_00 = arg_code.encode(self,'00000000','00','00',9999)
            # print(sn)
            # self.s3__send_text.setText(str(code_00))
            self.data_send(str(code_00))
        if tar_add != '':
            self.read_01()

    #读取文件
    def read_file(self):
        global path
        filepath=path
        with open(filepath, 'rb') as f:
            global file_MD5
            global hex_commit
            comment = f.read()
            file_MD5 = hashlib.md5(comment).hexdigest()
            hex_commit = ''.join(['%02x' % b for b in comment])
            ljname = hex_commit[0:30]
            versionlj = hex_commit[30:106]
            self.label_36.setText(tools.hex_to_ascill(ljname))
            # self.label_36.setText(tools.hex_dec(versionlj))
            print('即将转换的值：',self.label_36.text())
            global size_hex_com
            global num_0b
            global bit0b
            global offset
            offset = ''
            num_0b = 0
            bit0b = 0
            self.data_num_received = 0
            # self.lineEdit.setText(str(self.data_num_received))
            self.data_num_sended = 0
            # self.lineEdit_2.setText(str(self.data_num_sended))
            print("hex_commit:     ",type(hex_commit))
            size_hex_com=len(hex_commit)
            print('MD5:      ',file_MD5)
            print('文件大小长度：',size_hex_com)
            self.progressBar.setMaximum(size_hex_com)
            self.timer_send_0b.start()
            self.log_listWidget.setEnabled(False)
            self.get_logbt.setEnabled(False)
            self.log_textview.setVisible(False)
    #0A协议
    def read_0a(self):
        global tar_add
        global filename
        self.get_logbt.setEnabled(False)
        myfilename = filename
        # self.timer_heart.stop()
        code_0a = arg_code.encode(self, tar_add, '0a', '00', '20' + myfilename + '00', )
        print('0a发送:             ',code_0a)
        # self.s3__send_text.setText(str(code_0a))
        self.data_send(str(code_0a))
        time.sleep(1.5)
        QApplication.processEvents()

    #0B协议
    def read_0b(self):
        global tar_add
        global filequire_handle
        global hex_commit
        global num_0b
        global offset
        global bit0b
        global size_hex_com
        global numi
        i = num_0b
        allfile_hex = hex_commit
        handle = filequire_handle
        one_hex_commit = allfile_hex[i:i + self.offect_update]
        one_hex_commit = ''.join(one_hex_commit)
        try:
            if self.offset_num == self.num:
                if bit0b == 2:
                    time.sleep(1)
                    code_0e = arg_code.encode(self, tar_add, '0e', '00', '0101')
                    print('0e发送:   ', code_0e)
                    self.data_send(str(code_0e))
                    self.timer_send_0b.stop()
                    self.get_logbt.setEnabled(True)
                    self.log_listWidget.setEnabled(True)
                elif bit0b == 1:
                    global file_MD5
                    file_md5 = file_MD5
                    time.sleep(3)
                    code_0c = arg_code.encode(self, tar_add, '0c', '00', handle + file_md5)
                    print('0c发送:   ',code_0c)
                    self.data_send(str(code_0c))
                    bit0b = 2
                else:
                    if i == 0 :
                        code_0b = arg_code.encode(self, tar_add, '0b', '00', handle + '00000000' + self.filequire_len + one_hex_commit)
                        self.data_send(str(code_0b))
                        print('0b发送00:             ', code_0b)
                    elif num_0b < size_hex_com and size_hex_com - num_0b > self.offect_update:
                        file_0ffset = offset  # 偏移量
                        code_0b = arg_code.encode(self, tar_add, '0b', '00',
                                                  handle + str(file_0ffset) + self.filequire_len + one_hex_commit)
                        self.data_send(str(code_0b))
                        print('0b发送:             ', code_0b)
                        print('当前差值：  ',size_hex_com - num_0b)
                        numi += 1
                        print('执行次数：   ',numi)
                        self.label_17.setText(str(size_hex_com - num_0b))
                        self.progressBar.setValue(int(num_0b))
                        # self.progressBar.setValue(self.label_17.text())
                    elif (size_hex_com - num_0b) > 0 and (size_hex_com - num_0b) <= self.offect_update:
                        print("进入这里来了")
                        one_hex_commit = allfile_hex[i:i + (size_hex_com - num_0b)]
                        endlen = tools.b2(int((size_hex_com - num_0b) / 2))
                        endlen = tools.he(endlen) + '00'
                        if len(endlen)==3:
                            endlen = '0' + endlen
                        file_0ffset = offset  # 偏移量
                        code_0b = arg_code.encode(self, tar_add, '0b', '00',
                                                  handle + str(file_0ffset) + endlen + one_hex_commit)
                        self.data_send(str(code_0b))
                        self.label_17.setText('--')
                        bit0b = 1
                        self.progressBar.setValue(int(num_0b))
                        print('0b发送:             ', code_0b)
                        print('完成出来u！！！！')
                    time.sleep(0.06)
                self.num += 1
            else:
                time.sleep(1)
                self.num = self.num - 1
        except Exception as e:
            self.timer_send_0b.stop()
            QMessageBox.information(self, "提醒", "发送异常!！！\n请重启串口进行升级")


    #01协议
    def read_01(self):
        global tar_add
        request_sensor = arg_code.encode(self, tar_add, '01', '00', 'f0')
        # self.s3__send_text.setText(str(request_sensor))
        self.data_send(str(request_sensor))
    #11协议
    def read_11(self):
        global tar_add
        request_sensor = arg_code.encode(self, tar_add, '11', '00', 9999)
        self.data_send(str(request_sensor))
        # QApplication.processEvents()
        # receive = ''#获得的值：
        # receive1 = receive.find('1102')
        # if receive != -1:

    # 接收数据
    def data_receive(self):
        try:
            num = self.ser.inWaiting()
            time.sleep(0.01)
        except:
            self.port_close()
            return None
        if num > 0:
            data = self.ser.read(num)
            num = len(data)
            # hex显示
            out_s = ''
            for i in range(0, len(data)):
                out_s = out_s + '{:02X}'.format(data[i])
            self.datareceive_handle(out_s)
        else:
            return
        if self.label.text() == '检测模式':
            self.up_butt.setEnabled(True),self.mid_butt.setEnabled(True),self.dow_butt.setEnabled(True)
        else:
            self.up_butt.setEnabled(False), self.mid_butt.setEnabled(False), self.dow_butt.setEnabled(False)
        if self.label_41.text() == '标定模式':
            self.pushButton_2.setEnabled(True)
            # self.s2__receive_text.insertPlainText(out_s)
            # 串口接收到的字符串为b'123',要转化成unicode字符串才能输出到窗口中去
            # self.s2__receive_text.insertPlainText(data.decode('iso-8859-1'))
            # self.s2__receive_text.insertPlainText(str(binascii.b2a_hex(data))[2:-1])
            # 统计接收字符的数量
            # self.data_num_received += num
            # self.lineEdit.setText(str(self.data_num_received))

      # 接收数据处理
    def datareceive_handle(self, data):
        global file_size  # 文件大小
        global my_offect_0b  # 最大支持长度十进制
        global last_offerst  # 文件大小减去偏移量的值
        # print(data)
        sof = data.find('02005647')
        if sof != -1:
            code = data[sof + 10:sof + 12]
            ###########################################00解析###############################
            if code == '00':
                print('00协议返回',data)
                global tar_add
                tar_add = data[(sof - 8):sof]  # 目标地址
                # sn=data[(sof+16):(sof+32)]   #SN号获取
                # self.sn_show.setText(tar_add)
                if len(self.sn_show.text()) > 0:
                    self.get_logbt.setEnabled(True)
                    self.openfilebt.setEnabled(True)  # 浏览文件按钮不可点击
                    self.modequery()
            ###########################################01解析###############################
            elif code == '01':
                print('01接收:', data)
                getapp = data.find('010100')
                try:
                    if len(data) > 56:
                        hw = arg_code.v0_01_hw(self, data)
                        boot = arg_code.v0_01_boot(self, data)
                        app = arg_code.v0_01_app(self, data)
                        LJ_sn = arg_code.v0_01_sn(self, data)
                        self.label_11.setText(app)
                        self.label_13.setText(hw)
                        self.label_15.setText(boot)
                        self.sn_show.setText(LJ_sn)
                        if len(self.label_11.text()) > 8 and len(self.label_13.text()):
                            self.groupBox.setVisible(True)
                            # self.groupBox_2.setVisible(True)
                            self.groupBox_3.setVisible(True)
                            self.verticalGroupBox_2.setVisible(True)
                            self.timer_get_sn.stop()
                            self.timer_heart.start(1000)
                except:
                    pass
            ###########################################05解析###############################################
            elif code == '05':
                print('05协议通了:',data)
                sndata = data.find('0501000000')
                moderundata = data.find('0501000001')
                perioddata = data.find('0501000002')
                euidata = data.find('0501000003')
                keydata = data.find('0501000004')
                waitdata = data.find('0501000005')
                if sndata != -1:
                    print('SN号修改成功')
                    QMessageBox.information(self, "提示", self.label_43.text() + "修改成功\n重启生效")
                if moderundata != -1:
                    print('mode修改成功')
                    QMessageBox.information(self, "提示", self.label_44.text() + "修改成功\n重启生效")
                if perioddata != -1:
                    print('period修改成功')
                    QMessageBox.information(self, "提示", self.label_45.text() + "修改成功\n重启生效")
                if euidata != -1:
                    print('eui修改成功')
                    QMessageBox.information(self, "提示", self.label_46.text() + "修改成功\n重启生效")
                if keydata != -1:
                    print('key修改成功')
                    QMessageBox.information(self, "提示", self.label_47.text() + "修改成功\n重启生效")
                if waitdata != -1:
                    print('key修改成功')
                    QMessageBox.information(self, "提示", self.label_48.text() + "修改成功\n重启生效")



            ###########################################06解析###############################################
            elif code == '06':
                print('06协议通了',data)
                self.label_43.setText('SN')
                self.label_44.setText('运行模式')
                self.label_45.setText('上报周期')
                self.label_46.setText('上报等待')
                self.label_47.setText('eui')
                self.label_48.setText('key')
                configreply = data.find('0601FF')
                configreply00 = data.rfind('06010000')
                reply00 = data.rfind('0601000000')
                reply01 = data.rfind('0601000001')
                reply02 = data.rfind('0601000002')
                reply03 = data.rfind('0601000003')
                reply04 = data.rfind('0601000004')
                reply05 = data.rfind('0601000005')
                end00 = data.rfind('00')
                if configreply00 != -1:
                    if reply00 != -1:
                        self.fig = 2
                        configdata = data[configreply00+10 : -6]
                        configdata = tools.hex_to_ascill(configdata)
                        self.confignum += 1
                        self.lineEdit_32.setText(configdata)
                    if reply01 != -1:
                        configdata = data[configreply00 + 10: -6]
                        configdata = tools.hex_to_ascill(configdata)
                        self.confignum += 1
                        self.lineEdit_33.setText(configdata)
                    if reply02 != -1:
                        configdata = data[configreply00 + 10: -6]
                        configdata = tools.hex_to_ascill(configdata)
                        self.confignum += 1
                        self.lineEdit_34.setText(configdata)
                    if reply03 != -1:
                        configdata = data[configreply00 + 10: -6]
                        configdata = tools.hex_to_ascill(configdata)
                        self.confignum += 1
                        self.lineEdit_35.setText(configdata)
                    if reply04 != -1:
                        configdata = data[configreply00 + 10: -6]
                        configdata = tools.hex_to_ascill(configdata)
                        self.confignum += 1
                        self.lineEdit_36.setText(configdata)
                    if reply05 != -1:
                        configdata = data[configreply00 + 10: -6]
                        configdata = tools.hex_to_ascill(configdata)
                        self.confignum += 1
                        self.lineEdit_37.setText(configdata)
                if self.confignum == 5 and self.lineEdit_35.text() != '' and self.lineEdit_36.text() != '':
                    QMessageBox.information(self, "提示", "配置项已搜索完或")
                    self.timer_heart.start(1000)
                    self.timer_getconfig.stop()
                    self.confignum = 0
                if configreply !=-1:
                    self.timer_getconfig.stop()
                    self.confignum = 0
                    self.fig = 1
                    QMessageBox.information(self, "提示", "未搜索到")

            ###########################################0A解析###############################################
            elif code == '0A':
                print('0a返回', data)
                self.get_logbt.setEnabled(True)
                filequire = data.find('0A0100')
                if filequire!=-1:
                    global filequire_handle        #文件传输handle
                    global offect_0b               # 支持长度
                    global my_offect_0b
                    filequire_handle = data[filequire + 6:filequire + 8]
                    filequire_space = data[filequire + 8:filequire + 16]
                    print("存储控件大小：    ",filequire_space)
                    offect_0b = data[filequire + 16:filequire + 20]  # 读取大小字节限制
                    self.filequire_len = data[filequire + 16:filequire + 20]
                    file_space = tools.small_to_big1(filequire_space)  # 获取空间大小，并转换成十进制
                    file_size = int(tools.hex_dec(file_space))
                    # file_space = tools.hex_dec(file_space)
                    my_offect_0b = tools.hex_dec(tools.small_to_big1(offect_0b))
                    self.offect_update = int(tools.hex_dec(tools.small_to_big1(offect_0b))) * 2
                    print('0a获取-空间大小:',file_size)
                    self.progressBar_2.setMaximum(file_size)
                    print('传输长度:',my_offect_0b)
                    print('传输长度offect_update:',self.offect_update)
                    self.upbut.setEnabled(True)
                else:pass
            ###########################################0B解析###############################################
            elif code == '0B':
                print('0b接收：',data)
                self.upbut.setText('传输中')
                Offset_ide = data.find('0B0100')
                global num_0b
                global size_hex_com
                # error = data[Offset_ide + 4:Offset_ide + 6]
                try:
                    if Offset_ide != -1:
                        global offset  # 文件传输偏移量
                        offset = data[Offset_ide + 8:Offset_ide + 16]         #已经接收到的数据偏移
                        if self.num >self.offset_num:
                            self.offset_num += 1
                        fsize = (tools.hex_dec(tools.small_to_big1(offset)))
                        last_offerst = (int(file_size) - int(fsize))
                        self.progressBar_2.setValue(int(fsize))
                        print("last_offerst打印值：    ",last_offerst)
                        global save_path
                        if last_offerst > int(my_offect_0b):   #文件大小减去偏移量大小大于最大长度
                            me_data = data[Offset_ide + 20:-4]
                            if save_path != '':
                                # self.log_textview.setText(str(last_offerst))
                                filepath = save_path
                                try:
                                    file = open(filepath, 'a+')
                                    # print('打开文件成功')
                                    for j in tools.hex_to_ascill(me_data):
                                        file.write(j)
                                    file.close()
                                except Exception as e:
                                    pass

                        # self.log_textview.setText(str(last_offerst))
                        elif last_offerst == 0:
                            self.timer_send_0f_0b.stop()
                            QMessageBox.information(self, "提示", "下载成功！！！")
                            me_data = data[Offset_ide + 20:-4]
                            # me_data = tools.hex_to_ascill(me_data)
                            # global save_path
                            if save_path != '':
                                # self.log_textview.setText(str(last_offerst))
                                filepath = save_path
                                try:
                                    file = open(filepath, 'a+')
                                    # print('打开文件成功')
                                    for j in tools.hex_to_ascill(me_data):
                                        file.write(j)
                                    file.close()
                                except Exception as e:
                                    pass
                            else:
                                pass
                        # offsetlen = tools.small_to_big1(offset)
                        # offsetlen = tools.hex_dec(offset)
                        # print(offsetlen)
                        if size_hex_com !='':
                            if offset != 0 and (num_0b + self.offect_update) <= size_hex_com:
                                num_0b = num_0b + self.offect_update
                                print('长度：', num_0b)
                            else:
                                print('最终长度+：', num_0b)
                        else:pass
                    else:
                        self.timer_send_0b.stop()
                        self.timer_send_0f_0b.stop()
                        QMessageBox.information(self, "提醒","升级异常！！\n请重启串口进行升级" )
                except Exception as e:
                    self.timer_send_0b.stop()
                    self.timer_send_0f_0b.stop()
                    QMessageBox.information(self, "提醒", "串口异常！！！\n请重启串口进行升级")



            ###########################################0C解析###############################################
            elif code == '0C':
                self.upbut.setText('校验中')
                return_code_0c = data.find('0C01')
                print('0c:        ', data)
                QMessageBox.information(self, "提示", "升级完成,设备重启\n固件版本会更新")
                self.progressBar.setValue(100)
                if self.num > self.offset_num:
                    self.offset_num += 1
            ###########################################0E解析###############################################
            elif code == '0E':
                print('0e接收:        ', data)
                self.upbut.setText('完成')
                # self.label_11.setText(' ')
                # self.timer_get_sn.start(1000)
                upreset = data.find('0E010002')
                reset = data.find('0E010001')
                if upreset != -1:
                    self.timer_get_sn.start(1000)
                    self.label_11.setText(' ')
                    self.timer_heart.start()
                    QMessageBox.information(self, "提示", "升级完成：")
                if reset != -1:
                    self.timer_get_sn.start(1000)
                    self.label_11.setText(' ')
                    QMessageBox.information(self, "提示", "设备重启，请等待8S")
                Offset_ide = data.find('0D0100')
                if self.num > self.offset_num:
                    self.offset_num += 1
            ###########################################0F解析###############################################
            elif code == '0F':
                print('0F协议返回为:', data)
                data = data[:int(tools.hex_dec(data[2:4])) * 2]
                ide_0f = data.find('0F0100')
                if ide_0f != -1:
                    file_code = data[ide_0f + 6:ide_0f + 14]
                    file_createtime = data[ide_0f + 14:ide_0f + 22]
                    file_lasttime = data[ide_0f + 22:ide_0f + 30]
                    filename_of = data[ide_0f + 30:-6]
                    createtime = tools.size_time(file_createtime)
                    lasttime = tools.size_time(file_lasttime)
                    filename = tools.hex_to_ascill(filename_of)
                    # print(filename,         createtime,                        lasttime)
                    self.log_listWidget.addItem(filename + '          ' + createtime + '        ' + lasttime+'               '+filename_of)
                    global last_num
                    file_code1 = tools.small_to_big1(file_code)  # 大小端转换
                    file_code2 = tools.hex_dec(file_code1)  # 转换十进制
                    file_code3 = int(file_code2) + 1  # 转换成十进制后加1
                    file_code4 = hex(file_code3)[2:]  # 加1 后继续转换成十六进制
                    file_code5 = '0' * (8 - len(file_code4)) + str(file_code4)  # 转换成十六进制后，补全8个0
                    last_num = tools.small_to_big1(file_code5)
                    # self.log_list.set(filename_of)

                else:
                    self.timer_get_log.stop()
                    QMessageBox.information(self, "提示", "获取完成：")
                    self.get_logbt.setEnabled(True)
                    self.log_listWidget.setEnabled(True)
                    self.log_listWidget.clicked.connect(self.get_onelog)
            ###################################窖池新增功能  ---11解析协议####################################
            elif code =="11":
                print('11返回:', data)
                getdata = data.find('110100')
                if getdata != -1:
                    port1 = self.port1_data(data)
                    print('类型：',type(port1))
                    print('传感器获取的数据信息：',port1)
                # else:
                    # QMessageBox.information(self, "提示", "获取传感器失败，\n查询当前是否为采样模式")
                    # self.timer_getsensordata.stop()
                # port3 = arg_code.port3_data(self, data)
                # port4 = arg_code.port4_data(self, data)
                # self.water_content_4.setText(port1)
                # self.water_content_5.setText(port2)
                # self.water_content_6.setText(port3)
            ###################################窖池新增功能  ---FE解析协议####################################
            elif code == "FE":
                print('FE返回:', data)
                readdata = data.rfind('FE01000000')
                writedata = data.find('FE01000001')
                error = data.find('FE01FE')
                mode = data.find('FE0100')
                query = data.find('FE010002')
                querynor = data.find('FE010000')
                quire = data.find('FE010001')
                if quire != -1:
                    self.label.setText('检测模式')
                if query != -1:
                    self.label_41.setText('标定模式')
                if mode != -1 and self.checksordata == 1 or self.checksordata == 2 or self.checksordata == 3:
                    # self.get_jc_data()
                    print('检测数据的进来了------------------------')
                if querynor !=-1 and self.modeswitchnum == 1:
                    self.label_41.setText('正常模式')
                    self.modeswitchnum = 0
                if mode != -1 and self.modeswitchnum == 1:
                    self.label_41.setText('标定模式')
                    self.reboot()
                    QMessageBox.information(self, "提示", "重启5s\n切换模式为：标定模式")
                    self.modeswitchnum = 0
                if mode != -1 and self.modeswitchnum == 2:
                    self.label_41.setText('正常模式')
                    self.label.setText('正常模式')
                    self.reboot()
                    QMessageBox.information(self, "提示", "重启5s\n切换模式为：正常模式")
                    self.modeswitchnum = 0
                if mode != -1 and self.modeswitchnum == 3:
                    self.label.setText('检测模式')
                    self.reboot()
                    QMessageBox.information(self, "提示", "重启5s\n切换模式为：检测模式")
                    self.modeswitchnum = 0
                if readdata !=-1:
                    if len(data) > 268:
                        print('FE读标定值正常')
                        tempa = data[readdata + 14:readdata + 22]
                        tempb = data[readdata + 22:readdata + 30]
                        tempc = data[readdata + 30:readdata + 38]
                        tempd = data[readdata + 38:readdata + 46]
                        airpressa = data[readdata + 46:readdata + 54]
                        airpressb = data[readdata + 54:readdata + 62]
                        airpressc = data[readdata + 62:readdata + 70]
                        airpressd = data[readdata + 70:readdata + 78]
                        oxygena = data[readdata + 78:readdata + 86]
                        oxygenb = data[readdata + 86:readdata + 94]
                        oxygenc = data[readdata + 94:readdata + 102]
                        oxygend = data[readdata + 102:readdata + 110]
                        carbona = data[readdata + 110:readdata + 118]
                        carbonb = data[readdata + 118:readdata + 126]
                        carbonc = data[readdata + 126:readdata + 134]
                        carbond = data[readdata + 134:readdata + 142]
                        alcohola = data[readdata + 142:readdata + 150]
                        alcoholb = data[readdata + 150:readdata + 158]
                        alcoholc = data[readdata + 158:readdata + 166]
                        alcohold = data[readdata + 166:readdata + 174]
                        waterdataa = data[readdata + 174:readdata + 182]
                        waterdatab = data[readdata + 182:readdata + 190]
                        waterdatac = data[readdata + 190:readdata + 198]
                        waterdatad = data[readdata + 198:readdata + 206]
                        cropdataa = data[readdata + 206:readdata + 214]
                        cropdatab = data[readdata + 214:readdata + 222]
                        cropdatac = data[readdata + 222:readdata + 230]
                        cropdatad = data[readdata + 230:readdata + 238]
                        if len(waterdataa) == 8 and len(waterdatad) == 8:
                            self.lineEdit_13.setText(tools.strtofloat(tempa))
                            self.lineEdit_14.setText(tools.strtofloat(tempb))
                            self.lineEdit_15.setText(tools.strtofloat(tempc))
                            self.lineEdit_16.setText(tools.strtofloat(tempd))
                            self.lineEdit_17.setText(tools.strtofloat(alcohola))
                            self.lineEdit_18.setText(tools.strtofloat(alcoholb))
                            self.lineEdit_19.setText(tools.strtofloat(alcoholc))
                            self.lineEdit_20.setText(tools.strtofloat(alcohold))
                            self.lineEdit_8.setText(tools.strtofloat(carbona))
                            self.lineEdit_21.setText(tools.strtofloat(carbonb))
                            self.lineEdit_22.setText(tools.strtofloat(carbonc))
                            self.lineEdit_23.setText(tools.strtofloat(carbond))
                            self.lineEdit_24.setText(tools.strtofloat(airpressa))
                            self.lineEdit_25.setText(tools.strtofloat(airpressb))
                            self.lineEdit_26.setText(tools.strtofloat(airpressc))
                            self.lineEdit_27.setText(tools.strtofloat(airpressd))
                            self.lineEdit_28.setText(tools.strtofloat(oxygena))
                            self.lineEdit_29.setText(tools.strtofloat(oxygenb))
                            self.lineEdit_30.setText(tools.strtofloat(oxygenc))
                            self.lineEdit_31.setText(tools.strtofloat(oxygend))
                            self.lineEdit_7.setText(tools.strtofloat(waterdataa))
                            self.lineEdit_5.setText(tools.strtofloat(waterdatab))
                            self.lineEdit_6.setText(tools.strtofloat(waterdatac))
                            self.lineEdit_3.setText(tools.strtofloat(waterdatad))
                            self.lineEdit_9.setText(str(float(tools.strtofloat(cropdataa)) * 10000))
                            self.lineEdit_10.setText(str(float(tools.strtofloat(cropdatab)) * 10000))
                            self.lineEdit_11.setText(str(float(tools.strtofloat(cropdatac)) * 10000))
                            self.lineEdit_12.setText(str(float(tools.strtofloat(cropdatad)) * 10000))
                            self.lineEdit_13.setCursorPosition(0),self.lineEdit_14.setCursorPosition(0),self.lineEdit_15.setCursorPosition(0)
                            self.lineEdit_16.setCursorPosition(0),self.lineEdit_17.setCursorPosition(0),self.lineEdit_18.setCursorPosition(0)
                            self.lineEdit_19.setCursorPosition(0),self.lineEdit_20.setCursorPosition(0),self.lineEdit_8.setCursorPosition(0)
                            self.lineEdit_21.setCursorPosition(0),self.lineEdit_22.setCursorPosition(0),self.lineEdit_23.setCursorPosition(0)
                            self.lineEdit_24.setCursorPosition(0),self.lineEdit_25.setCursorPosition(0),self.lineEdit_26.setCursorPosition(0)
                            self.lineEdit_27.setCursorPosition(0),self.lineEdit_28.setCursorPosition(0),self.lineEdit_29.setCursorPosition(0)
                            self.lineEdit_30.setCursorPosition(0),self.lineEdit_31.setCursorPosition(0),self.lineEdit_9.setCursorPosition(0)
                            self.lineEdit_10.setCursorPosition(0),self.lineEdit_11.setCursorPosition(0),self.lineEdit_12.setCursorPosition(0)
                            self.lineEdit_3.setCursorPosition(0),self.lineEdit_5.setCursorPosition(0),self.lineEdit_6.setCursorPosition(0)
                            self.lineEdit_7.setCursorPosition(0)
                            QMessageBox.information(self, "提示", "读取标定值成功")
                    else:
                        QMessageBox.information(self, "提示", "读取不全，再次获取")
                if writedata != -1 and self.pushButton_2.isEnabled() == True:
                    # self.reboot()
                    if self.comboBox_2.currentText() == '上层':
                        self.textEdit.setStyleSheet("background:green")
                    elif self.comboBox_2.currentText() == '中层':
                        self.textEdit_3.setStyleSheet("background:green")
                    elif self.comboBox_2.currentText() == '下层':
                        self.textEdit_2.setStyleSheet("background:green")
                    QMessageBox.information(self, "提示", "标定成功，\n可读取数值进一步确认")
                if error != -1:
                    QMessageBox.information(self, "提示", "获取数据失败，\n请重试")



            #################################################################################
        else:
            print('返回数据异常')

    # 响应选listview 中选中的数据
    def get_onelog(self, qModelIndex):
        # 对数据经行判断
        errocod=self.log_listWidget.selectedIndexes()
        for i in errocod:
            if i.row()==0:
                pass
            else:
                my_list_text=self.log_listWidget.selectedItems()
                for j in my_list_text:
                    global smal_filename  # 0f 协议传输十六进制文件路径和文件名
                    global save_name
                    name_first=(j.text().rindex(' '))
                    big_filename=(j.text()[-1:name_first:-1])
                    smal_filename=big_filename[::-1]
                    aa = (j.text().index(' '))
                    bb = (j.text().index('/'))
                    save_name = j.text()[bb + 1:aa]
                    self.createtime = j.text()[aa+10:aa+29]
                    self.createtime = self.createtime.replace(':','_')
                    # print('获取值：',createtime)
                    self.download_logbt.setEnabled(True)

                    print(smal_filename)
                    print(save_name)

    # 清除显示
    def send_data_clear(self):
        self.s3__send_text.setText("")

    def receive_data_clear(self):
        self.s2__receive_text.setText("")

    # 浏览升级文件事件
    def open_event(self):
        directory1 = QFileDialog.getOpenFileName(None, "选择文件", './',"files(*.img)")
        global path
        global filename  # 文件名
        if directory1[0] == '':
            pass  # 防止关闭或取消导入关闭所有页面
        else:
            path = directory1[0]
            filename_ide = path.rfind('/')
            filename_asi = path[filename_ide + 1:]
            filename = tools.ascill_to_hex(filename_asi)
            print('文件名：  ',filename)
            self.lineEdit_4.setText(path)
            self.upbut.setText('升级')
            self.read_0a()

    # 保存log事件
    def save_event(self):
        global save_path
        fileName2, ok2 = QFileDialog.getSaveFileName(None, "文件保存", "./")
        # print(fileName2)  # 打印保存文件的全部路径（包括文件名和后缀名）
        save_path = fileName2

    #升级事件
    #1、像设备发送OA协议，后去传输字节大小，然后根据字节大小对升级文件进行切割。
    #2、将切割的数据组装到0B协议，进行发送
    def updata_event(self):
        self.timer_heart.stop()
        self.upbut.setEnabled(False)
        self.read_file()

    # 保存窗口
    def save_receive_to_file(self):
        if self.lineEdit_4.text() == '':
            win32api.MessageBox(0, "请先输入SN号再保存！", "提醒", win32con.MB_ICONWARNING)
        elif len(self.lineEdit_4.text()) != 16:
            win32api.MessageBox(0, "SN号有16位吗？", "提醒", win32con.MB_ICONWARNING)
        else:
            file_name = QFileDialog.getSaveFileName(self, '保存窗口为txt文件', self.lineEdit_4.text() + '_' +
                                                    time.strftime('%Y_%m_%d_%H_%M', time.localtime()) + '.txt')
            if file_name[1]:
                with open(file_name[0], 'a') as file:
                    my_text = self.s2__receive_text.toPlainText()
                    file.write(my_text)
            else:
                pass


    # 发送数据 -
    # 变量stringdata为封装好的发送行
    def data_send(self, stringdata):
        if self.ser.isOpen():
            input_s = stringdata
            if input_s != "":
                # 非空字符串
                # ascii发送
                input_s = bytes.fromhex(input_s)
                # input_s = input_s.encode('utf-8')
                num = self.ser.write(input_s)
                # self.data_num_sended += num
                # self.lineEdit_2.setText(str(self.data_num_sended))
        else:
            pass

def mainwindows():
    app = QtWidgets.QApplication(sys.argv)
    myshow = Pyqt5_Serial()
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    # with open("darkorange.qss") as f:
    #     qss = f.read()
    # app.setStyleSheet(qss)
    # app.setStyleSheet(PyQt5_stylesheets.load_stylesheet_pyqt5(style="style_blue"))
    myshow.show()
    # QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    sys.exit(app.exec_())

if __name__ == '__main__':
    # workThread = WorkThread()
    # workThread.start()
    mainwindows()

