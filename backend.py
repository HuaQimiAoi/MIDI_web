from utils import merge_midi_tracks, generate_midi_v2
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from utils import upload_midi_file
from transformer import Transformer
from train_parameters import (max_len, d_model, d_ff, n_layers,
                              heads, dropout_rate, PAD_ID, tokenizer, vocab_len, device)
import os
import torch
app = Flask(__name__)

model_Drum = Transformer(src_vocab_size=vocab_len, dst_vocab_size=vocab_len, pad_idx=PAD_ID, d_model=d_model,
                         d_ff=d_ff, n_layers=n_layers, heads=heads, dropout=dropout_rate, max_seq_len=max_len)
model_Guitar = Transformer(src_vocab_size=vocab_len, dst_vocab_size=vocab_len, pad_idx=PAD_ID, d_model=d_model,
                           d_ff=d_ff, n_layers=n_layers, heads=heads, dropout=dropout_rate, max_seq_len=max_len)
model_Piano = Transformer(src_vocab_size=vocab_len, dst_vocab_size=vocab_len, pad_idx=PAD_ID, d_model=d_model,
                          d_ff=d_ff, n_layers=n_layers, heads=heads, dropout=dropout_rate, max_seq_len=max_len)
model_Bass = Transformer(src_vocab_size=vocab_len, dst_vocab_size=vocab_len, pad_idx=PAD_ID, d_model=d_model,
                         d_ff=d_ff, n_layers=n_layers, heads=heads, dropout=dropout_rate, max_seq_len=max_len)

model_Drum_path = "./models/model_Drum.pth"
model_Guitar_path = "./models/model_Guitar.pth"
model_Piano_path = "./models/model_Piano.pth"
model_Bass_path = "./models/model_Bass.pth"

model_Drum.load_state_dict(
    torch.load(
        model_Drum_path,
        map_location=torch.device(device)))
model_Bass.load_state_dict(
    torch.load(
        model_Bass_path,
        map_location=torch.device(device)))
model_Piano.load_state_dict(
    torch.load(
        model_Piano_path,
        map_location=torch.device(device)))
model_Guitar.load_state_dict(
    torch.load(
        model_Guitar_path,
        map_location=torch.device(device)))

token = "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"
repo = 'upload_MIDIs'
message = 'user_commit'
branch = "main"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files.get('file')

        # 创建一个 secure filename
        secure_f = secure_filename(f.filename)

        # 指定一个上传文件的路径
        upload_folder = './MIDIs'

        # 检查路径是否存在，如果不存在则创建
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        f.save(os.path.join(upload_folder, secure_f))
        local_file = f"{upload_folder}/{secure_f}"
        midi_url = upload_midi_file(
            token=token,
            repo=repo,
            local_file=local_file,
            message=message,
            branch=branch)
        return jsonify({
            'message': midi_url,
            'state': 'success'
        })


@app.route('/generate', methods=['GET', 'POST'])
def generate_midi():
    if request.method == 'POST':
        data = request.data.decode()
        src_midi = f"./MIDIs/{data}"
        generate_midi_v2(model=model_Drum, tokenizer=tokenizer, src_midi=src_midi, max_len=max_len, PAD_ID=PAD_ID,
                         tgt_midi="./MIDIs/Drum_track.mid")
        generate_midi_v2(model=model_Guitar, tokenizer=tokenizer, src_midi=src_midi, max_len=max_len, PAD_ID=PAD_ID,
                         tgt_midi="./MIDIs/Guitar_track.mid")
        generate_midi_v2(model=model_Piano, tokenizer=tokenizer, src_midi=src_midi, max_len=max_len, PAD_ID=PAD_ID,
                         tgt_midi="./MIDIs/Piano_track.mid")
        generate_midi_v2(model=model_Bass, tokenizer=tokenizer, src_midi=src_midi, max_len=max_len, PAD_ID=PAD_ID,
                         tgt_midi="./MIDIs/Bass_track.mid")
        merge_midi_tracks(src_midi, "./MIDIs/Drum_track.mid", "./MIDIs/Bass_track.mid",
                          "./MIDIs/Guitar_track.mid", "./MIDIs/Piano_track.mid",
                          tgt_dir="./MIDIs/generated_midi.mid")
        midi_url = upload_midi_file(
            token=token,
            repo=repo,
            local_file="./MIDIs/generated_midi.mid",
            message=message,
            branch=branch)
        return jsonify({
            'message': midi_url,
            'state': 'success'
        })


if __name__ == '__main__':
    app.run(port=5500, debug=True)
