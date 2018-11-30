from datetime import datetime
from statistics import median
from typing import Optional
from api import get_friends
from api_models import User


def age_predict(user_id: int) -> Optional[float]:
    """ Наивный прогноз возраста по возрасту друзей
    Возраст считается как медиана среди возраста всех друзей пользователя
    :param user_id: идентификатор пользователя
    :return: медианный возраст пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    friends = get_friends(user_id, 'bdate')

    ages = []
    friends = [User(**friend) for friend in friends]

    for friend in friends:
        if friend.bdate is not None:
            date = friend.bdate.split('.')
            if len(date) == 3:
            	bday = int(date[0])
            	bmonth = int(date[1])
            	age = datetime.now().year - int(date[2])
            	if (datetime.now().month < bmonth) or ((datetime.now().month == bmonth) and (datetime.now().day < bday)):
            		age -= 1
            	ages.append(age)
    if ages != []:
    	return median(ages)
    else:
    	return None


if __name__ == '__main__':
    predicted_age = age_predict(57902269)
    print(predicted_age)

