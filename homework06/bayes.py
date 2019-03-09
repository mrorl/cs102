import string
import math
import copy


class NaiveBayesClassifier:

    def __init__(self, alpha=1) -> None:
        self.smoothing = alpha
        self.chance = [0, 0, 0]
        self.labels = []
        self.table = []

    def fit(self, X, y):
        """ Fit Naive Bayes classifier according to X, y."""
        words = []
        words_in_table = []
        labeled_news = [0, 0, 0]  # сколько новостей отмечены good, maybe, never
        lab_num = [0, 0, 0]  # сколько раз встречаются слова, относящиеся к good, maybe, never
        self.labels = [i for i in set(y)]
        self.labels.sort()

        '''Найдем ln от априорных вероятностей классов good, maybe, never'''

        for i in range(len(X)):
            if y[i] == 'good':
                labeled_news[0] += 1
            elif y[i] == 'maybe':
                labeled_news[1] += 1
            elif y[i] == 'never':
                labeled_news[2] += 1
        for i in range(3):
            self.chance[i] = math.log(labeled_news[i]/len(X))

        '''Приведем все сообщения к нижнему регистру и избавимся от символов пунктуации и разделим'''                       

        translator = str.maketrans("", "", string.punctuation)
        for i, st in enumerate(X):
            for word in st.translate(translator).lower().split():
                words.append([word, y[i]])

        '''Создаем таблицу, заполняем первые 4 столбца'''

        self.table = [[0]*7 for _ in range(len(words))]

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
                    lab_num[0] += 1
                elif words[idx][1] == 'maybe':
                    self.table[idx][2] += 1
                    lab_num[1] += 1
                elif words[idx][1] == 'never':
                    self.table[idx][3] += 1
                    lab_num[2] += 1

        '''Вычисляем вероятность встретить слово в каждом из классов'''
        
        for i in range(len(words)):
            self.table[i][4] = math.log(((self.table[i][1] + self.smoothing)/(lab_num[0] + len(words_in_table)*self.smoothing)))
            self.table[i][5] = math.log(((self.table[i][2] + self.smoothing)/(lab_num[1] + len(words_in_table)*self.smoothing)))
            self.table[i][6] = math.log(((self.table[i][3] + self.smoothing)/(lab_num[2] + len(words_in_table)*self.smoothing)))


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
                        chance[label] += self.table[i][label+4]
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
