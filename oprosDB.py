import pymysql.cursors  
 
# Подключиться к базе данных на просервере
connProserver = pymysql.connect(host='172.15.0.225',
                                user='myuser',
                                password='promyadm',                             
                                db='DispAll_CBK',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)
 
print ("connect to proserver successful!!")

# Подключиться к базе данных на просервере
connTurb = pymysql.connect(host='172.15.202.20',
                           user='asu',
                           password='12341234',                             
                           db='tec_cbk',
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)

print ("Connect to turb successful!!")
try:
  
 
    with connProserver.cursor() as cursor:
       
        # SQL - самые поздние имеющиеся записи
        sql = "SELECT * FROM ustr_accumulated WHERE (id, Date_In) IN (SELECT id, MAX(Date_In) FROM ustr_accumulated GROUP BY id)"
         
        # Выполнить команду запроса (Execute Query).
        cursor.execute(sql)
        
        #print ("cursor.description: ", cursor.description)
 
        #print()
        
        for row in cursor:
            print(row)
            #print(row["Id"]," : ", row['Date_In']," : ",row["Znach"])
            #print("SELECT * FROM ustr_accumulated WHERE (id = " + str(row["Id"]) + ") and (Date_In > '" + str(row['Date_In']) + "')")
            
            with connTurb.cursor() as cursorTurb:
                # вытащим все недостающие данные на удалённой машине
                str_now = row["Date_In"].date().isoformat()
                sql = "SELECT * FROM ustr_accumulated WHERE (id = " + str(row["Id"]) + ") and (Date_In > '" + str(row['Date_In']) + "')"
                cursorTurb.execute(sql)
                try:
                    x = connProserver.cursor()
                    for r in cursorTurb:
                        x.execute("INSERT INTO ustr_accumulated VALUES (%s,%s,%s)",(r["Id"],r["Date_In"],r["Znach"]))
                    connProserver.commit()
                    print("Параметр " + row["Id"] + " загружен")
                except:
                    connProserver.rollback()
                            
finally:
    # Закрыть соединение (Close connection).
    connTurb.close()
    print("Соединение с турбинным закрыто")
    connProserver.close()
    print("Соединение с сервером закрыто")