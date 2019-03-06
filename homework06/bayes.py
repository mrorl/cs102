import string
import math
import copy


class NaiveBayesClassifier:

    def __init__(self, alpha=1) -> None:
        self.smoothing = alpha
        self.chance = [0, 0, 0]

    def fit(self, X, y):
        """ Fit Naive Bayes classifier according to X, y.
        X - объекты News
        y - label-ы
        """
        self.labels = [i for i in set(y)]
        self.labels.sort()
        words = []
        words_in_table = []

        lab_num = [0, 0, 0]

        translator = str.maketrans("", "", string.punctuation)  # избавимся от символов пунктуации:
        for i, st in enumerate(X):
            for word in st.translate(translator).lower().split():  # приведем к нижнему регистру и разделим
                words.append([word, y[i]])  # формируем список слов и лейблов при них

        self.table = [[0]*7 for _ in range(len(words))]  # создаем таблицу

        for i in range(len(words)):
            if words[i][0] not in words_in_table:
                self.table[i][0] = words[i][0]
                words_in_table.append(words[i][0])

                if words[i][1] == 'good':
                    self.table[i][1] += 1
                    lab_num[0] += 1
                elif words[i][1] == 'maybe':
                    self.table[i][2] += 1
                    lab_num[1] += 1
                elif words[i][1] == 'never':
                    self.table[i][3] += 1
                    lab_num[2] += 1
            else:
                idx = words_in_table.index(words[i][0])

                if words[idx][1] == 'good':
                    self.table[idx][1] += 1
                elif words[idx][1] == 'maybe':
                    self.table[idx][2] += 1
                elif words[idx][1] == 'never':
                    self.table[idx][3] += 1
        for i in range(len(words)):
            self.table[i][4] = (self.table[i][1] + self.smoothing)/(lab_num[0] + len(words_in_table)*self.smoothing)
            self.table[i][5] = (self.table[i][2] + self.smoothing)/(lab_num[1] + len(words_in_table)*self.smoothing)
            self.table[i][6] = (self.table[i][3] + self.smoothing)/(lab_num[2] + len(words_in_table)*self.smoothing)

        for i in range(3):
            self.chance[i] = math.log(lab_num[i]/(lab_num[0] + lab_num[1] + lab_num[2]))

    def predict(self, X):
        """ Perform classification on an array of test vectors X. """
        predict_label = []
        words = []

        for st in X.split():
            words.append(st)

        for word in words:
            chance = copy.deepcopy(self.chance)
            for i in range(len(self.table)):
                if word == self.table[i][0]:
                    for label in range(len(self.labels)):
                        chance[label] += math.log(self.table[i][label+4])
        predict_label.append(self.labels[chance.index(max(chance))])

        return predict_label

    def score(self, X_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        prediction = self.predict(X_test)
        count = 0
        for i in range(len(prediction)):
            if prediction[i] == y_test[i]:
                count += 1
        score = count / len(y_test)
        return score
