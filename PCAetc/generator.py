import pandas as pd
import random as rnd
from tqdm import tqdm

# List of around 1000 commonly used verbs, listed in rough order of usage rate
default_verbs = pd.read_csv('data/verbs_new.csv')

# List of around 1000 commonly used nouns, listed in rough order of usage rate
default_nouns = pd.read_csv('data/nouns_new.csv')


# Scrambles sentences
def scramble(sentence: str) -> str:
    words = sentence.split()
    rnd.shuffle(words)
    return ' '.join(words)


# We generate active sentences of the form
# "the " + noun1 + present tense verb + " the " + noun2
# e.g. "the dog chases the car"
# And passive sentences of the form
# "the " + noun2 + " is being " past participle verb + " by the " + noun1
# e.g. "the car is being chased by the dog"

# Produces n active passive sentence pairs in the format given above by randomly selecting 2 nouns (singular) and a verb (present).
# Optionally, we can include reverse of the noun pairs, or include scrambled versions of the sentences.
def act_pass_gen(n: int,
                 nouns: pd.DataFrame = default_nouns,
                 verbs: pd.DataFrame = default_verbs,
                 reverse: bool = True,
                 scramble: bool = True,
                 save_csv: str = None,
                 seed: int = 1) -> pd.DataFrame:
    rnd.seed(seed)
    N = len(nouns.index)
    V = len(verbs.index)
    sentence_list = []
    for _ in tqdm(range(n)):
        n1 = rnd.randrange(N)
        n2 = rnd.randrange(N)
        v = rnd.randrange(V)
        active = f"the {nouns.at[n1, 'Word']} {verbs.at[v, '3singular']} the {nouns.at[n2, 'Word']}"
        passive = f"the {nouns.at[n2, 'Word']} is being {verbs.at[v, 'Past Participle']} by the {nouns.at[n1, 'Word']}"
        if reverse:
            rev_active = f"the {nouns.at[n2, 'Word']} {verbs.at[v, '3singular']} the {nouns.at[n1, 'Word']}"
            rev_passive = f"the {nouns.at[n1, 'Word']} is being {verbs.at[v, 'Past Participle']} by the {nouns.at[n2, 'Word']}"
            if scramble:
                scr_active = scramble(active)
                scr_passive = scramble(passive)
                sentence_list.append([active, passive, rev_active, rev_passive, scr_active, scr_passive])
            else:
                sentence_list.append([active, passive, rev_active, rev_passive])
        else:
            if scramble:
                scr_active = scramble(active)
                scr_passive = scramble(passive)
                sentence_list.append([active, passive, scr_active, scr_passive])
            else:
                sentence_list.append([active, passive])
    if reverse:
        if scramble:
            df = pd.DataFrame(sentence_list,
                              columns=['Active', 'Passive', 'Active Reversed', 'Passive Reversed', 'Active scrambled',
                                       'Passive scrambled'])
        else:
            df = pd.DataFrame(sentence_list, columns=['Active', 'Passive', 'Active Reversed', 'Passive Reversed'])
    else:
        if scramble:
            df = pd.DataFrame(sentence_list, columns=['Active', 'Passive', 'Active scrambled', 'Passive scrambled'])
        else:
            df = pd.DataFrame(sentence_list, columns=['Active', 'Passive'])

    if save_csv is not None:
        df.to_csv(save_csv)

    return df


if __name__ == '__main__':
    print(act_pass_gen(10000, scramble=False, save_csv='data/simple_example_sentences.csv'))