import vk_api
import pymysql
import os
import random
import threading
import dateparser
import re
import Login_info as LI
from mysql.connector import connect, Error
#from timefhuman import timefhuman
from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType


load_dotenv()
print("привет")
vk = vk_api.VkApi(token=LI.token)
longpoll = VkLongPoll(vk)

host = os.getenv('host')
port = os.getenv('port')
user = os.getenv('user')
password = os.getenv('password')
database = os.getenv('database')
charset = os.getenv('charset')

#connection = pymysql.connect(host=host, user=user, password=password, db=database, charset=charset, cursorclass=pymysql.cursors.DictCursor)
#database connection
with connect(
    host="localhost",
    user="root",
    password="root",
    database="vkbotpr",
) as connection:
    print("с базой есть соединения")

# Таймер для выполнения
#
# def (i):
#     threading.Timer(2.0, printit, [i+1]).start()
#     vk.method('messages.send', {'user_id': 4591935, 'message': 'Привет ' + str(i),
#                                 'random_id': random.randint(0, 1000)})
#     print("Hello ", i)
#
# printit(1)

# Основной цикл программы
for event in longpoll.listen():
    print(event.type)
    # Если пришло новое сообщение
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            user = vk.method("users.get", {"user_ids": event.user_id,
                                           "fields": "photo_id, verified, sex, bdate, city, country, home_town, "
                                                     "has_photo, photo_50, photo_100, photo_200_orig, photo_200, "
                                                     "photo_400_orig, photo_max, photo_max_orig, online, domain, "
                                                     "has_mobile, contacts, site, education, universities, schools, "
                                                     "status, last_seen, followers_count, occupation, nickname, "
                                                     "relatives, relation, personal, connections, exports, activities, "
                                                     "interests, music, movies, tv, books, games, about, quotes, "
                                                     "can_post, can_see_all_posts, can_see_audio, "
                                                     "can_write_private_message, can_send_friend_request, "
                                                     "is_favorite, is_hidden_from_feed, timezone, screen_name, "
                                                     "maiden_name, crop_photo, is_friend, friend_status, career, "
                                                     "military, blacklisted, blacklisted_by_me, "
                                                     "can_be_invited_group"})[0]
            print(user["first_name"])

            try:
               with connect (
                       host="localhost",
                       user="root",
                       password="root",
                       database="vkbotpr",
               ) as connection:
                    print("\n Успешное соединение")
                    n = 0
                    query= "SELECT * FROM users WHERE user_id =" + str(event.user_id)
                    print("Запрос №1: " + query)
                    with connection.cursor() as cursor:
                        cursor.execute (query)
                        result = cursor.fetchall()
                        n = len(result)
                    if n == 0:
                        query = "INSERT INTO users (fist_name, last_name, user_id, login) VALUES (%s, %s, %s, %s)"
                        print("Запрос №2: " + query)
                        with connection.cursor(buffered=True) as cursor:
                            cursor.execute (query, (user["first_name"], user["last_name"], user["id"], user['screen_name']))
            except Error as e:
                print("Ошибка соединения №1: " + str(e))
            #a = input("dffdsfsdg")






           # # cur = connection.cursor()
           #  # Выбираем из таблицы users пользователя, отправивишего сообщение
           #  print(event.user_id)
           #  cur.execute("SELECT * FROM users WHERE user_id =" + str(event.user_id))
           #  input("нннн")
           #  # Получаем количество выбранных строк (0 или 1)
           #  n = cur.rowcount
           #  cur.close()
           #  # Если пользователя нет в таблице
           #  if n == 0:
           #      cur = connection.cursor()
           #      # Добавляем пользователя в таблицу
           #      cur.execute("INSERT INTO users (first_name, last_name, user_id, login) VALUES (%s, %s, %s, %s)",
           #                  (user["first_name"], user["last_name"], user["id"], user['screen_name']))
           #      connection.commit()
           #      cur.close()
            # Получение id пользователя - добавленного или имеющегося
            rows = []
            try:
                with connect(
                    host="localhost",
                    user="root",
                    password="root",
                    database="vkbotpr",
                ) as connection:
                    query = "SELECT * FROM users WHERE users.user_id=" + str(user["id"])
                    print("Запрос №3: " + query)
                    with connection.cursor(buffered=True) as cursor:
                        cursor.execute(query)
                        #cur = connection.cursor()
                        #cur.execute()
                        rows = cursor.fetchall()
            except Error as e:
                print("Ошибка соединения №2: " + str(e))

            for row in rows:
                id_user = row['user_id']
                print(row['user_id'])
            vk.method('messages.send', {'peer_id': event.user_id, 'message': 'Приветствую Вас, ' + user["first_name"] + '! Я бот!',
                                        'random_id': random.randint(0, 1000)})
            # Текст сообщения пользователя
            request = str(event.text)
            # Массив элементов команды
            params = re.split(";|,",request)
            try:
                with connect(
                    host="localhost",
                    user="root",
                    password="root",
                    database="vkbotpr",
                ) as connection:
                    with connection.cursor(buffered=True) as cursor:
                        if params[0] in ['','statements', 'add', 'добавить']:
                            #cur = connection.cursor()
                            # Добавляем заявление в таблицу
                            query = "INSERT INTO statements (name, deadline, statements, user_id) VALUES (%s, %s, %s, %s)"
                            print("Запрос №4.1: "+ query)
                            cursor.execute(query,
                                        (params[1], params[2], params[3].strip(' '), user["id"]))
                            #connection.commit()
                            #cur.close()
                        else:
                        #    cur = connection.cursor()
                            query = "SELECT * FROM users, statements WHERE statements.user_id = " + str(user["id"]) + " and users.user_id = " + str(user["id"])
                            print("Запрос №4.2: "+ query)
                            cursor.execute(query)
                            rows = cursor.fetchall()
                            print("Результат запроса №4.2: " + str(rows))
                            msg = 'Что-то пошло не так...'
                            for row in rows:
                                print(row)
                                msg = msg + str(row['statements.id']) + ' ' + row['name'] + ' ' + str(row['deadline']) + '\n'
                            vk.method('messages.send',
                                      {'peer_id': event.user_id, 'message': msg, 'random_id': random.randint(0, 1000)})
            except Error as e:
                print("Ошибка соединения №3: " + str(e))



#for event in longpoll.listen():
#    if event.type == VkEventType.MESSAGE_NEW:
 #     if event.to_me:
            # Сообщение от пользователя
  #          request = event.text
          #  user = vk.method("users.get", {"user_id":event.user_id, "fields": "photo_id, verified, sex, bdate, city, country, home_town, has_photo, photo_50, photo_100, photo_200_orig, photo_200, photo_400_orig, photo_max, photo_max_orig, online, domain, has_mobile, contacts, site, education, universities, schools, status, last_seen, followers_count, occupation, nickname, relatives, relation, personal, connections, exports, activities, interests, music, movies, tv, books, games, about, quotes, can_post, can_see_all_posts, can_see_audio, can_write_private_message, can_send_friend_request, is_favorite, is_hidden_from_feed, timezone, screen_name, maiden_name, crop_photo, is_friend, friend_status, career, military, blacklisted, blacklisted_by_me, can_be_invited_group"})[0]
           # print("Пришло сообщение от пользователя"+ user["first_name"] + user["last_name"])
          #  send_msg(vk, event.user_id, "Здравствуйте,"+ user["first_name"] + user["last_name"])
            #send_msg(vk, event.user_id, "Здравствуйте," + user["first_name"] + user["last_name"])
