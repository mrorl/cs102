import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from datetime import datetime
from api import messages_get_history
from api_models import Message
from collections import Counter
from typing import List, Tuple
import config


Dates = List[datetime.date]
Frequencies = List[int]


plotly.tools.set_credentials_file(
    username=config.PLOTLY_CONFIG['username'],
    api_key=config.PLOTLY_CONFIG['api_key']
)


def fromtimestamp(ts: int) -> datetime.date:
    return datetime.fromtimestamp(ts).date()


def count_dates_from_messages(messages: List[Message]) -> Tuple[Dates, Frequencies]:
    """ Получить список дат и их частот

    :param messages: список сообщений
    """
    msgl = [fromtimestamp(c.get('date')) for c in messages]
    num = Counter(msgl)
    dates = []
    freq = []

    for date in num:
        dates.append(date)
        freq.append(num[date])

    return dates, freq


def plotly_messages_freq(dates: Dates, freq: Frequencies) -> None:
    """ Построение графика с помощью Plot.ly

    :param date: список дат
    :param freq: число сообщений в соответствующую дату
    """
    data = [go.Scatter(x=dates, y=freq)]
    py.iplot(data)


if __name__ == '__main__':
    messages = messages_get_history(222885805, offset=0, count=200)
    x, y = count_dates_from_messages(messages)
    plotly_messages_freq(x, y)
