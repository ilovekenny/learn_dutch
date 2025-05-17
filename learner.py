from wordlist import WordList
import random
class MyLearner:
    def __init__(self, words_list:WordList):
        self.status = 0
        self.words_list = words_list
        self.words_items = self.words_list.get_all_words()
        self.n_list = len(self.words_list.get_all_words())
        
    def SelectWords(self,n:int=10):
        # n, int, number of words to test
        score_list = self.words_items[4]
        print(score_list)


