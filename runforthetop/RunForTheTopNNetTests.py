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


class NNetTests(unittest.TestCase):
    def xtest_write_model_summary(self):
        # write model summary to file
        game = RunForTheTopGame()
        net = RunForTheTopNNet(game, ARGS)
        with open('RunForTheTopNNetTests_model_summary.txt', 'w') as f:
            f.write(get_model_summary(net.model))

    def test_model_is_unchanged(self):
        # compare model summary to saved model summary
        with open(TEST_DATA_DIR + 'RunForTheTopNNetTests_model_summary.txt', 'r') as f:
            saved_model_summary = f.read()
            model = RunForTheTopNNet(RunForTheTopGame(), ARGS).model
            self.assertEqual(saved_model_summary, get_model_summary(model))

    def test_save_and_restore_checkpoint(self):
        dirname = "/tmp/runforthetop"
        filename = "foo.keras"
        self.ensure_empty(dirname)
        net = NNetWrapper(RunForTheTopGame())
        net.save_checkpoint(folder=dirname, filename=filename)
        self.assertTrue(os.path.exists(os.path.join(dirname, filename)))
        net.load_checkpoint(folder=dirname, filename=filename)

    @staticmethod
    def ensure_empty(dir):
        shutil.rmtree(dir)
        os.makedirs(dir)


