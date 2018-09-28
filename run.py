from model.config import Config
from model.ner_model import NERModel

def do_run(runs=10, epochs=15, char_dim=100, glove_dim=300, lm_dim=None,
           glove_pretrained=True, lm_pretrained=True, glove_trainable=False,
           lm_trainable=False, log_suffix=None, lm_embeddings_filename=None):
    for run in range(runs):

        config = Config(epochs=epochs,
                        char_dim=char_dim,
                        glove_dim=glove_dim,
                        lm_dim=lm_dim,
                        glove_pretrained=glove_pretrained,
                        lm_pretrained=lm_pretrained,
                        glove_trainable=glove_trainable,
                        lm_trainable=lm_trainable,
                        run_number=run+1,
                        log_suffix=log_suffix,
                        lm_embeddings_file=lm_embeddings_filename)

        model = NERModel(config)

        model.train(train=config.dataset_train, dev=config.dataset_dev)

        model.restore_session(config.dir_model)
        model.evaluate(config.dataset_test)

        model.close_session()
        model.reset_session_graph()

# BASELINE: glove d300, init chars d100, crf
do_run(runs=6, epochs=20, log_suffix="baseline")

# baseline + train glove
do_run(runs=6, epochs=20, glove_trainable=True, log_suffix="train_glove")

# baseline + lm d50
do_run(runs=6, epochs=20, lm_dim=50)
do_run(lm_dim=50, epochs=20, lm_trainable=True)
do_run(lm_dim=50, epochs=20, lm_pretrained=False, lm_trainable=True)

# baseline + lm d100
do_run(runs=6, epochs=20, lm_dim=100)
do_run(lm_dim=100, epochs=20, lm_trainable=True)
do_run(lm_dim=100, epochs=20, lm_pretrained=False, lm_trainable=True)

# baseline + lm d200
do_run(runs=6, epochs=20, lm_dim=200)
do_run(lm_dim=200, epochs=20, lm_trainable=True)
do_run(lm_dim=200, epochs=20, lm_pretrained=False, lm_trainable=True)

# baseline + lm d300
do_run(runs=6, epochs=20, lm_dim=300)
do_run(lm_dim=300, epochs=20, lm_trainable=True)
do_run(lm_dim=300, epochs=20, lm_pretrained=False, lm_trainable=True)

# baseline + lm d1024
do_run(runs=6, epochs=20, lm_dim=1024)
do_run(lm_dim=1024, epochs=20, lm_trainable=True)
do_run(lm_dim=1024, epochs=20, lm_pretrained=False, lm_trainable=True)

# baseline + lm d1024 (NO PCA)
# do_run(runs=10, epochs=15, lm_dim=1024, log_suffix="no_pca", lm_embeddings_filename="data/lm1b_embeddings_d1024.npz")
do_run(runs=10, epochs=20, lm_dim=1024, log_suffix="no_pca", lm_embeddings_filename="data/lm1b_embeddings_d1024.npz", lm_trainable=True)

# -> take best dimension and run:
# with training enabled
# with training enabled and no pretrained lm embeddings
# with different hyperparameters:
# hidden lstm size
# 200, 300, 400, 500
# dropout
# learning rate
