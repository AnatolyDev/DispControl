from datetime import datetime
import dbclass

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


# создаём соединение с базой
a = dbclass.MySQLConn.getInstance()
a.setConnect()


cl = snap7.client.Client()
print('Подключаемся к контроллеру 172.15.202.150')
cl.connect('172.15.202.150',0,2)
print('Подключено к контроллеру')

# читаем данные
for num in range(20):
    # текущая дата
    d = datetime.now()
    d_str = datetime.strftime(d, "%Y.%m.%d %H:%M:%S")

    print('Читаем значение с контроллера')
    reading = cl.db_read(16, 6, 4)     # расход в машинный бассейн
    r = snap7.util.get_real(reading,0) # читаем параметр с контроллера
    r = float("{0:.1f}".format(r))     # урезаем формат до двух знаков после запятой
    a.setCurrentValue(12,d_str,r)      # пишем в базу
    #print("W=%4.1f"%(r))

    time.sleep(2)

print('Отключаемся от контроллера')
cl.disconnect()

a.disconnect()