import requests
import config
import telebot
import datetime as datetime
from bs4 import BeautifulSoup
from datetime import datetime
from typing import Optional, Tuple


bot = telebot.TeleBot(config.BOT_CONFIG['access_token'])


@bot.message_handler(commands=['start'])
def echo(message):
    bot.send_message(message.chat.id, "Примеры команд:")
    bot.send_message(message.chat.id, "Получить расписание на указанный день:")
    bot.send_message(message.chat.id, "/monday K3142 1")
    bot.send_message(message.chat.id, "/tuesday K3142 1")
    bot.send_message(message.chat.id, "/wednesday K3142 1")
    bot.send_message(message.chat.id, "/thursday K3142 1")
    bot.send_message(message.chat.id, "/friday K3142 1")
    bot.send_message(message.chat.id, "/saturday K3142 1")
    bot.send_message(message.chat.id, "/sunday K3142 1")
    bot.send_message(message.chat.id, "Получить расписание на следующий день:")
    bot.send_message(message.chat.id, "/tomorrow K3142")
    bot.send_message(message.chat.id, "Получить ближайшее занятие:")
    bot.send_message(message.chat.id,  "/near K3142")
    bot.send_message(message.chat.id, "Получить расписание на всю неделю:")
    bot.send_message(message.chat.id, "/all K3142")


def get_page(group: str, week: str = '') -> str:
    if week:
        week = str(week) + '/'
    url = '{domain}/{group}/{week}raspisanie_zanyatiy_{group}.htm'.format(
        domain=config.BOT_CONFIG['domain'],
        week=week,
        group=group)
    print(url)
    response = requests.get(url)
    web_page = response.text
    return web_page


def parse_schedule_for_a_day(web_page: str, day_num: str) -> Optional[tuple]:

    soup = BeautifulSoup(web_page, "html5lib")

    # Получаем таблицу с расписанием
    schedule_table = soup.find("table", attrs={"id": day_num + "day"})

    # Время проведения занятий
    times_list = schedule_table.find_all("td", attrs={"class": "time"})
    times_list = [time.span.text for time in times_list]

    # Место проведения занятий
    locations_list = schedule_table.find_all("td", attrs={"class": "room"})
    locations_list = [room.span.text for room in locations_list]

    # Название дисциплин и имена преподавателей
    lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})

    lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
    lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]

    return times_list, locations_list, lessons_list


def get_week_num(week: int) -> str:
    if week % 2 != 0:
        week = "2"
    else:
        week = "1"

    return week


@bot.message_handler(commands=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])
def get_schedule(message):
    """ Получить расписание на указанный день """
    try:
        day_num = ""
        info = message.text.split()

        if len(info) == 3:
            day, group, week = info
            web_page = get_page(group, str(week))
        else:
            day, group = info
            week = "0"

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

        if week == "0":
            web_page = get_page(group, "1")
            times_lst, locations_lst, lessons_lst = parse_schedule_for_a_day(web_page, str(day_num))
            resp1 = '<b>Четная неделя:</b> \n\n'
            for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
                resp1 += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
            bot.send_message(message.chat.id, resp1, parse_mode='HTML')

            web_page = get_page(group, "2")
            times_lst, locations_lst, lessons_lst = parse_schedule_for_a_day(web_page, str(day_num))
            resp2 = '<b>Нечетная неделя:</b> \n\n'
            for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
                resp2 += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
            if resp1 != resp2:
                bot.send_message(message.chat.id, resp2, parse_mode='HTML')

        else:
            times_lst, locations_lst, lessons_lst = parse_schedule_for_a_day(web_page, str(day_num))
            resp = ''
            for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
                resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
            bot.send_message(message.chat.id, resp, parse_mode='HTML')
    except AttributeError:
        bot.send_message(message.chat.id, 'Занятий нет')
    except ValueError:
        bot.send_message(message.chat.id, 'Неверные данные. Повторите запрос.')


@bot.message_handler(commands=['near'])
def get_near_lesson(message):
    """ Получить ближайшее занятие """
    try:
        _, group = message.text.split()
        dt = datetime.today().date()
        dttuple = datetime.isocalendar(dt)

        week_num = dttuple[1]
        week = get_week_num(week_num)

        day = dttuple[2]

        current_time = datetime.today().time()
        c_time = str(current_time).split(":")
        c_hour = int(c_time[0])
        c_minute = int(c_time[1])

        web_page = get_page(group, week)
        times_lst, locations_lst, lessons_lst = parse_schedule_for_a_day(web_page, str(day))
        resp = '<b>Ближайшее занятие:</b> \n\n'
        for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
            class_time = str(time).split("-")
            cl_time = str(class_time[0]).split(":")
            hour = int(cl_time[0])
            minute = int(cl_time[1])
            if (hour == c_hour and minute > c_minute) or (hour > c_hour):
                resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
                break

        if resp == '<b>Ближайшее занятие:</b> \n\n':
            day += 1
            if day == 7 or day == 8:
                day = 1
                if week == "1":
                    week = "2"
                else:
                    week = "1"
            web_page = get_page(group, week)
            times_lst, locations_lst, lessons_lst = parse_schedule_for_a_day(web_page, str(day))
            for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
                resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
                break

        bot.send_message(message.chat.id, resp, parse_mode='HTML')
    except AttributeError:
        bot.send_message(message.chat.id, 'У вас нет занятий в ближайшее время.')
    except ValueError:
        bot.send_message(message.chat.id, 'Неверные данные. Повторите запрос.')


@bot.message_handler(commands=['tomorrow'])
def get_tommorow(message):
    """ Получить расписание на следующий день """
    try:
        _, group = message.text.split()
        dt = datetime.today().date()
        dttuple = datetime.isocalendar(dt)

        week_num = dttuple[1]
        week = get_week_num(week_num)

        next_day = dttuple[2] + 1
        if next_day == 8:
            next_day = 1

        web_page = get_page(group, week)
        times_lst, locations_lst, lessons_lst = parse_schedule_for_a_day(web_page, str(next_day))
        resp = '<b>Расписание на завтра:</b> \n\n'
        for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
            resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
        bot.send_message(message.chat.id, resp, parse_mode='HTML')
    except AttributeError:
        bot.send_message(message.chat.id, 'Занятий нет')
    except ValueError:
        bot.send_message(message.chat.id, 'Неверные данные. Повторите запрос.')


@bot.message_handler(commands=['all'])
def get_all_schedule(message):
    """ Получить расписание на всю неделю для указанной группы """
    try:
        _, group = message.text.split()
        dt = datetime.today().date()
        dttuple = datetime.isocalendar(dt)

        week_num = dttuple[1]
        week = get_week_num(week_num)
        web_page = get_page(group, week)

        days = (1, 2, 3, 4, 5, 6, 7)
        weekdays = ("Понедельник:", "Вторник:", "Среда:", "Четверг:", "Пятница:", "Суббота:", "Воскресенье:")

        for day in days:
            times_lst, locations_lst, lessons_lst = parse_schedule_for_a_day(web_page, str(day))
            resp = '<b>{}</b> \n\n'.format(weekdays[day - 1])
            for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
                resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
            bot.send_message(message.chat.id, resp, parse_mode='HTML')
    except AttributeError:
        bot.send_message(message.chat.id, 'Занятий нет')
    except ValueError:
        bot.send_message(message.chat.id, 'Неверные данные. Повторите запрос.')


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
