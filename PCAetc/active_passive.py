import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm

from sklearn.decomposition import PCA

from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('all-mpnet-base-v2')

active_sentences = [
    'The man was eating the bread,',
    'The cat chased the mouse.',
    'A man is riding a horse.',
    'A string quartet is playing Mozart.',
    'Two gorillas fought over the last banana.',
    'A large ship blocked the Suez canal for weeks.',
    'The deer stared into the headlights.',
    'Tom was denied entry since he had lost his passport.',
    'Angela called the police after the altercation.',
    'The mathematician had drunk far too much coffee.'
    ]

passive_sentences = [
    'The bread was eaten by the man.',
    'The mouse was chased by the cat.',
    'The horse was being ridden by the man.',
    'Mozart is being played by the string quartet.',
    'The last banana was fought over by the the two gorillas.',
    'The Suez canal was blocked by a large ship for weeks.',
    'The headlights were stared into by a deer.',
    'Entry was denied to Tom since he had lost his passport.',
    'The police were called by Angela after the altercation.',
    'Far too much coffee had been drunk by the mathematician.'
    ]

differing_meaning = [
    'By the eaten man was the bread.',
    'The chased cat was by the mouse.',
    'By the horse was the ridden man.',
    'Mozart is playing a string quartet.',
    'The two bananas fight was over the last gorilla.',
    'By the Suez ship, the large canal was blocked for weeks.',
    'By the deer, the headlights stared.',
    'The lost passport was denied entry by Tom.',
    'Angela was called to the altercation by the police.',
    'The coffee had drunk far too much mathematician.'
]

unrelated_words = [
    'We hold these truths to be self-evident.',
    'It was the best of times, it was the worst of times.',
    'To be or not to be, that is the question.',
    'I have discovered a truly marvelous proof of this, which this margin is too narrow to contain.',
    'The bureaucracy is expanding to meet the needs of the expanding bureaucracy.',
    'Teach a man to fish, you feed him for a day',
    'It is one small step for man, one giant leap for mankind.',
    'Compound interest is the most powerful force in the universe.',
    'It is not the strongest of the species that survive, but the one most responsive to change.',
    'Any sufficiently advanced technology is indistinguishable from magic.'    
]

def get_embeddings(lst):
    embeddings_lst = []
    for sentence in lst:
        embeddings_lst.append(model.encode(sentence))
    return embeddings_lst

def list_average(lst):
    return sum(lst)/len(lst)

def pairwise_diff(emb_lst1,emb_lst2):
    return [a - b for a, b in zip(emb_lst1, emb_lst2)]

def average_pairwise_diff_cos_sim(emb_lst1,emb_lst2):
    lst_out = []
    for i, embi in enumerate(pairwise_diff(emb_lst1, emb_lst2)):
        for j, embj in enumerate(pairwise_diff(emb_lst1, emb_lst2)):
            if i > j:
                lst_out.append(util.cos_sim(embi, embj).item())
            else: 
                break
    return list_average(lst_out)

def main():        
    active_embedded = get_embeddings(active_sentences)
    passive_embedded = get_embeddings(passive_sentences)
    differing_embedded = get_embeddings(differing_meaning)
    unrelated_embedded = get_embeddings(unrelated_words)

    active_passive_sim = util.pairwise_cos_sim(active_embedded, passive_embedded).tolist()

    differing_passive_sim = util.pairwise_cos_sim(passive_embedded, differing_embedded).tolist() 

    differing_active_sim = util.pairwise_cos_sim(active_embedded, differing_embedded).tolist() 

    unrelated_active_sim = util.pairwise_cos_sim(active_embedded, unrelated_embedded).tolist() 

    cos_sim = pd.DataFrame({'active-passive': active_passive_sim,
                    'active-differing': differing_active_sim,
                    'passive-differing':  differing_passive_sim,
                    'unrelated-active': unrelated_active_sim
                    })

    cos_sim_av =  pd.Series({'active-passive': list_average(active_passive_sim),
                    'active-differing': list_average(differing_active_sim),
                    'passive-differing':  list_average(differing_passive_sim),
                    'unrelated-active': list_average(unrelated_active_sim)
                    })


    average_diff_cos_sim = pd.Series({'active-passive': average_pairwise_diff_cos_sim(active_embedded, passive_embedded),
                    'active-differing': average_pairwise_diff_cos_sim(passive_embedded, differing_embedded),
                    'passive-differing':  average_pairwise_diff_cos_sim(active_embedded, differing_embedded),
                    'unrelated-active': average_pairwise_diff_cos_sim(active_embedded, unrelated_embedded)
                    })

    cos_sim.plot.bar(rot=0, legend = False)
    plt.show()

    cos_sim_av.plot.bar(rot=0, legend = False)
    plt.show()

    average_diff_cos_sim.plot.bar(rot=0, legend = False)
    plt.show()

if __name__ == "__main__":
    main()
