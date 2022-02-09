# coding:utf-8
# @FileName  :tools.py
# @Time      :2021/4/28 15:23
# @Author    :liuman
import binascii
import time
import struct

#十六进制转换十进制
def hex_dec(data):
    return str(int(data.upper(), 16))
#十六进制转换成二进制
def hex_bin(data):
    return '0'+bin(int(data,16))[2:]

#二进制转十进制
def bin_dec(data):
    return str(int(data,2))

#十六进制解析时间戳
def size_time(data):
    medata = []
    for i in range(0, len(data), 2):
        medata.append(data[i:i + 2])
    medata=''.join(medata[::-1])
    mydata=hex_dec(medata)
    time_ar = time.localtime(int(mydata))
    endtime = time.strftime("%Y-%m-%d:%H:%M:%S", time_ar)
    # print(endtime)
    return endtime

#十六进制转换成二进制并取[15:4][3:0]后转换成十进制
def hex_bin1(data):
    undata = data[::-1]
    undata = ''.join(undata)
    a= int(undata,16)
    b='{:016b}'.format(a)

    a_15_4=b[:12]
    a_3_0 =b[12:16]

    a_15_4=hex(int(a_15_4,2))[2:]
    # print(a_15_4)
    if len(a_15_4)==1:
        a_15_4='0x'+'00'+a_15_4
        # print(a_15_4)
    elif len(a_15_4)==2:
        a_15_4='0x'+'0'+a_15_4

    return a_15_4,a_3_0


#十六进制转换成二进制并取[15:8][7:0]后转换成十进制(设备事件专用)
def hex_bin2(data):
    # print(data)
    undata = data[::-1]
    # print(undata)
    undata = ''.join(undata)
    a= int(undata,16)
    b='{:016b}'.format(a)

    a_15_8=b[:8]
    a_7_0 =b[8:16]

    a_15_8=hex(int(a_15_8,2))[2:]
    # print(a_15_4)
    if len(a_15_8)==1:
        a_15_8='0x'+'0'+a_15_8
        # print(a_15_8)
    elif len(a_15_8)==2:
        a_15_8='0x'+a_15_8

    return a_15_8,a_7_0

#十六进制转换成二进制并取[7:4][3:0]后转换成十进制
def hex_bin3(data):
    a= int(data,16)
    b='{:016b}'.format(a)
    # print(b)
    a_7_4=b[8:12]
    a_3_0 =b[12:16]
    # a_3_0 = hex(int(a_3_0, 2))[2:]
    return a_7_4,a_3_0

#10协议专用  bit[31:25] - 电池电量  bit[24:10] - 充电电压 bit[09:03] - 信号质量 bit[02:00] - 电源状态
def hex_bin4(data):
    undata = data[::-1]
    undata = ''.join(undata)
    b=bin(int(undata,16))[2:]
    if len(b)<32:
        b=(32-len(b))*'0'+b
    else:b=b
    a_31_25 = bin_dec(b[0:7])
    a_24_10 = bin_dec(b[7:22])
    a_09_03 = bin_dec(b[22:28])
    a_02_00 = b[28:32]
    return a_31_25,a_24_10,a_09_03,a_02_00


#10协议专用   bit[31:29] - SD卡状态 bit[28:25] - Modem类型  bit[24:21] - Modem状态  bit[20:18] - GPS模块状态
#bit[17:10] - 传感器连接状态，每个2bit代表一个物理接口  bit[09:09] - 扩展IO芯片状态  bit[08:07] - 温度报警 bit[06:06] - 扫描状态
#bit[05:04] - 升级状态  bit[01:00] - 工作模式
def hex_bin5(data):
    undata = data[::-1]
    undata = ''.join(undata)
    # print(undata)
    b=bin(int(undata,16))[2:]
    if len(b)<32:
        b=(32-len(b))*'0'+b
    else:b=b
    # print(b)
    a_31_29 = b[0:3]
    a_28_25 = b[3:7]
    a_24_21 = b[7:11]
    a_20_18 = b[11:14]
    a_17_10 = b[14:22]
    a_09_09 = b[22]
    a_08_07 = b[23:25]
    a_06_06 = b[25]
    a_05_04 = b[26:28]
    a_01_00 = b[30:32]
    return a_31_29,a_28_25,a_24_21,a_20_18,a_17_10,a_09_09,a_08_07,a_06_06,a_05_04,a_01_00

