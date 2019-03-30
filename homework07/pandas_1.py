'''1. Сколько мужчин и женщин (признак sex) представлено в этом наборе данных?'''
data['sex'].value_counts()

'''2. Каков средний возраст (признак age) женщин?'''
data[data['sex'] == 'Female']['age'].mean()

'''3. Какова доля граждан Германии (признак native-country)?'''
data['native-country'].value_counts(normalize=True)['Germany']

'''4-5. Каковы средние значения и среднеквадратичные отклонения возраста тех, 
кто получает более 50K в год (признак salary) и тех, кто получает менее 50K в год?'''
data.groupby(['salary'])['age'].agg([np.mean, np.std])

'''6. Правда ли, что люди, которые получают больше 50k, имеют как минимум высшее образование? 
(признак education – Bachelors, Prof-school, Assoc-acdm, Assoc-voc, Masters или Doctorate)'''
pd.crosstab(data['education'], data['salary'])

'''7. Выведите статистику возраста для каждой расы (признак race) и каждого пола. 
Используйте groupby и describe. Найдите таким образом максимальный возраст мужчин расы Amer-Indian-Eskimo.'''
data[data['sex'] == 'Female'].groupby(['race'])['age'].describe(percentiles=[])
data[data['sex'] == 'Male'].groupby(['race'])['age'].describe(percentiles=[])

'''8. Среди кого больше доля зарабатывающих много (>50K): среди женатых или холостых мужчин (признак marital-status)? 
Женатыми считаем тех, у кого marital-status начинается с Married (Married-civ-spouse, Married-spouse-absent или Married-AF-spouse), остальных считаем холостыми.'''
pd.crosstab(data['marital-status'], data['salary'])

'''9. Какое максимальное число часов человек работает в неделю (признак hours-per-week)? 
Сколько людей работают такое количество часов и каков среди них процент зарабатывающих много?'''
data['hours-per-week'].max()
data[data['hours-per-week'] == data['hours-per-week'].max()]['age'].count()
pd.crosstab(data['hours-per-week'] == data['hours-per-week'].max(), data['salary'])

'''10. Посчитайте среднее время работы (hours-per-week) зарабатывающих мало и много (salary) для каждой страны (native-country).'''
countries = set(data['native-country'])
for country in countries:
    result1 = data[(data['salary'] == '>50K') & (data['native-country'] == country)]['hours-per-week'].mean()
    result2 = data[(data['salary'] == ' <=50K') & (data['native-country'] == country)]['hours-per-week'].mean()
    print(country, '>50K', result1, ' <=50K', result2)
