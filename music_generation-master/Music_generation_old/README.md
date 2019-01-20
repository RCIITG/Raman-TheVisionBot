- Music Generation is done using LSTM (Long Short-Term Memory )network. 
- It uses basic one-hot encoding to represent extracted melodies as input to the LSTM. They are a type of Recurrent Neural Network that can efficiently learn via gradient descent. 
For that we have trained a model on midi files.
- ' 2018-03-08_181404_10.mid 'contains a already generated melody 

**Generate a melody**

BUNDLE_PATH=<absolute path of .mag file>

CONFIG=<one of 'basic_rnn', 'lookback_rnn', or 'attention_rnn', matching the bundle>

melody_rnn_generate \
--config=${CONFIG} \
--bundle_file=${BUNDLE_PATH} \
--output_dir=/tmp/melody_rnn/generated \
--num_outputs=10 \
--num_steps=128 \
--primer_melody="[60, -2, 60, -2, 67, -2, 67, -2]"

This melody would prime the model with the first four notes of Twinkle Twinkle Little Star.


