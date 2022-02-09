# coding:utf-8
import threading
import time
from ctypes import *
import datetime
from crcmod import *
from binascii import *
from threading import Thread, Lock

def encode(dst, cmd, attribute, desploy=9999):
    sof = '0b'  # 帧同步11或0B
    now = datetime.datetime.now()
    then = datetime.datetime(1970, 1, 1)
    timesence = now - then
    timstamp = int(timesence.total_seconds())
    timstamp = (hex(timstamp))
    timstamp = timstamp[2:]  # 时间戳
    src = '02005647'  # 源设备地址  已知
    dst = dst  # 目标设备序地址
    seq = '00'  # 帧序列号
    cmd = cmd  # 更改命令ID
    # print(cmd)
    attribute = attribute  # 命令属性
    payload = desploy
    if payload == 9999:
        lenth = int((len(sof) + len(timstamp) + len(src) + len(dst) +
                    len(seq) + len(cmd) + len(attribute) + 4 + 2) / 2)
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
    readcrcout = hex(crc16(unhexlify(crc16data))).upper()
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
    j = tuple(int(z, 16) for z in allsizicode)
    print(j)
    print("初始化协议成功")
    return j





def decode(decodedata):
    print(decodedata)
    if len(decodedata) > 0:
        # decodedata=decodedata
        codeid = decodedata[15]
        print(codeid)
        print("协议ID是", codeid)
        if codeid == '00':
            print("协议属性是：", decodedata[16])
            att_code = (decodedata[18:26][::-1])
            att_code = ''.join(tuple(att_code))
            print("设备SN号是：", att_code)
        elif codeid == '01':
            print("协议属性是：", decodedata[16])
            # 获取plyload整串数据
            barr = decodedata[:-2][17:]
            print("设备返回的payload数据是：", ''.join(barr))

        elif codeid == '02':
            print("协议属性是：", decodedata[16])
            # 获取plyload整串数据
            barr = decodedata[:-2][17:]
            print("设备返回的payload数据是：", ''.join(barr))

        elif codeid == '03':
            print("协议属性是：", decodedata[16])
            # 获取plyload整串数据
            barr = decodedata[:-2][17:]
            print("设备返回的payload数据是：", ''.join(barr))

        elif codeid == '04':
            print("协议属性是：", decodedata[16])
            # 获取plyload整串数据
            barr = decodedata[:-2][17:]
            print("设备返回的payload数据是：", ''.join(barr))

        elif codeid == '05':
            print("协议属性是：", decodedata[16])
            # 获取plyload整串数据
            barr = decodedata[:-2][17:]
            print("设备返回的payload数据是：", ''.join(barr))

        elif codeid == '06':
            print("协议属性是：", decodedata[16])
            # 获取plyload整串数据
            barr = decodedata[:-2][17:]
            print("设备返回的payload数据是：", ''.join(barr))
        elif codeid == '0A' or codeid == '0a':
            print("协议属性是：", decodedata[16])
            # 获取plyload整串数据
            barr = decodedata[:-2][17:]
            print("设备返回的payload数据是：", ''.join(barr))
        elif codeid == '0B':
            print("协议属性是：", decodedata[16])
            # 获取plyload整串数据
            barr = decodedata[:-2][17:]
            print("设备返回的payload数据是：", ''.join(barr))
        elif codeid == '0C':
            print("协议属性是：", decodedata[16])
            # 获取plyload整串数据
            barr = decodedata[:-2][17:]
            print("设备返回的payload数据是：", ''.join(barr))
        elif codeid == '15' :
            if decodedata[16] == '02':
                print("设备推送数据")
            if decodedata[17] == '01':
                print("子模块为主板")
            elif decodedata[17] == '04':
                print("子模块为电池板")
        elif codeid == '85' :
            if decodedata[16] == '02':
                print("设备推送姿态状态")
            print("imu状态：", decodedata[18])
            print("应答状态：", decodedata[17])



