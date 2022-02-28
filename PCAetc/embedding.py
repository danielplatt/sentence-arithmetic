import pandas as pd
import numpy as np
from tqdm import tqdm


from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('all-mpnet-base-v2')

# Our sentences we'd like to encode
sentences = pd.read_csv('data/act_pass_pairs.csv')
sentences = sentences.drop(columns = ['index'])

# Change this value to whatever you want.
sentences = sentences.truncate(after = 9999)
sentences_list = sentences.values.tolist()

# Sentences are encoded by calling model.encode()
def create_embeddings():
    embeddings_list = []
    for sublist in tqdm(sentences_list):
        embeddings_sublist = []
        for sentence in sublist:
            embeddings_sublist.append(model.encode(sentence).tolist())
        for i,_ in enumerate(sublist[1:]):
            embeddings_sublist.append(np.add(embeddings_sublist[0], np.negative(embeddings_sublist[i+1])))
        embeddings_list.append(embeddings_sublist)
    return np.array(embeddings_list)



def main():  
    # Export embeddings to an npy
    a = create_embeddings()
    np.save('data/embedded_act_pass.npy', a)

if __name__ == "__main__":
    main()