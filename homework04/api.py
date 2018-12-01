import requests
import time
import config


def get(url, params={}, timeout=5, max_retries=5, backoff_factor=0.3):
    """ Выполнить GET-запрос

    :param url: адрес, на который необходимо выполнить запрос
    :param params: параметры запроса
    :param timeout: максимальное время ожидания ответа от сервера
    :param max_retries: максимальное число повторных запросов
    :param backoff_factor: коэффициент экспоненциального нарастания задержки
    """
    for i in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=timeout)
            return response
        except requests.exceptions.RequestException:
            if i == max_retries - 1:
                raise
            delay = backoff_factor * (2 ** i)
            time.sleep(delay)


def get_friends(user_id: int, fields="") -> dict:
    """ Вернуть данных о друзьях пользователя

    :param user_id: идентификатор пользователя, список друзей которого нужно получить
    :param fields: список полей, которые нужно получить для каждого пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"

    query_params = {
        'domain': config.VK_CONFIG["domain"],
        'access_token': config.VK_CONFIG["access_token"],
        'user_id': user_id,
        'fields': fields,
        'version': config.VK_CONFIG['version']
        }

    query = "{domain}/friends.get?access_token={" \
            "access_token}&user_id={user_id}&fields={fields}&v={version}".format(
        **query_params)
    response = get(query, query_params)
    err = response.json().get('error')
    if err:
        return []
    return response.json()['response']['items']


def messages_get_history(user_id: int, offset: int = 0, count: int = 200) -> list:
    """ Получить историю переписки с указанным пользователем

    :param user_id: идентификатор пользователя, с которым нужно получить историю переписки
    :param offset: смещение в истории переписки
    :param count: число сообщений, которое нужно получить
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    assert isinstance(offset, int), "offset must be positive integer"
    assert offset >= 0, "user_id must be positive integer"
    assert count >= 0, "user_id must be positive integer"
    max_count = 200
    messages: list = []

    query_params = {
        'domain': config.VK_CONFIG["domain"],
        'access_token': config.VK_CONFIG["access_token"],
        'user_id': user_id,
        'offset': offset,
        'count': min(count, max_count),
        'version': config.VK_CONFIG['version']
        }

    while count > 0:
        query = "{domain}/messages.getHistory?access_token={access_token}&user_id={user_id}&offset={offset}&count={count}&v={version}".format(**query_params)
        response = requests.get(query)  # создает модуль requests
        count -= min(count, max_count)
        query_params['offset'] += 200
        query_params['count'] = min(count, max_count)
        messages += response.json()['response']['items']  # формируем словарь
        time.sleep(0.4)
    return messages
