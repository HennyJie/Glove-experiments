import codecs
import json
import numpy as np

'''Serializable/Pickleable class to replicate the functionality of collections.defaultdict'''


class autovivify_list(dict):
    def __missing__(self, key):
        value = self[key] = []
        return value

    def __add__(self, x):
        '''Override addition for numeric types when self is empty'''
        if not self and isinstance(x, Number):
            return x
        raise ValueError

    def __sub__(self, x):
        '''Also provide subtraction method'''
        if not self and isinstance(x, Number):
            return -1 * x
        raise ValueError


def build_word_vector_matrix(vector_file, n_words):
    '''Read a GloVe array from sys.argv[1] and return its vectors and labels as arrays'''
    np_arrays = []
    labels_array = []

    with codecs.open(vector_file, 'r', 'utf-8') as f:
        for i, line in enumerate(f):
            sr = line.split()
            print(sr[0])
            labels_array.append(sr[0])
            print(sr[1:])
            np_arrays.append(np.array([float(j) for j in sr[1:]]))
            if i == n_words - 1:
                return np.array(np_arrays), labels_array
        return np.array(np_arrays), labels_array


def custom_build_word_vector_matrix(vector_file):
    '''Read a GloVe array from sys.argv[1] and return its vectors and labels as arrays'''
    np_arrays = []
    labels_array = []

    final_np_arrays = []
    final_labels_array = []

    with codecs.open(vector_file, 'r', 'utf-8') as f:
        for i, line in enumerate(f):
            sr = line.split()
        #     print(sr[0])
            labels_array.append(sr[0])
        #     print(sr[1:])
            np_arrays.append(np.array([float(j) for j in sr[1:]]))

    word_to_vec_dict = dict(zip(labels_array, np_arrays))

    not_existed_path = "/Users/hejiecui/Developer/Research/SceneGraph/Dataset/scenegraph_train_objects_not_existed_in_yago.txt"
    with open(not_existed_path, "r") as f:
        word_list = [word.strip() for word in f.readlines()]
    word_list = word_list[1:]

#     with codecs.open(vector_file, 'r', 'utf-8') as f:
#         for i, line in enumerate(f):
#             sr = line.split()
#             print(sr[0])
#             labels_array.append(sr[0])
#             print(sr[1:])
#             np_arrays.append(np.array([float(j) for j in sr[1:]]))
#             if i == n_words - 1:
#                 return np.array(np_arrays), labels_array
#         return np.array(np_arrays), labels_array

    for word in word_list:
        if word in word_to_vec_dict:
            vec = word_to_vec_dict[word]
        else:
            vec = [0.0] * 100
        final_labels_array.append(word)
        final_np_arrays.append(np.array(vec))
    return np.array(final_np_arrays), final_labels_array


def get_cache_filename_from_args(args):
    a = (args.vector_dim, args.num_words, args.num_clusters)
    return '{}D_{}-words_{}-clusters.json'.format(*a)


def get_label_dictionaries(labels_array):
    id_to_word = dict(zip(range(len(labels_array)), labels_array))
    word_to_id = dict((v, k) for k, v in id_to_word.items())
    return word_to_id, id_to_word


def save_json(filename, results):
    with open(filename, 'w') as f:
        json.dump(results, f)


def load_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)
