# 1. процесс загрузки в photos.saveMessagesPhoto не нашел как на прямую загружать фото по ссылке
# не сохраняя на ПК


import io
import json
from data.tokens import token, token2
from vk_api import VkApi
from random import randrange
from urllib.request import urlopen

import numpy
import vk_api

from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.upload import FilesOpener
from vk_api.vk_api import VkApiMethod
import urllib
import re
import requests

import data.creation_db, data.fullfill_db



def city_encoder(city):
    return vk_user.method('database.getCities', {'country_id': 1,
                                                 'q': city,
                                                 'need_all': 0,
                                                 'count': 10000,
                                                 })


def city_decoder(city_id):
    return vk_user.method('database.getCitiesById', {'city_ids': city_id})[0]['title']


def sex_decoder(sex_id):
    if sex_id == 1 or sex_id == '1':
        return 'Женский'
    elif sex_id == 2 or sex_id == '2':
        return 'Мужской'
    else:
        return 'не указан'


def write_msg(user_id, message, attach=None):
    return vk_bot.method('messages.send',  {'user_id': user_id,
                                            'message': message,
                                            'attachment': attach,
                                            'random_id': randrange(10 ** 7)})


def user_get_by_id(id1):
    return vk_user.method('users.get', {'user_ids': id1,
                                        'fields': 'first_name, last_name'})


def bot_photo_attach(photo_url):
    file = requests.get(photo_url).content
    #print(requests.get(photo_url))
    data = vk_bot.method('photos.getMessagesUploadServer', {'peer_id': 0})
    upload_url = data['upload_url']

    with open('dump/1.jpg', 'wb') as f:
        f.write(file)
    upfile = {'photo': open('dump/1.jpg', 'rb')}

    r = requests.post(upload_url, files=upfile)
    r2 = vk_bot.method('photos.saveMessagesPhoto', {'photo': r.json()['photo'],
                                                    'server': r.json()['server'],
                                                    'hash': r.json()['hash']})
    return f'photo{r2[0]["owner_id"]}_{r2[0]["id"]}'




