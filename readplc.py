"""
Snap7 client used for connection to a siemens7 server.
"""
import time # функции времени
import re   # регулярные выражения
from ctypes import c_int, c_char_p, byref, sizeof, c_uint16, c_int32, c_byte
from ctypes import c_void_p

import logging # логирование


import snap7 # основная библиотека для связи с контроллером
from snap7 import six
from snap7.snap7types import S7Object, buffer_type, buffer_size, BlocksList
from snap7.snap7types import TS7BlockInfo, param_types, cpu_statuses

from snap7.common import check_error, load_library, ipv4
from snap7.snap7exceptions import Snap7Exception

import pymysql.cursors


logger = logging.getLogger(__name__)

cl = snap7.client.Client()
print('Подключаемся')
cl.connect('172.15.202.150',0,2)
print('Подключено')

#Get CPU INFO
x=cl.get_cpu_info()
print (x.ModuleTypeName)
print ("""CPU Information:
%s
Serial Number:
%s
AS Name:
%s
Copy Right:
%s
Module Name:
%s
"""
%(x.ModuleTypeName.decode("utf-8"),
x.SerialNumber.decode("utf-8"),
x.ASName.decode("utf-8"),
x.Copyright.decode("utf-8"),
x.ModuleName.decode("utf-8")
)
)

# читаем данные
for num in range(10):
    print('Читаем мощность')
    reading = cl.db_read(8, 2, 4)
    r = snap7.util.get_real(reading,0)
    print("W=%4.1f"%(r))
    time.sleep(1)

print('Отключаемся')
cl.disconnect()