#小端模式转大端模式(协议01专用)
def small_to_big(data):
    undata = data[::-1]
    undata = ''.join(undata)
    undata = hex_dec(undata[0:2]) + '.' + hex_dec(undata[2:4]) + '.' + hex_dec(undata[4:])
    # undata = hex_dec(undata)
    return undata

#字符串翻转并转化成字符串
def unsize(data):
    undata=data[::-1]
    undata=''.join(undata)

    return undata

#字符串翻转，并解析时间戳
def unsize_time(data):
    mydata=data[::-1]
    # print(mydata)
    mydata=''.join(mydata)
    mydata=str(int(mydata.upper(), 16))
    time_ar = time.localtime(int(mydata))
    endtime = time.strftime("%Y-%m-%d：%H：%M：%S", time_ar)
    # print(endtime)
    return endtime


#传感器float数据解析
def size_to_float(data):
    if data ==['00', '00', '00', '00']:
        return 0
    else:
        # newdata=[]
        # for i in range(0,len(data),2):
        #     newdata.append(data[i*1:i+2])
        # print(newdata)
        # mydata=newdata[::-1]
        mydata=data[::-1]
        # print(mydata)
        mydata=''.join(mydata)
        # print(mydata)
        mydata=struct.unpack('!f',bytes.fromhex(mydata))[0]
        mydata=round(mydata,3)
        return mydata

def size_to_double(data):
    if data == ['00', '00', '00', '00']:
        return 0
    else:
        mydata = ''.join(data)
        # print(mydata)
        mydata = struct.unpack('d', binascii.unhexlify(mydata))
        # print(type(str(mydata[0])))
        return str(mydata[0])
        # float_

#十六进制转换ASmal
def hex_to_ascill(data):
    medata = []
    for i in range(0, len(data), 2):
        medata.append(chr(int(data[i:i + 2], 16)))
    return ''.join(medata)


#ASmal转换十六进制
def ascill_to_hex(data):
    medata=[]
    for c in data:
        medata.append(str(hex(ord(c))[2:]))
        medata1=''.join(medata)

    return medata1

#大小端转换
def small_to_big1(data):
    newdata=[]
    for i in range(0,len(data),2):
        newdata.append(data[i*1:i+2])
    mydata=newdata[::-1]
    undata = ''.join(mydata)
    # print(ddata)
    return undata

#十进制转换十六进制
def dec_hex(data):
    return (hex(data)[2:])

#十六进制转字符串
def hex_to_str1(data):
    data=binascii.unhexlify(data)
    return data.decode('utf-8')

def b2(str1):                                    #获得十进制转二进制的字符串
    bi2=str(bin(int(str1))).replace('0b','')
    return bi2

def he(str0):                                      #二进制字符串转大写十六进制
    strw=str(hex(int(str0,2))).replace('0x','').upper()
    return strw
def floattostr(f):                              #float类型转换成str类型
    f = float(f)
    put = hex(struct.unpack('<I', struct.pack('<f', f))[0])
    put = str(put[2:])
    if put =='0':
        put = '00000000'
    put = small_to_big1(put)
    return put
def strtofloat(f):                              #str类型转换成float类型
    f = small_to_big1(f)
    put = struct.unpack('!f', bytes.fromhex(f))[0]
    put ='{:.12f}'.format(put)
    return str(put)

def as_num(x):
    y = '{:.12f}'.format(x) # 5f表示保留5位小数点的float型
    return(y)

# if __name__ == '__main__':
#     aa = ascill_to_hex('b2edf4a38bc6afd8')
#     print(aa)
#     aa = hex_to_ascill('354A0C41dbce003a')
#     print(aa)
#     def as_num(x):
#         y = '{:.7f}'.format(x)
#         return (y)
#     a = 1.37e-05
#     print(as_num(a))
    # aa = float(f)
    # print(aa)
    # put = hex(struct.unpack('<I', struct.pack('<f', f))[0])
    # print('输出',put[2:])
#
#     put = str(put[2:])
#     print('string类型',type(put),put)