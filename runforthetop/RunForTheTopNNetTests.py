import io
import os
import shutil
import unittest

from runforthetop.RunForTheTopGame import RunForTheTopGame
from runforthetop.keras.RunForTheTopNNet import RunForTheTopNNet
from runforthetop.keras.NNet import NNetWrapper
from utils import dotdict


def get_model_summary(model):
    stream = io.StringIO()
    model.summary(print_fn=lambda x: stream.write(x + '\n'))
    summary_string = stream.getvalue()
    stream.close()
    return summary_string


ARGS = dotdict({
    'lr': 0.001,
    'dropout': 0.3,
    'epochs': 10,
    'batch_size': 64,
    'cuda': False,
    'num_channels': 512,
})


TEST_DATA_DIR = 'runforthetop/test-data/'


def get_saved_model(filename='RunForTheTopNNetTests_model_summary.txt'):
    with open(TEST_DATA_DIR + filename, 'r') as f:
        saved_model_summary = f.read()
    return saved_model_summary


def save_model_summary(model, filename='RunForTheTopNNetTests_model_summary.txt'):
    with open(TEST_DATA_DIR + filename, 'w') as f:
        f.write(get_model_summary(model))


class NNetTests(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_write_model_summary_to_file(self):
        net = RunForTheTopNNet(RunForTheTopGame(), ARGS)
        save_model_summary(net.model)

    def xtest_model_is_unchanged(self):
        model = RunForTheTopNNet(RunForTheTopGame(), ARGS).model
        self.assertEqual(get_saved_model(), get_model_summary(model))

    def test_save_and_restore_checkpoint(self):
        dirname = "/tmp/runforthetop"
        checkpoint_name = "foo.keras"
        summary_name = "temp.txt"
        self.ensure_empty(dirname)
        net = NNetWrapper(RunForTheTopGame())
        save_model_summary(net.nnet.model, summary_name)
        self.assertEqual(get_saved_model(summary_name), get_model_summary(net.nnet.model))
        net.save_checkpoint(dirname, checkpoint_name)
        self.assertTrue(os.path.exists(os.path.join(dirname, checkpoint_name)))
        net.load_checkpoint(dirname, checkpoint_name)
        self.assertEqual(get_saved_model(summary_name), get_model_summary(net.nnet.model))

    @staticmethod
    def ensure_empty(dir):
        shutil.rmtree(dir)
        os.makedirs(dir)

    def test_predict(self):
        game = RunForTheTopGame()
        state = game.getInitBoard()
        net = RunForTheTopNNet(game, ARGS)
        canonical_form = game.getCanonicalForm(state, 1)
        pi, v = net.predict(canonical_form)
        valids = game.getValidMoves(canonical_form, 1)
        self.Ps[s] = self.Ps[s] * valids  # masking invalid moves
        sum_Ps_s = np.sum(self.Ps[s])
        self.assertTrue(sum_Ps_s > 0)

