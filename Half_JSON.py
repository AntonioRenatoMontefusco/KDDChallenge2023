import json

def split_json_dataset(filename):
    with open(filename, 'r') as file:
        data = json.load(file)

    total_records = len(data)
    half_records = total_records // 2

    first_half = data[:half_records]
    second_half = data[half_records:]

    with open('Output/first_half.json', 'w') as file:
        json.dump(first_half, file, indent=4)

    with open('Output/second_half.json', 'w') as file:
        json.dump(second_half, file, indent=4)

    print(f"Dataset diviso in due file: 'first_half.json' e 'second_half.json'.")

def count_json_array_elements(filename):
    with open(filename, 'r') as file:
        data = json.load(file)

    if isinstance(data, list):
        num_elements = len(data)
        print(f"Il file '{filename}' contiene {num_elements} elementi.")
    else:
        print("Il file non contiene un array JSON.")



# Esempio di utilizzo
count_json_array_elements('Output/second_half.json')