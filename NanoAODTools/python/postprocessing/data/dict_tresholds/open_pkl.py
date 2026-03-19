import pickle as pkl

file_path =  'tresholds.pkl'

with open(file_path, 'rb') as f: 
    data = pkl.load(f)

print(data)