import argparse, utils, sys
from scipy.spatial.distance import cosine

def word_arithmetic(base_word, minus_word, plus_word, word_to_id, id_to_word, df):
	'''Returns a word string that is the result of the vector arithmetic'''
	try:
		base_vec  = df[word_to_id[base_word]]
		minus_vec = df[word_to_id[minus_word]]
		plus_vec  = df[word_to_id[plus_word]]
	except KeyError as err:
		print(err)
		return err, None

	result = base_vec - minus_vec + plus_vec
	words = (base_word, minus_word, plus_word)
	return None, find_nearest(words, result, id_to_word, df)

def find_nearest(words, vec, id_to_word, df, method='cosine'):

	if method == 'cosine':
		minim = (sys.maxsize, 0) # min, index		
		for i, v in enumerate(df):
			# skip the base word, its usually the closest
			if id_to_word[i] in words:
				continue
			dist = cosine(vec, v)
			if dist < minim[0]:
				minim = (dist, i)
		return id_to_word[minim[1]], minim[0] # word, cosine distance
	else:
		raise Exception('{} is not an excepted method parameter'.format(method))


def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('--vector_depth', '-d',
						type=int,
						choices=[50, 100, 200, 300],
						default=50,
						help='What vector GloVe vector depth to use.')
	parser.add_argument('--glove_path', '-i',
		                default='data/glove',
		                help='GloVe vector file path')
	parser.add_argument('--num_words', '-n',
						type=int,
						default=10000,
						help='The number of lines to read from the GloVe vector file.')
	return parser.parse_args()

if __name__ == '__main__':

	args = parse_args()
	vector_file = args.glove_path + '/' + 'glove.6B.' + str(args.vector_depth) + 'd.txt'
	
	df, labels_array = utils.build_word_vector_matrix(vector_file, args.num_words)
	word_to_id, id_to_word = utils.get_label_dictionaries(labels_array)
	err, result = word_arithmetic('king', 'man', 'woman', word_to_id, id_to_word, df)

	if result:
		print(result)
	else:
		print('"{}"	not found in the dataset.')
		
