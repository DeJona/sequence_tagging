import os
import sys

from model.conll_dataset import CoNLLDataset
from .data_utils import get_trimmed_glove_vectors, load_vocab, processing_chars_word_id, \
    processing_word_id
from .general_utils import get_logger


class Config:

    # general config
    dir_output = "results/test/"
    dir_model = dir_output + "model.weights/"
    path_log = dir_output + "log.txt"

    # embeddings
    dim_word = 300
    dim_char = 100

    # glove files
    filename_glove = "data/glove.6B/glove.6B.{}d.txt".format(dim_word)
    # trimmed embeddings (created from glove_filename with build_data.py)
    filename_trimmed = "data/glove.6B.{}d.trimmed.npz".format(dim_word)
    use_pretrained = True

    # dataset
    filename_dev = "data/germeval2014/NER-de-dev-CoNLL2003.txt"
    filename_test = "data/germeval2014/NER-de-test-CoNLL2003.txt"
    filename_train = "data/germeval2014/NER-de-train-CoNLL2003.txt"

    max_iter = sys.maxsize  # max number of examples in a dataset

    # vocab (created from dataset with build_data.py)
    filename_words = "data/words.txt"
    filename_tags = "data/tags.txt"
    filename_chars = "data/chars.txt"

    # training
    train_embeddings = False
    nepochs          = 15
    dropout          = 0.5
    batch_size       = 20
    lr_method        = "adam"
    lr               = 0.001
    lr_decay         = 0.9
    clip             = -1  # if negative, no clipping
    nepoch_no_imprv  = 3

    # model hyperparameters
    hidden_size_char = 100  # lstm on chars
    hidden_size_lstm = 300  # lstm on word embeddings

    # NOTE: if both chars and crf, only 1.6x slower on GPU
    use_crf = True      # if crf, training is 1.7x slower on CPU
    use_chars = True    # if char embedding, training is 3.5x slower on CPU

    def __init__(self, load=True):
        """Initialize hyperparameters and load vocabs

        Args:
            load_embeddings: (bool) if True, load embeddings into
                np array, else None

        """
        # directory for training outputs
        if not os.path.exists(self.dir_output):
            os.makedirs(self.dir_output)

        # create instance of logger
        self.logger = get_logger(self.path_log)

        # load if requested (default)
        if load:
            """Loads vocabulary, processing functions, embeddings and datasets

            Supposes that build_data.py has been run successfully and that
            the corresponding files have been created (vocab and trimmed GloVe
            vectors)

            """
            # 1. vocabulary
            self.vocab_chars = load_vocab(self.filename_chars)
            self.vocab_words = load_vocab(self.filename_words)
            self.vocab_tags  = load_vocab(self.filename_tags)

            # 2. get processing functions that map str -> id
            if self.use_chars:
                self.processing_word = processing_chars_word_id(self.vocab_chars, self.vocab_words, lowercase=True, allow_unk=True)
            else:
                self.processing_word = processing_word_id(self.vocab_words, lowercase=True, allow_unk=True)

            self.processing_tag = processing_word_id(self.vocab_tags, lowercase=False, allow_unk=False)

            # 3. get pre-trained embeddings
            self.embeddings = get_trimmed_glove_vectors(self.filename_trimmed) if self.use_pretrained else None

            # 4. get datasets
            self.dataset_dev = CoNLLDataset(self.filename_dev, self.processing_word, self.processing_tag, self.max_iter)
            self.dataset_train = CoNLLDataset(self.filename_train, self.processing_word, self.processing_tag, self.max_iter)
            self.dataset_test = CoNLLDataset(self.filename_test, self.processing_word, self.processing_tag, self.max_iter)
