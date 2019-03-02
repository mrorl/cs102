import string
from string import maketrans

class NaiveBayesClassifier:

    def __init__(self, alpha) -> None:
        self.smoothing = alpha 


    def fit(self, X, y):
        """ Fit Naive Bayes classifier according to X, y. 
        X - объекты News
        y - label-ы
        """
        self.labels = [i for i in set(y)]
        self.labels.sort()
        words = []
        words_in_table = []

        lab_num0 = 0
        lab_num1 = 0
        lab_num2 = 0

        translator = str.maketrans("", "", string.punctuation)  # избавимся от символов пунктуации:
        for i, st in enumerate(X):
            for word in st.translate(translator).lower().split(): # приведем к нижнему регистру и разделим
                words.append([word, y[i]])  # формируем список слов и лейблов при них

        self.table = [[0]*7 for _ in range(len(words))] # создаем таблицу

        for i in len(words):
            if words[i][0] not in words_in_table:
                self.table[i][0] = words[i][0]
                words_in_table.append(words[i][0])

                if words[i][1] == 'good':
                    self.table[i][1] += 1
                    lab_num0 += 1
                elif words[i][1] == 'maybe':
                    self.table[i][2] += 1
                    lab_num2 += 1
                elif words[i][1] == 'never':
                    self.table[i][3] += 1
                    lab_num3 += 1
            else:
                idx = words_in_table.index(words[i][0])

                if words[idx][1] == 'good':
                    self.table[idx][1] += 1
                elif words[idx][1] == 'maybe':
                    self.table[idx][2] += 1
                elif words[idx][1] == 'never':
                    self.table[idx][3] += 1
        for i in len(words):
            self.table[i][4] = (self.table[i][1] + self.smoothing)/(lab_num0 + len(words_in_table)*self.smoothing)
            self.table[i][5] = (self.table[i][2] + self.smoothing)/(lab_num1 + len(words_in_table)*self.smoothing)
            self.table[i][6] = (self.table[i][3] + self.smoothing)/(lab_num2 + len(words_in_table)*self.smoothing)


    def predict(self, X):
        """ Perform classification on an array of test vectors X. """
        predict_label =  []
        words = []

        translator = str.maketrans("", "", string.punctuation) # избавимся от символов пунктуации:
        for i in X:
            for word in i.translate(translator).lower().split():  # приведем к нижнему регистру и разделим
                words.append(word)  # формируем словарь

        for words in words:
            for i in range(len(self.table)):
                if words == self.table[i][0]:
                    for label in range(len(set(y))):
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
