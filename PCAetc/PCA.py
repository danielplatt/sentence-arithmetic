import numpy as np
import pandas as pd
from tqdm import tqdm

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

npy= np.load("data/embedded_act_pass.npy")
aslst = npy.tolist()
 
def collapse_to_df():
    # Collapse outer list
    collapsed = []
    for i in aslst:
        for j in i:
            collapsed.append(j)
    return pd.DataFrame(collapsed)

def emb_to_PCA(df):
    df = StandardScaler().fit_transform(df)
    pca = PCA(n_components = 2)
    principalComponents = pca.fit_transform(df)
    principalDf = pd.DataFrame(data = principalComponents, columns = ['principal component 1', 'principal component 2'])

    # Adding a label column
    n = int(len(principalDf.index)/11)
    labels = ["Active", "Passive", "Active Reversed", "Passive Reversed", "Active scrambled", "Passive scrambled", "Act - Pass", "Act -ActRev", "Act - PassRev", "Act - ActScr", "Act - PassScr"]*n
    principalDf["Sentence type"] = labels

    return principalDf

def main():
    # Collapse to a pd
    df = collapse_to_df()
    # Export PCA to an csv
    a = emb_to_PCA(df)
    a.to_csv("data/act_pass_pca.csv")


if __name__ == "__main__":
    main()