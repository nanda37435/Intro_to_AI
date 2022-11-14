

data = []

def load_data():
    global data
    f = open('alldata.txt', "r", encoding = 'utf-8')
    data = f.readlines()
    f.close()

load_data()

lines = data 
temp_dict = dict()
for each_line in lines:

	rating, review_id, review = each_line.split('|')
	flag = True if rating == '5' else False

	spl_chars = ("'", '"', '?', ',', '!', '.', '-', '(', ')', ':', ';', '*', "&", '@', '#', '$', '^', 
				'+', '=', '/', '[', ']', '{', '}', '<', '>', '%', '_', '\\', '`', '~')
	for each_word in review.split():
		each_word = each_word.lower()
		for spl_char in spl_chars:
			each_word = each_word.replace(spl_char, '')

		if each_word in temp_dict.keys():
			temp_dict[each_word]['total'] += 1
			if flag:
				temp_dict[each_word]['total_5'] += 1
			else:
				temp_dict[each_word]['total_1'] += 1
		else:
			temp_dict[each_word] = dict()
			temp_dict[each_word]['total'] = 1
			temp_dict[each_word]['total_1'] = 0
			temp_dict[each_word]['total_5'] = 0
			if flag:
				temp_dict[each_word]['total_5'] = 1
			else:
				temp_dict[each_word]['total_1'] = 1

temp_dict = dict(sorted(temp_dict.items(), key = lambda word: word[1]['total'], reverse = True))

for keys, values in temp_dict.items():
	print(keys, values['total'])















		for each_line in lines:

			rating, review_id, review = each_line.split('|')
			flag = True if rating == '5' else False

			spl_chars = ("'", '"', '?', ',', '!', '.', '-', '(', ')', ':', ';', '*', "&", '@', '#', '$', '^', 
						'+', '=', '/', '[', ']', '{', '}', '<', '>', '%', '_', '\\', '`', '~')
			for each_word in review.split():
				each_word = each_word.lower()
				for spl_char in spl_chars:
					each_word = each_word.replace(spl_char, '')

				if each_word in temp_dict.keys():
					temp_dict[each_word]['total'] += 1
					if flag:
						temp_dict[each_word]['total_5'] += 1
					else:
						temp_dict[each_word]['total_1'] += 1
				else:
					temp_dict[each_word] = dict()
					temp_dict[each_word]['total'] = 1
					temp_dict[each_word]['total_1'] = 0
					temp_dict[each_word]['total_5'] = 0
					if flag:
						temp_dict[each_word]['total_5'] = 1
					else:
						temp_dict[each_word]['total_1'] = 1