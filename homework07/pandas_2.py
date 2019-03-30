''' 1. В каком месяце (и какого года) было больше всего публикаций?'''
sns_plot = sns.jointplot(df['month'], df['year'], kind='kde', color='green')

''' 2. Проанализируйте публикации в месяце из предыдущего вопроса'''
#features = ['content_len','comments','favs','views','votes_plus','votes_minus']

features = ['comments','favs','votes_plus','votes_minus']
data = df[(df['year'] == 2015) & (df['month'] == 3)]
sales_data = data[[x for x in features] + ['dayofweek']]
sales_data.groupby('dayofweek').sum().plot()

features = ['comments','favs','votes_plus','votes_minus']
data = df[(df['year'] == 2015) & (df['month'] == 3)]
sales_data = data[[x for x in features] + ['hour']]
sales_data.groupby('hour').sum().plot()

''' 3. Когда лучше всего публиковать статью?'''
_, axes = plt.subplots(1, 2, sharey=True, figsize=(16,6))
sns.boxplot(x='hour', y='views', data=df, ax=axes[0]);
sns.violinplot(x='hour', y='views', data=df, ax=axes[1]);

_, axes = plt.subplots(1, 2, sharey=True, figsize=(16,6))
sns.boxplot(x='dayofweek', y='views', data=df, ax=axes[0]);
sns.violinplot(x='dayofweek', y='views', data=df, ax=axes[1]);

''' 4. Кого из топ-20 авторов чаще всего минусуют?'''
top_authors = df.author.value_counts().sort_values(ascending = False).head(20).index.values
sns.boxplot(y="author", x="votes_minus", data=df[df.author.isin(top_authors)], orient="h")

''' 5. Сравните субботы и понедельники'''
#features = ['content_len','comments','favs','views','votes_plus','votes_minus']
features = ['votes_plus','votes_minus']

monday = df[df['dayofweek'] == 1]
sales_data = monday[[x for x in features] + ['hour']]
sales_data.groupby('hour').sum().plot()

saturday = df[df['dayofweek'] == 6]
sales_data = saturday[[x for x in features] + ['hour']]
sales_data.groupby('hour').sum().plot()
