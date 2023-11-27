#!/usr/bin/env python3
from binascii import b2a_hex
import re
import sys
import datetime
from Crypto.Cipher import AES
from binascii import a2b_hex
import uuid
import socket
from time import ctime

import datetime
import time
import ntplib
import requests

from utils.\
    log import log

date = '20231227'



def get_beijin_time():
    try:
        url = 'https://beijing-time.org/'
        request_result = requests.get(url=url)
        if request_result.status_code == 200:
            headers = request_result.headers
            net_date = headers.get("date")
            gmt_time = time.strptime(net_date[5:25], "%d %b %Y %H:%M:%S")
            bj_timestamp = int(time.mktime(gmt_time) + 8 * 60 * 60)
            return datetime.datetime.fromtimestamp(bj_timestamp)
    except Exception as exc:
        return datetime.datetime.now()


def get_ntp_time():
    ntp_client = ntplib.NTPClient()
    response = ntp_client.request('cn.ntp.org.cn')
    return datetime.datetime.fromtimestamp(response.tx_time)


def encrypt(content):
    # content length must be a multiple of 16.
    while len(content) % 16:
        content += ' '
    content = content.encode('utf-8')
    # Encrypt content.
    aes = AES.new(b'2019092520190925', AES.MODE_CBC, b'2019092520190925')
    encrypted_content = aes.encrypt(content)
    return(b2a_hex(encrypted_content))

def gen_license_file():
    license_file = './License.dat'
    with open(license_file, 'w') as LF:
        mac = get_mac_address()
        LF.write('MAC : %s\n'%(mac))
        tmp = "Date : "+date+"\n"
        LF.write(tmp)
        tmp = str(mac)+"#"+date
        sign = encrypt(tmp)
        LF.write('Sign : ' + str(sign.decode('utf-8')) + '\n')

def get_mac_address():
    hostname = socket.gethostname()
    mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
                           for ele in range(0, 8 * 6, 8)][::-1])
    return mac_address

def get_mac_address():
    hostname = socket.gethostname()
    mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
                           for ele in range(0, 8 * 6, 8)][::-1])
    return mac_address


def get_network_time():
    c = ntplib.NTPClient()
    response = c.request('pool.ntp.org')
    return ctime(response.tx_time)

def license_check():


    bj_time = get_beijin_time()
    tmp = str(bj_time)
    tmp = tmp.split(' ')
    tmp = tmp[0].split('-')

    current_date1 = str(tmp[0]) + str(tmp[1]) + str(tmp[2])

    ntp_time = get_ntp_time()
    tmp = str(ntp_time)
    tmp = tmp.split(' ')
    tmp = tmp[0].split('-')

    current_date2 = str(tmp[0]) + str(tmp[1]) + str(tmp[2])


    license_dic = parse_license_file()
    sign = decrypt(license_dic['Sign'])
    sign_list = sign.split('#')
    lic_mac = sign_list[0].strip()
    lic_date = sign_list[1].strip()
    # Check license file is modified or not.
    if (lic_mac != license_dic['MAC']) or (lic_date != license_dic['Date']):
        log.error('*Error*: License file is modified!')
        log.error('lic_mac：%s,license_dic[MAC]：%s',lic_mac,license_dic['MAC'])
        log.error('lic_date：%s,license_dic[Date]：%s',lic_date,license_dic['Date'])
        exit(0)
    # Check MAC and effective date invalid or not.
    if len(sign_list) == 2:
        mac = get_mac_address()
        # current_date = datetime.datetime.now().strftime('%Y%m%d')
        # print(current_date)
        # Must run this script under specified MAC.
        if lic_mac != mac:
            log.error('*Error*: Invalid host!')
            log.error('lic_mac：%s,mac：%s', lic_mac, mac)

            exit(0)
        # Current time must be before effective date.
        log.info("北京时间：%s",current_date1)
        log.info("ntp时间：%s",current_date2)
        try:
            if lic_date < current_date1 or lic_date < current_date2:
                log.error('*Error*: License is expired! lic_date:%d ',lic_date)
                exit(0)
            else:
                log.info("*OK* Licsence valid")
        except:
            log.error("data err")

    else:
        log.error('*Error*: Wrong Sign setting on license file.')
        exit(0)

def parse_license_file():
    license_dic = {}
    license_file = './License.dat'
    with open(license_file, 'r') as LF:
        for line in LF.readlines():
            if re.match('^\s*(\S+)\s*:\s*(\S+)\s*$', line):
                my_match = re.match('^\s*(\S+)\s*:\s*(\S+)\s*$', line)
                license_dic[my_match.group(1)] = my_match.group(2)
    return(license_dic)

def decrypt(content):
    aes = AES.new(b'2019092520190925', AES.MODE_CBC, b'2019092520190925')
    decrypted_content = aes.decrypt(a2b_hex(content.encode('utf-8')))
    return(decrypted_content.decode('utf-8'))

