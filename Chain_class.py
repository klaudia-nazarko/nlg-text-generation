import scipy.sparse
from sklearn.preprocessing import normalize
import numpy as np
import re
import warnings

class Chain:
    def __init__(self, text_object, n=2):
        self.text_object = text_object
        self.n = n

        self.tokens, self.tokens_distinct = text_object.tokens, text_object.tokens_distinct
        self.ngrams, self.ngrams_distinct = self.create_ngrams()
        self.token2ind, self.ind2token = text_object.token2ind, text_object.ind2token
        self.ngram2ind, self.ind2ngram = text_object.create_word_mapping(self.ngrams_distinct)
        self.transition_matrix_prob = self.create_transition_matrix_prob()

    def create_ngrams(self):
        sequences = [self.tokens[i:] for i in range(self.n)]
        ngrams = [' '.join(ngram) for ngram in list(zip(*sequences))]
        return ngrams, list(set(ngrams))

    def tokens_info(self):
        self.text_object.tokens_info()

    def ngrams_info(self):
        print('ngrams level: %d, total ngrams: %d, distinct ngrams: %d' % (
        self.n, len(self.ngrams), len(self.ngrams_distinct)))

    def random_ngram(self):
        return np.random.choice(self.ngrams)

    def create_transition_matrix(self):
        row_ind, col_ind, values = [], [], []

        for i in range(len(self.tokens[:-self.n])):
            ngram = ' '.join(self.tokens[i:i + self.n])
            ngram_ind = self.ngram2ind[ngram]
            next_word_ind = self.token2ind[self.tokens[i + self.n]]

            row_ind.extend([ngram_ind])
            col_ind.extend([next_word_ind])
            values.extend([1])

        S = scipy.sparse.coo_matrix((values, (row_ind, col_ind)), shape=(len(self.ngram2ind), len(self.token2ind)))
        return S

    def create_transition_matrix_prob(self):
        transition_matrix = self.create_transition_matrix()
        return normalize(transition_matrix, norm='l1', axis=1)

    def check_prefix(self, prefix):
        prefix_list = prefix.split(' ')[-self.n:]
        if len(prefix_list) < self.n:
            warnings.warn(
                'Prefix is too short, please provide prefix of length: %d. Random ngram used instead.' % self.n)
            return self.random_ngram()
        else:
            prefix = ' '.join(prefix_list)
            if prefix in self.ngrams:
                return prefix
            else:
                warnings.warn(
                    'Prefix is not included in ngrams of the model. Provide another prefix. Random ngram used instead.')
                return self.random_ngram()

    @staticmethod
    def add_weights_temperature(input_weights, temperature):
        weights = np.where(input_weights == 0, 0, np.log(input_weights + 1e-10)) / temperature
        weights = np.exp(weights)
        return weights / np.sum(weights)

    @staticmethod
    def reverse_preprocess(text):
        text_reverse = re.sub(r'\s+([!?"\'().,;-])', r'\1', text)
        text_reverse = re.sub(' +', ' ', text_reverse)
        return text_reverse

    def return_next_word(self, prefix, temperature=1):
        prefix = self.check_prefix(prefix)
        prefix_ind = self.ngram2ind[prefix]
        weights = self.transition_matrix_prob[prefix_ind].toarray()[0]
        if temperature != 1:
            weights = self.add_weights_temperature(weights, temperature)

        token_ind = np.random.choice(range(len(weights)), p=weights)
        next_word = self.ind2token[token_ind]
        return next_word

    def generate_sequence(self, prefix, k, temperature=1):
        prefix = self.check_prefix(prefix)
        sequence = prefix.split(' ')

        for i in range(k):
            next_word = self.return_next_word(prefix, temperature=temperature)
            sequence.append(next_word)
            prefix = ' '.join(sequence[-self.n:])

        return self.reverse_preprocess(' '.join(sequence))

    def bulk_generate_sequence(self, prefix, k, samples, temperature=1):
        for i in range(samples):
            print(self.generate_sequence(prefix, k, temperature=temperature))
            print('\n')