class SearchRequest:
    """ Класс созданный для передачи пошаговых параметров поиска """

    c_search = 1
    c_step = 0
    c_age_from = 0
    c_age_to = 0
    c_sex = 0
    c_city = 0
    c_status = 1
    c_send = 0
    c_more = 'еще'
    temp_list = []
    dump_list = []
    favor_dump_list = []
    user_collection = []

    def __init__(self, user_id):
        self.user_id = user_id

    def number_in_request_handler(self, user_input):
        # поиск чисел в запросе пользователя (для преобразования в действия на определенных шагах)
        if len(re.findall(r'\d+', user_input)):
            return int(re.findall(r'\d+', user_input)[0])
        else:
            return user_input

    def main_search(self, user_input):
        """основной метод для поиска по параметрам"""

        if self.c_step == 1:
            """первый шаг - возраст от """
            self.c_age_from = user_input
        elif self.c_step == 2:
            """второй шаг - возраст до """
            self.c_age_to = user_input
        elif self.c_step == 3:
            """третий шаг (опционально) - пол """
            if isinstance(self.number_in_request_handler(user_input), int):
                self.c_sex = user_input
            else:
                if user_input.lower() == "ж" or user_input.lower() == "жен" or user_input.lower() == "женский":
                    self.c_sex = 1
                elif user_input.lower() == "м" or user_input.lower() == "муж" or user_input.lower() == "мужской":
                    self.c_sex = 2
                else:
                    self.c_sex = 0

        elif self.c_step == 4:
            """четвертый шаг (опционально) - Город """
            if not isinstance(self.number_in_request_handler(user_input), int):
                print('city = not int')
                self.c_city = city_encoder(user_input.lower())['items'][0]['id']
            else:
                print('city = int')
                self.c_city = user_input

    def base_request(self, user_input):
        """ базовая функция обработки запросов пользователя """

        if user_input.lower() == "привет":

            return write_msg(self.user_id, f"Привет, {user_get_by_id(self.user_id)[0]['first_name']}!")
        elif user_input.lower() == "пока":
            return write_msg(self.user_id, "Пока((")
        elif user_input.lower() == "поиск" or user_input.lower() == "gjbcr":
            write_msg(self.user_id, 'Возраст от: ')
            self.c_step = 1
        elif user_input.lower() in ['favor', 'избранное', 'fav', 'изб']:
            print('hohooh')
            self.show_collection(self.user_collection)

        elif user_input.lower() == "gjbcr":
            #request_reset()
            write_msg(self.user_id, 'Не забудьте переключить раскладку клавиатуры!')
            write_msg(self.user_id, 'Возраст от: ')

        # потом подумаю над оптимизацией
        elif self.c_step == 1:
            self.main_search(user_input)
            write_msg(self.user_id, 'Возраст до: ')
            self.c_step = 2
        elif self.c_step == 2:
            self.main_search(user_input)
            write_msg(self.user_id, 'Пол: ')
            self.c_step = 3

        elif self.c_step == 3:
            self.main_search(user_input)
            write_msg(self.user_id, 'Укажите город, в котором осуществить поиск: ')
            self.c_step = 4
        elif self.c_step == 4:
            self.main_search(user_input)
            self.c_step = 5

            summury_request_result = {'age_from': self.c_age_from,
                                      'age_to': self.c_age_to,
                                      'sex': sex_decoder(self.c_sex),
                                      'city': city_decoder(self.c_city)}

            #print(summury_request_result)
            write_msg(self.user_id, f'Вы ищите людей: \n'
                                    f'возраст от: {self.c_age_from}, \n'
                                    f'возраст до: {self.c_age_to}, \n'
                                    f'пол: {sex_decoder(self.c_sex)}, \n'
                                    f'город: {city_decoder(self.c_city)}')
            self.temp_list = [result for result in self.search_user()['items']]
            print(self.search_user()['items'][0])
            for element in self.temp_list:
                if not element in self.dump_list:
                    if self.c_send == 2:
                        self.c_send = 0
                        write_msg(self.user_id, 'Вывести еще парочку?\n'
                                                'Напиши "еще" или "1" или "да"')
                        break
                    self.dump_list.append(element)
                    #print(self.dump_list)
                    self.favor_dump_list.append(element)
                    self.send_search_result(element)

        elif self.c_step == 5:
            if str(user_input).lower() in 'save':
                self.save_collection(user_input, self.favor_dump_list)
                write_msg(self.user_id, 'Вывести еще парочку?\n'
                                        'Напиши "еще" или "1" или "да"')

            elif user_input.lower() in ['еще', '1', 'да', 'tot', 'lf']:

                self.c_more = None
                #print(composite_request)
                self.favor_dump_list = []

                for element in self.temp_list:
                    if not element in self.dump_list:
                        if self.c_send == 2:
                            self.c_send = 0

                            write_msg(self.user_id, 'Вывести еще парочку?\n'
                                                    'Напиши "еще" или "1" или "да"')
                            break
                        self.dump_list.append(element)
                        #print(self.dump_list)
                        self.favor_dump_list.append(element)
                        self.send_search_result(element)


        else:
            return write_msg(self.user_id, "Не поняла вашего ответа...")

    def search_user(self):
        print(self.c_city)
        print(city_decoder(self.c_city))
        #почему то сломался user.search по параметру "city". не ищет город который указывают. в интернете - не нашел.
        return vk_user.method('users.search', {'age_from': self.c_age_from,
                                               'age_to': self.c_age_to,
                                               'city': self.c_city,
                                               'sex': self.c_sex,

                                               #'hometown': city_decoder(self.c_city),
                                               'status': self.c_status,
                                               'sort': 0,
                                               'has_photo': 1,
                                               'count': 1000,
                                               'can_access_closed': True,
                                               'is_closed': False,
                                               #'v': '5.130',
                                               'fields': 'city, domain, about, photo_max_orig'})

    def save_collection(self, command, favorite_list):
        if str(command).lower() == 'save':
            for l in favorite_list:
                print(type(data.fullfill_db.db_get(event.user_id)[0][2]))
                if not l['id'] in data.fullfill_db.db_get(event.user_id)[0][2]:
                    self.user_collection.append(l)
                # print(favorite_list[-i])
            write_msg(self.user_id, 'Результаты поиска добавлены в Избранное!')
            json_favorite = json.dumps(self.user_collection)
            # print(json_favorite)
            data.fullfill_db.db_fill(self.user_id, json_favorite)
            return json_favorite

    def show_collection(self, collection_list):
        for element in collection_list:
            self.send_search_result(element)

    def send_search_result(self, user_get):
        # выводит фотографию в сообщение от бота пользователю

        if not user_get['is_closed'] and 'city' in str(user_get):
            first_name = user_get['first_name']
            last_name = user_get['last_name']
            city = user_get['city']['title']

            mess = f"{last_name} {first_name}, {city}, https://vk.com/{user_get['domain']}"
            write_msg(self.user_id, mess, bot_photo_attach(user_get['photo_max_orig']))
            self.c_send += 1


if __name__ == '__main__':
    bot_used_users = []

    # token = input('Token: ')
    vk_bot = vk_api.VkApi(token=token)
    vk_user = vk_api.VkApi(token=token2)

    vk_method = vk_user.get_api()

    longpoll = VkLongPoll(vk_bot)
    print('ok')

    data.creation_db.db_create()

    for event in longpoll.listen():

        if event.type == VkEventType.USER_TYPING and not event.user_id in bot_used_users:
            vars()[str(event.user_id) + "UserSearch"] = SearchRequest(event.user_id)

            if data.fullfill_db.db_get(event.user_id):
                bot_used_users.append(data.fullfill_db.db_get(event.user_id)[0][1])
                #print('297087910' in data.fullfill_db.db_get(event.user_id)[0][2])
                write_msg(event.user_id, f'И снова Привет, {user_get_by_id(event.user_id)[0]["first_name"]}! \n'
                                         f'Не забыл, что доступны следующие команды:\n'
                                         f'"Привет", "Поиск", "Пока"')
            else:
                #vars()[str(event.user_id) + "UserSearch"] = SearchRequest(event.user_id)
                bot_used_users.append(event.user_id)
                print(bot_used_users)
                write_msg(event.user_id, f'Привет, {user_get_by_id(event.user_id)[0]["first_name"]}! \n'
                                         f'Я помогу тебе найти пользователей в VK с фото! \n'
                                         f'В настоящее время доступны следующие команды:\n'
                                         f'"Привет", "Поиск", "Пока"')
        if event.type == VkEventType.MESSAGE_NEW:

            if event.to_me:
                request = event.text
                if not event.user_id in bot_used_users:
                    vars()[str(event.user_id) + "UserSearch"] = SearchRequest(event.user_id)
                    bot_used_users.append(event.user_id)
                vars()[str(event.user_id) + "UserSearch"].base_request(request)
