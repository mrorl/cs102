import psycopg2
import psycopg2.extras
from pprint import pprint as pp
from tabulate import tabulate


conn = psycopg2.connect("host=127.0.0.1 port=5432 dbname=adult_data user=postgres password=z12x34c43v21")
cursor = conn.cursor() # cursor_factory=psycopg2.extras.DictCursor)

def fetch_all(cursor):
    colnames = [desc[0] for desc in cursor.description]
    records = cursor.fetchall()
    return [{colname:value for colname, value in zip(colnames, record)} for record in records]


cursor.execute("SELECT * FROM adult_data LIMIT 5")  #Посмотрим на первые 5 строк
records = cursor.fetchall()
print(records)


'''1. Сколько мужчин и женщин (признак sex) представлено в этом наборе данных?'''
print('1. Сколько мужчин и женщин (признак sex) представлено в этом наборе данных?')
cursor.execute(
    """
    SELECT sex, COUNT(*)
        FROM adult_data
        GROUP BY sex
    """
)
print(tabulate(fetch_all(cursor), "keys", "psql"))


'''2. Каков средний возраст (признак age) женщин?'''
print('2. Каков средний возраст (признак age) женщин?')
cursor.execute("""
    SELECT AVG(age) FROM adult_data WHERE sex = 'Female'
""")
print(tabulate(fetch_all(cursor), "keys", "psql"))

'''3. Какова доля граждан Германии (признак native-country)?'''
print('3. Какова доля граждан Германии (признак native-country)?')
cursor.execute(
    """
    SELECT native_country, ROUND((COUNT(*) / (SELECT COUNT(*) FROM adult_data)::numeric), 6)
        FROM adult_data WHERE native_country = 'Germany'
        GROUP BY native_country;
    """
)
print(tabulate(fetch_all(cursor), "keys", "psql"))


'''4-5. Каковы средние значения и среднеквадратичные отклонения возраста тех, 
кто получает более 50K в год (признак salary) и тех, кто получает менее 50K в год?'''
print('4-5. Каковы средние значения и среднеквадратичные отклонения возраста тех, кто получает более 50K в год (признак salary) и тех, кто получает менее 50K в год?')
cursor.execute("""
    SELECT COUNT(*),
           AVG(age), STDDEV(age)
    FROM adult_data
    GROUP BY salary
""")
print(tabulate(fetch_all(cursor), "keys", "psql"))


'''6. Правда ли, что люди, которые получают больше 50k, имеют как минимум высшее образование? 
(признак education – Bachelors, Prof-school, Assoc-acdm, Assoc-voc, Masters или Doctorate)'''
print('6. Правда ли, что люди, которые получают больше 50k, имеют как минимум высшее образование?')
cursor.execute("""
    SELECT education, salary, COUNT(*) FROM adult_data
    GROUP BY education, salary
""")
print(tabulate(fetch_all(cursor), "keys", "psql"))


'''7. Выведите статистику возраста для каждой расы (признак race) и каждого пола. 
Используйте groupby и describe. Найдите таким образом максимальный возраст мужчин расы Amer-Indian-Eskimo.'''
print('7. Выведите статистику возраста для каждой расы (признак race) и каждого пола.')
print('Найдите таким образом максимальный возраст мужчин расы Amer-Indian-Eskimo')
cursor.execute("""
    SELECT COUNT(*),
           AVG(age), STDDEV(age), MIN(age), MAX(age)
    FROM adult_data WHERE sex = 'Female'
    GROUP BY race
""")
print(tabulate(fetch_all(cursor), "keys", "psql"))

cursor.execute("""
    SELECT COUNT(*),
           AVG(age), STDDEV(age), MIN(age), MAX(age)
    FROM adult_data WHERE sex = 'Male'
    GROUP BY race
""")
print(tabulate(fetch_all(cursor), "keys", "psql"))

cursor.execute("""
    SELECT COUNT(*),
           AVG(age), STDDEV(age), MIN(age), MAX(age)
    FROM adult_data WHERE sex = 'Male' AND race = 'Amer-Indian-Eskimo'
    GROUP BY race
""")
print(tabulate(fetch_all(cursor), "keys", "psql"))


'''8. Среди кого больше доля зарабатывающих много (>50K): среди женатых или холостых мужчин (признак marital-status)? 
Женатыми считаем тех, у кого marital-status начинается с Married (Married-civ-spouse, Married-spouse-absent или Married-AF-spouse), остальных считаем холостыми.'''
print('8. Среди кого больше доля зарабатывающих много (>50K): среди женатых или холостых мужчин (признак marital-status)?')
cursor.execute("""
    SELECT marital_status, salary, COUNT(*) FROM adult_data WHERE sex = 'Male' AND salary = '>50K'
    GROUP BY marital_status, salary
""")
print(tabulate(fetch_all(cursor), "keys", "psql"))


'''9. Какое максимальное число часов человек работает в неделю (признак hours-per-week)? 
Сколько людей работают такое количество часов и каков среди них процент зарабатывающих много?'''
print('9. Какое максимальное число часов человек работает в неделю (признак hours-per-week)?')
print('Сколько людей работают такое количество часов и каков среди них процент зарабатывающих много?')
cursor.execute("SELECT MAX(hours_per_week::int) FROM adult_data")
print(tabulate(fetch_all(cursor), "keys", "psql"))

cursor.execute(
    """
    SELECT salary, COUNT(*)
        FROM adult_data WHERE hours_per_week = 99
        GROUP BY salary
    """
)
print(tabulate(fetch_all(cursor), "keys", "psql"))

cursor.execute("""
    SELECT hours_per_week, salary, COUNT(*) FROM adult_data WHERE hours_per_week = 99
    GROUP BY hours_per_week, salary
""")
print(tabulate(fetch_all(cursor), "keys", "psql"))


'''10. Посчитайте среднее время работы (hours-per-week) зарабатывающих мало и много (salary) для каждой страны (native-country).''' 
print('10. Посчитайте среднее время работы (hours-per-week) зарабатывающих мало и много (salary) для каждой страны (native-country).')
cursor.execute(
"""
SELECT native_country, salary, AVG(hours_per_week)
FROM adult_data
GROUP BY native_country, salary
"""
)
print(tabulate(fetch_all(cursor), "keys", "psql"))