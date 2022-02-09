# coding:utf-8
# @FileName  :agree_dis.py
# @Time      :2021/9/15 20:57
# @Author    :liuman
from datetime import datetime
import binascii

import win32api
import win32con
from crcmod import crcmod
from tools import small_to_big1
import tools

class arg_code(object):
    def encode(self, dst, cmd, attribute, desploy=9999): #目标地址，协议ID，命令属性，payload
        sof = '0b'  # 帧同步11或0B
        now = datetime.now()
        then = datetime(1970, 1, 1, 8)
        timesence = now - then
        timstamp = hex(int(timesence.total_seconds()))[2:]
        timstamp= small_to_big1(timstamp)
        src = '02005647'  # 源设备地址  已知
        dst = dst  # 目标设备序地址
        seq = '00'  # 帧序列号
        cmd = cmd  # 更改命令ID
        # print(cmd)
        attribute = attribute  # 命令属性
        payload = desploy
        if payload == 9999:
            lenth = int((len(sof) + len(timstamp) + len(src) + len(dst) +len(seq) + len(cmd) + len(attribute) + 4 + 2) / 2)
        else:
            lenth = int((len(sof) + len(timstamp) + len(src) + len(dst) + len(seq) + len(cmd) + len(attribute) + len(
                desploy) + 4 + 2) / 2)
        len1 = format(lenth, 'x')
        # 组合后求出最后两位crc的值
        if payload == 9999:
            sitecode = sof + len1 + timstamp + src + dst + seq + cmd + attribute
            # print(sitecode)
        else:
            sitecode = sof + len1 + timstamp + src + dst + seq + cmd + attribute + desploy
            # print(sitecode)
            # 获取CRC位数
        crc16data = sitecode
        # print(crc16data)
        crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xFFFF, xorOut=0x0000)
        readcrcout = hex(crc16(binascii.unhexlify(crc16data))).upper()
        str_list = list(readcrcout)
        if len(str_list) < 6:
            str_list.insert(2, '0' * (6 - len(str_list)))  # 位数不足补0
        crc_data = "".join(str_list)
        # print(crc_data)
        crc_data = crc_data[2:]
        a1 = crc_data[0:2]
        a2 = crc_data[2:]
        crccode = a2 + a1
        # print(crccode)

        # 完整协议
        allcode = sitecode + crccode
        # print(allcode)
        # return allcode
        # 对完整协议进行格式化：使其符合发送协议的格式
        allsizicode = []
        i = 0
        while i < len(allcode):
            allsizicode.append(allcode[i:i + 2])
            i += 2
        # j = tuple(int(z, 16) for z in allsizicode)
        # print(j)
        # print("初始化协议成功")
        return allcode

    def v0_01_hw(self,data):
        getapp = data.find('010100')
        app = str(int(data[getapp + 32:getapp + 34],16)) + '.' + str(int(data[getapp + 30:getapp + 32],16)) + '.' + \
              str(int(small_to_big1(data[getapp + 26:getapp + 30]),16))
        return app
    def v0_01_boot(self, data):
        getapp = data.find('010100')
        app = str(int(data[getapp + 42:getapp + 44],16)) + '.' + str(int(data[getapp + 40:getapp + 42], 16)) + '.' + \
              str(int(small_to_big1(data[getapp + 36:getapp + 40]), 16))
        return app
    def v0_01_app(self, data):
        getapp = data.find('010100')
        app = str(int(data[getapp + 52:getapp + 54],16)) + '.' + str(int(data[getapp + 50:getapp + 52],16)) + '.' + \
              str(int(small_to_big1(data[getapp + 46:getapp + 50]), 16))
        return app
    def v0_01_sn(self, data):
        getapp = data.find('010100')
        app = small_to_big1(data[getapp + 8:getapp + 24])
        return app
    def port1_data(self, data):
        newdata = []
        getdata = data.find('110100')
        cutdata = data[getdata + 6:len(data)-4]
        for i in range(0, len(cutdata), 2):
            newdata.append(cutdata[i * 1:i + 2])
        print('截取的部分： ',newdata)
        self.Sensor_data(self,newdata)
    def port2_data(self, data):
        request_11 = data.rfind('110100')
    def port3_data(self, data):
        request_11 = data.rfind('110100')
    def port4_data(self, data):
        request_11 = data.rfind('110100')
    #传感器个数，数据处理站：
    def sensor_data(self,num):
        request_11 = num.rfind('110100')
