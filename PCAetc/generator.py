import pandas as pd
import random as rnd
from tqdm import tqdm

def word_row_finder(word, words):
    word_initial = word[:1]
    for i in verbs.index:
        if words.at[i, 'Initial'] == word_initial:
            for j in verbs.columns:
                if word == words.at[i,j]:
                    return i

# We generate active sentences of the form 
# "the " + noun1 + present tense verb + " the " + noun2
# e.g. "the dog chases the car"
# And passive sentences of the form
# "the " + noun2 + " is being " past participle verb + " by the " + noun1
# e.g. "the car is being chased by the dog"
def scramble(sentence):
    words = sentence.split()
    rnd.shuffle(words)
    return ' '.join(words)

# Produces n active passive sentence pairs in the format given above by randomly selecting 2 nouns (singular) and a verb (present).
def act_pass_gen(n: int, nouns: pd.DataFrame, verbs: pd.DataFrame):
    rnd.seed(1)
    N = len(nouns.index)
    V = len(verbs.index)
    sen_list = []
    for _ in tqdm(range(n)):
        n1 = rnd.randrange(N)
        n2 = rnd.randrange(N)
        v = rnd.randrange(V)
        act = "the " + nouns.at[n1, 'Word'] + " " + verbs.at[v,'3singular'] + " the " + nouns.at[n2, 'Word']
        pas = "the " + nouns.at[n2, 'Word'] + " is being " + verbs.at[v,'Past Participle'] + " by the " + nouns.at[n1, 'Word']
        rev_act = "the " + nouns.at[n2, 'Word'] + " " + verbs.at[v,'3singular'] + " the " + nouns.at[n1, 'Word']
        rev_pas = "the " + nouns.at[n1, 'Word'] + " is being " + verbs.at[v,'Past Participle'] + " by the " + nouns.at[n2, 'Word']
        scr_act = scramble(act)
        scr_pas = scramble(pas)
        sen_list.append([act, pas, rev_act, rev_pas, scr_act, scr_pas])
    df = pd.DataFrame(sen_list, columns = ['Active', 'Passive', 'Active Reversed', 'Passive Reversed', 'Active scrambled', 'Passive scrambled'])
    return df

if __name__ == "__main__":
    # List of around 1000 commonly used verbs, listed in rough order of usage rate
    verbs = pd.read_csv('data/verbs_new.csv')
    
    # List of around 1000 commonly used nouns, listed in rough order of usage rate
    nouns = pd.read_csv('data/nouns_new.csv')

    act_pass_gen(100000, nouns, verbs).to_csv('data/act_pass_pairs.csv', index_label = 'index')