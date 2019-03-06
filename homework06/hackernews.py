import bottle
from bottle import (
    route, run, template, request, redirect
)
from scraputils import get_news
from db import News, session
from bayes import NaiveBayesClassifier
import string
bottle.TEMPLATE_PATH.insert(0, 'views')


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template.tpl', rows=rows)


@route("/add_label/")
def add_label():
    # PUT YOUR CODE HERE
    # 1. Получить значения параметров label и id из GET-запроса
    # 2. Получить запись из БД с соответствующим id (такая запись только одна!)
    # 3. Изменить значение метки записи на значение label
    # 4. Сохранить результат в БД
    s = session()
    get_label = request.query.label
    get_id = request.query.id
    record = s.query(News).filter(News.id == get_id).one()
    record.label = get_label
    s.commit()
    redirect("/news")


@route("/update")
def update_news():
    # PUT YOUR CODE HERE
    # 1. Получить данные с новостного сайта
    # 2. Проверить, каких новостей еще нет в БД. Будем считать,
    #    что каждая новость может быть уникально идентифицирована
    #    по совокупности двух значений: заголовка и автора
    # 3. Сохранить в БД те новости, которых там нет
    s = session()
    news = get_news("https://news.ycombinator.com/newest", n_pages=1)
    old_news = s.query(News).all()
    for i in range(len(news)):
        for j in range(len(old_news)):
            if news[i]['author'] != old_news[j].author and news[i]['title'] != old_news[j].title:
                news_add = News(title=news[i]['title'],
                            author=news[i]['author'],
                            url=news[i]['url'],
                            comments=news[i]['comment'],
                            points=news[i]['point'])
                s.add(news_add)
                break
    s.commit()
    redirect("/news")


@route("/classify")
def classify_news():
    s = session()
    labeled_news = s.query(News).filter(News.label != None).all()
    x_train = [news.title for news in labeled_news]
    y_train = [news.label for news in labeled_news]
    classifier = NaiveBayesClassifier()
    classifier.fit(x_train, y_train)

    new_news = s.query(News).filter(News.label == None).all()
    good, maybe, never = [], [], []
    for current in new_news:
        prediction = classifier.predict(current.title)

        if prediction == ['good']:
            good.append(current)
        elif prediction == ['maybe']:
            maybe.append(current)
        elif prediction == ['never']:
            never.append(current)

    return template('recommendations', good=good, maybe=maybe, never=never)


if __name__ == '__main__':
    run(host="localhost", port=8080)
