import io
import unittest

from runforthetop.RunForTheTopGame import RunForTheTopGame
from runforthetop.keras.RunForTheTopNNet import RunForTheTopNNet
from utils import dotdict

MODEL_SUMMARY = """
Model: "model"
__________________________________________________________________________________________________
 Layer (type)                   Output Shape         Param #     Connected to
==================================================================================================
 input_1 (InputLayer)           [(None, 8, 8)]       0           []

 reshape (Reshape)              (None, 8, 8, 1)      0           ['input_1[0][0]']

 conv2d (Conv2D)                (None, 8, 8, 512)    4608        ['reshape[0][0]']

 batch_normalization (BatchNorm  (None, 8, 8, 512)   2048        ['conv2d[0][0]']
 alization)

 activation (Activation)        (None, 8, 8, 512)    0           ['batch_normalization[0][0]']

 conv2d_1 (Conv2D)              (None, 8, 8, 512)    2359296     ['activation[0][0]']

 batch_normalization_1 (BatchNo  (None, 8, 8, 512)   2048        ['conv2d_1[0][0]']
 rmalization)

 activation_1 (Activation)      (None, 8, 8, 512)    0           ['batch_normalization_1[0][0]']

 conv2d_2 (Conv2D)              (None, 6, 6, 512)    2359296     ['activation_1[0][0]']

 batch_normalization_2 (BatchNo  (None, 6, 6, 512)   2048        ['conv2d_2[0][0]']
 rmalization)

 activation_2 (Activation)      (None, 6, 6, 512)    0           ['batch_normalization_2[0][0]']

 conv2d_3 (Conv2D)              (None, 4, 4, 512)    2359296     ['activation_2[0][0]']

 batch_normalization_3 (BatchNo  (None, 4, 4, 512)   2048        ['conv2d_3[0][0]']
 rmalization)

 activation_3 (Activation)      (None, 4, 4, 512)    0           ['batch_normalization_3[0][0]']

 flatten (Flatten)              (None, 8192)         0           ['activation_3[0][0]']

 dense (Dense)                  (None, 1024)         8388608     ['flatten[0][0]']

 batch_normalization_4 (BatchNo  (None, 1024)        4096        ['dense[0][0]']
 rmalization)

 activation_4 (Activation)      (None, 1024)         0           ['batch_normalization_4[0][0]']

 dropout (Dropout)              (None, 1024)         0           ['activation_4[0][0]']

 dense_1 (Dense)                (None, 512)          524288      ['dropout[0][0]']

 batch_normalization_5 (BatchNo  (None, 512)         2048        ['dense_1[0][0]']
 rmalization)

 activation_5 (Activation)      (None, 512)          0           ['batch_normalization_5[0][0]']

 dropout_1 (Dropout)            (None, 512)          0           ['activation_5[0][0]']

 pi (Dense)                     (None, 4097)         2101761     ['dropout_1[0][0]']

 v (Dense)                      (None, 1)            513         ['dropout_1[0][0]']

==================================================================================================
Total params: 18,112,002
Trainable params: 18,104,834
Non-trainable params: 7,168
__________________________________________________________________________________________________
None
"""

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

class NNetTests(unittest.TestCase):
    def xtest_write_model_summary(self):
        # write model summary to file
        game = RunForTheTopGame()
        net = RunForTheTopNNet(game, ARGS)
        with open('RunForTheTopNNetTests_model_summary.txt', 'w') as f:
            f.write(get_model_summary(net.model))

    def test_model_is_unchanged(self):
        # compare model summary to saved model summary
        with open('RunForTheTopNNetTests_model_summary.txt', 'r') as f:
            saved_model_summary = f.read()
            model = RunForTheTopNNet(RunForTheTopGame(), ARGS).model
            self.assertEqual(saved_model_summary, get_model_summary(model))
