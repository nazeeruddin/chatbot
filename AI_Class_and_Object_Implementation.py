import cPickle
# from duckling_simplified import Parse_date_duckling
# import re
# nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.util import ngrams
import re


class Email_AI:

    def __init__(self):

        with open('./Data/my_dumped_classifier.pkl', 'rb') as fid:
            self.clf = cPickle.load(fid)

        with open('./Data/my_dumped_idf.pkl', 'rb') as fid:
            self.idf = cPickle.load(fid)

        with open('./Data/my_dumped_data.pkl', 'rb') as fid:
            self.vector = cPickle.load(fid)

        with open('./Data/my_dumped_y.pkl', 'rb') as fid:
            self.y = cPickle.load(fid)

    def fit_classifier(self):

        self.clf.fit(self.vector, self.y)

    def generate_ngrams(self, s, n):
        l = []
        s = s.lower()
        tokens = [token for token in s.split(" ") if token != ""]
        output = list(ngrams(tokens, n))
        for i in output:
            l.append(' '.join(i))
        return l

    def user_data_preparation(self, sentence):

        self_flag = 0
        """    duckling   """
        # print "---------duckling---------"
        # grain, date, end_date, date_string = Parse_date_duckling(sentence)
        # print "--------------------------"
        """   removing Time in Question 
        if date_string is not None and date_string.lower() in sentence.lower():
            sentence = sentence.replace(date_string, '')
            sentence = sentence.strip()"""
        """  ---- FINDING I/My FLAG ---  """

        if re.search(r'\bmy\b', sentence.lower()):
            self_flag = 1
        if re.search(r'\bi\b', sentence.lower()):
            self_flag = 1

        """   --- Filter ALl Date Formats (Numbers) and any special Characters Except Aphabets ---   """
        sentence = re.sub('[^a-zA-Z]', ' ', sentence)

        return sentence, self_flag, '', ''

    def user_input(self, text):

        # text = raw_input('Q: ')
        text, self_flag, date, end_date = self.user_data_preparation(text)
        print 'after:', text
        # review = re.sub('[^a-zA-Z]', ' ', text)
        review = text.lower()
        review = review.split()
        ps = PorterStemmer()
        review = [ps.stem(word) for word in review if not word in set(stopwords.words('english'))]
        review = ' '.join(review)
        user_input = self.idf.transform([review]).toarray()
        output = self.clf.predict(user_input)
        confidence = self.clf.predict_proba(user_input).max().round(3)*100
        mean = self.clf.predict_proba(user_input).mean().round(3)*100
        print "reply: ", output
        print "confidence: ", confidence
        print 'Mean: ', mean
        return output[0], self_flag, date, end_date, review, confidence
