from miditok import REMI, TokenizerConfig
batch_size = 64
lr = 0.0001
d_model = 512
d_ff = 2048
n_layers = 6
heads = 8
dropout_rate = 0.2
n_epochs = 60
PAD_ID = 0
device = "mps"
# device = "cuda:0"
print_interval = 100
max_len = 750
data_split_rate = 0.99
len_Dataset = {'Drum': 18621,
               'Bass': 14316,
               'Guitar': 20037,
               'Piano': 11684}
TOKENIZER_PARAMS = {
    "pitch_range": (21, 109),
    "beat_res": {(0, 4): 8, (4, 12): 4},
    "num_velocities": 32,
    "special_tokens": ["PAD", "BOS", "EOS"],
    "use_chords": True,
    "use_rests": False,
    "use_tempos": True,
    "use_programs": True,
    "num_tempos": 191,
    "tempo_range": (60, 250),
    "program_changes": True,
    "programs": [-1, 0, 24, 27, 30, 33, 36],
}
config = TokenizerConfig(**TOKENIZER_PARAMS)

# Creates the tokenizer
tokenizer = REMI(config)

word2idx = tokenizer.vocab
idx2word = {idx: word for idx, word in enumerate(word2idx)}
vocab_len = len(word2idx)
