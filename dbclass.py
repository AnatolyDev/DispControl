import pymysql.cursors

class MySQLConn(object):
    __instance__ = None
    __conn = None

    __host='172.15.0.225'
    __user='myuser'
    __password='promyadm'
    __db='test'
    __charset='utf8mb4'

    def __init__(self):
        print('Создание класса')

    @staticmethod
    def getInstance():
        if MySQLConn.__instance__ is None:
            MySQLConn.__instance__ = MySQLConn()
        
        return MySQLConn.__instance__

    def setConnParams(self,host,user,password,db,charset):
        self.__host     = host
        self.__user     = user
        self.__password = password
        self.__db       = db
        self.__charset  = charset

    def setConnect(self):
        try:
            self.__conn = pymysql.connect(host=self.__host,
                                          user=self.__user,
                                          password=self.__password,                             
                                          db=self.__db,
                                          charset=self.__charset,
                                          cursorclass=pymysql.cursors.DictCursor)
            print('Соединение установлено')
        except:
            self.__conn = None
            print('Соединение установить не удаётся')

    def disconnect(self):
        self.__conn.close()
        print('Соединение закрыто')

    def setCurrentValue(self,id,dat,val):
        try:
            with self.__conn.cursor() as cursor:
                # проверим, есть ли запись в базе
                sql = 'SELECT * FROM ustr_now_test WHERE id = %s'%(id)
                rows_count = cursor.execute(sql)
                
                if rows_count > 0:
                    # запись есть
                    x = self.__conn.cursor()
                    sql = "UPDATE ustr_now_test SET date_in = '%s', znach = %s WHERE id = %s"%(dat,val,id)
                    x.execute(sql)
                    print('Обновление значения')
                else:
                    # записи нет
                    sql = "INSERT INTO ustr_now_test VALUES(%s,'%s',%s)"%(id,dat,val)
                    x = self.__conn.cursor()
                    x.execute(sql)
                    print('Добавление значения')
                self.__conn.commit()
        except:
            print('Ошибка при добавлении/обновлении записи')
            self.disconnect()