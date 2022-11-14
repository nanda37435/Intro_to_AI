import math
import re

class Bayes_Classifier:

    def __init__(self):
        self.features = dict()
        """self.stop_words = set(['i', 'me', 'a', 'is', 'the', 'for', 'am', 'was', 'actually', 'myself', 
        	'this', 'and', 'of', 'it', 'to', 'in', 'that', 'you', 'one', 'as', 'with', 'movie', 'made', 
        	'on', 'its', 'my', 'be', 'are', 'so', 'his', 'at', 'he', 'who', 'when', 'were', 'or', 'had',
        	'even', 'would', 'will', 'how', 'than', 'did', 'should', 'been', 'through', 'being', 'such',
        	'after', 'cant', 'im', 'say', 'ive', 'him', 'those', 'two', 'does', 'now', 'why', 'these',
        	'us', 'thats', 'take', 'tom', 'plot', 'thought', 'together', 'anything', ])"""
        self.stop_words = set(['the', 'and', 'a', 'of', 'i', 'movie', 'it', 'is', 'to', 'this', 'was', 'in', 'that', 'you', 'one', 'for', 'as', 'with', 'but', 'film', 'all', 'have', 'on', 'its', 'my', 'be', 'are', 'so', 'an', 'his', 'he', 'movies', 'at', 'time', 'just', 'about', 'see', 'ever', 'they', 'who', 'me', 'what', 'by', 'out', 'if', 'from', 'has', 'when', 'seen', 'made', 'there', 'well', 'can', 'were', 'think', 'or', 'had', 'even', 'would', 'up', 'will', 'how', 'some', 'people', 'first', 'most', 'only', 'dont', 'than', 'watch', 'because', 'get', 'did', 'no', 'acting', 'much', 'way', 'her', 'also', 'could', 'their', 'too', 'do', 'make', 'life', 'into', 'plot', 'your', 'which', 'been', 'action', 'should', 'we', 'films', 'any', 'other', 'know', 'go', 'she', 'him', 'ive', 'makes', 'say', 'after', 'im', 'times', 'every', 'cant', 'them', 'those', 'saw', 'again', 'real', 'then', 'two', 'through', 'cast', 'being', 'such', 'though', 'where', 'off', 'man', 'book', 'now', 'does ', 'want', 'watching', 'got', 'job', 'whole', 'part', 'thing', 'why', 'star', 'always', 'ending', 'back', 'something', 'while', 'long', 'actually', 'everyone', 'anyone', 'another', 'years', 'done', 'going', 'give', 'am', 'these', 'new', 'find', 'guy', 'john', 'far', 'things', 'look', 'come', 'same', 'especially', 'watched', 'us', 'around', 'thats', 'take', 'our', 'both', 'kids', 'top', 'probably', 'work', 'since', 'show', 'yet', 'gets ', 'everything', 'before', 'seeing', 'almost ', 'without ', 'year', 'wasnt', 'last', 'may', 'enough', 'put', 'nothing', 'own', 'went', 'together', 'anything', 'bit', 'once', 'isnt', 'away', 'making', 'tom', 'between', 'kind', 'found', 'came', 'shows', 'here', 'girl', 'said ', 'three', 'course', 'couldnt', 'hes', 'along', 'need', 'point', 'parts', 'although', 'until', 'black', 'havent', 'next', 'based', 'totally', 'however', 'each', 'idea', 'youre', 'heart', 'today', 'gave', 'during', 'might', 'entire', 'dead', 'picture', 'simply', 'remember', 'plays ', 'version', 'night', 'else', 'left', 'oh', 'maybe', 'gives', 'michael', 'someone', 'goes', 'guys', 'trying', 'boy', 'person', 'place', 'kid', 'used', 'hope', 'keep', 'takes', 'dvd', 'comes', 'human', 'set', 'lines', 'others', 'main', 'tell', 'wrong', 'jack', 'theater', 'jim'])
        self.spl_chars = ("'", '"', '?', ',', '!', '.', '-', '(', ')', ':', ';', '*', "&", '@', '#', '$', '^', 
						'+', '=', '/', '[', ']', '{', '}', '<', '>', '%', '_', '\\', '`', '~')
        self.total_ratings_5 = 0
        self.total_ratings_1 = 0
        self.total_words_rating_5 = 0
        self.total_words_rating_1 = 0
        self.unique_words_rating_5 = set()
        self.unique_words_rating_1 = set()



    def train(self, lines):
        for each_line in lines:

        	rating, review_id, review = each_line.split('|')
        	flag = True if rating == '5' else False

        	if flag:
        		self.total_ratings_5 += 1
        	else:
        		self.total_ratings_1 += 1


        	for each_word in review.split():

        		each_word = each_word.lower()

        		for spl_char in self.spl_chars:
        			each_word = each_word.replace(spl_char, '')

        		if each_word in self.stop_words:
        			continue

        		try:
        			each_word = int(each_word)
        			continue
        		except:
        			pass

        		if not each_word:
        			continue

        		if each_word in self.features.keys():
        			self.features[each_word]['total'] += 1
        			if flag:
        				self.features[each_word]['total_5'] += 1
        			else:
        				self.features[each_word]['total_1'] += 1
        		else:
        			self.features[each_word] = dict()
        			self.features[each_word]['total'] = 1
        			self.features[each_word]['total_1'] = 0
        			self.features[each_word]['total_5'] = 0
        			if flag:
        				self.features[each_word]['total_5'] = 1
        			else:
        				self.features[each_word]['total_1'] = 1

        		if flag:
        			self.total_words_rating_5 += 1
        			self.unique_words_rating_5.add(each_word)
        		else:
        			self.total_words_rating_1 += 1
        			self.unique_words_rating_1.add(each_word)





    def classify(self, lines):

    	predictions = []

    	prior_probab_rating_5 = self.total_ratings_5/(self.total_ratings_5 + self.total_ratings_1)
    	prior_probab_rating_1 = self.total_ratings_1/(self.total_ratings_5 + self.total_ratings_1)

    	total_words = len(self.features.keys())
        
    	for each_line in lines:
    		rating, review_id, review = each_line.split('|')

    		post_probab_rating_5 = prior_probab_rating_5
    		post_probab_rating_1 = prior_probab_rating_1

    		for each_word in each_line.split():
    			
    			each_word = each_word.lower()
    			
    			for spl_char in self.spl_chars:
    				each_word = each_word.replace(spl_char, '')

    			if each_word in self.stop_words:
    				continue

    			try:
    				each_word = int(each_word)
    				continue
    			except:
    				pass

    			if not each_word:
    				continue

    			if each_word in self.features.keys():
    				probab_rating_5 = (self.features[each_word]['total_5'] + 1) / (self.total_words_rating_5 + total_words)
    				probab_rating_1 = (self.features[each_word]['total_1'] + 1) / (self.total_words_rating_1 + total_words)
    				    				
    			else:
    				probab_rating_5 = 1 / (self.total_words_rating_5 + total_words)
    				probab_rating_1 = 1 / (self.total_words_rating_1 + total_words)


    			post_probab_rating_5 *= probab_rating_5
    			post_probab_rating_1 *= probab_rating_1

    		predictions.append('5' if probab_rating_5 > probab_rating_1 else '1')

    	return predictions

