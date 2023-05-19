import numpy as np
import tiktoken

def encode_file(input_file_path, output_file_path, tokenizer_name):
    tokenizer = tiktoken.get_encoding(tokenizer_name)
    with open(input_file_path, 'r') as f:
        data = f.read()
    enc_data = tokenizer.encode(data)
    enc_data = np.array(enc_data, dtype=np.uint32)
    enc_data.tofile(output_file_path)

encode_file('output/val.csv', 'output/val.bin', 'cl100k_base')
