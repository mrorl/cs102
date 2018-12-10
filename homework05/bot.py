import requests
import config
import telebot
import datetime
from bs4 import BeautifulSoup
from datetime import datetime


bot = telebot.TeleBot(config.BOT_CONFIG['access_token'])


def get_page(group, week=''):
    if week:
        week = str(week) + '/'
    url = '{domain}/{group}/{week}raspisanie_zanyatiy_{group}.htm'.format(
        domain=config.BOT_CONFIG['domain'],
        week=week,
        group=group)
    response = requests.get(url)
    web_page = response.text
    return web_page


def parse_schedule_for_a_day(web_page, day_num: str):

    soup = BeautifulSoup(web_page, "html5lib")

    # Получаем таблицу с расписанием
    schedule_table = soup.find("table", attrs={"id": "{}day".format(day_num)})

    times_list = schedule_table.find_all("td", attrs={"class": "time"})  # Время проведения занятий
    times_list = [time.span.text for time in times_list]

    locations_list = schedule_table.find_all("td", attrs={"class": "room"})  # Место проведения занятий
    locations_list = [room.span.text for room in locations_list]

    lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})  # Название дисциплин и имена преподавателей

    lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
    lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]

    return times_list, locations_list, lessons_list



@bot.message_handler(commands=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])
def get_schedule(message):
    """ Получить расписание на указанный день """

    day_num = ""

    info = message.text.split()
    if len(info) == 3:
        day, group, week = info
        web_page = get_page(group, week)
    else:
        day, group = info
    web_page = get_page(group)
    if day == "/monday":
        day_num = "1"
    elif day == "/tuesday":
        day_num = "2"
    elif day == "/wednesday":
        day_num = "3"
    elif day == "/thursday":
        day_num = "4"
    elif day == "/friday":
        day_num = "5"
    elif day == "/saturday":
        day_num = "6"
    elif day == "/sunday":
        day_num = "7"

    times_lst, locations_lst, lessons_lst = \
        parse_schedule_for_a_day(web_page, day_num)
    resp = ''
    for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
        resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
    bot.send_message(message.chat.id, resp, parse_mode='HTML')




@bot.message_handler(commands=['near'])  #разработка
def get_near_lesson(message):
    """ Получить ближайшее занятие """
    _, group = message.text.split()
    dt = datetime.today().date()
    dtuple = datetime.isocalendar(dt)
    week = dtuple[1]
    if week % 2 != 0:
        week = "2"
    else:
        week = "1"
    web_page = get_page(group, week)

    day_num = datetime.datetime.today().isoweekday()

    times_lst, locations_lst, lessons_lst = \
        parse_schedule_for_a_day(web_page, str(day_num))
    resp = ''
    for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
        resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['tommorow'])
def get_tommorow(message):
    """ Получить расписание на следующий день """
    _, group = message.text.split()
    dt = datetime.today().date()
    dtuple = datetime.isocalendar(dt)
    week = dtuple[1]
    if week % 2 != 0:
        week = "2"
    else:
        week = "1"
    web_page = get_page(group, week)

    weekday = datetime.datetime.today().isoweekday()
    day_num = 1 + weekday
    
    if day_num == 8:
        day_num = 1

    times_lst, locations_lst, lessons_lst = \
        parse_schedule_for_a_day(web_page, str(day_num))
    resp = ''
    for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
        resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
    bot.send_message(message.chat.id, resp, parse_mode='HTML')



@bot.message_handler(commands=['all'])
def get_all_schedule(message):
    """ Получить расписание на всю неделю для указанной группы """
    _, group = message.text.split()
    dt = datetime.today().date()
    dtuple = datetime.isocalendar(dt)
    week = dtuple[1]
    if week % 2 != 0:
        week = "2"
    else:
        week = "1"
    web_page = get_page(group, week)
    for day in range(6):
        times_lst, locations_lst, lessons_lst = \
            parse_schedule_for_a_day(web_page, str(day))
        resp = ''
        for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
            resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
        bot.send_message(message.chat.id, resp, parse_mode='HTML')


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)

