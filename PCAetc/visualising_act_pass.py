import numpy as np
import pandas as pd
from tqdm import tqdm

import matplotlib.pyplot as plt

df = pd.read_csv('data/act_pass_pca.csv')
active = df[df["Sentence type"] == "Active"]
passive = df[df["Sentence type"] == "Passive"]
active_reversed = df[df["Sentence type"] == "Active Reversed"]
passive_reversed = df[df["Sentence type"] == "Passive Reversed"]
scrambled_active = df[df["Sentence type"] == "Active Scrambled"]
scrambled_passive = df[df["Sentence type"] == "Passive Scrambled"]
act_pass_diff = df[df["Sentence type"] == "Act - Pass"]
act_actrev_diff = df[df["Sentence type"] ==  "Act -ActRev"]
act_passrev_diff = df[df["Sentence type"] ==  "Act - PassRev"]
act_actscr_diff = df[df["Sentence type"] ==  "Act - ActScr"]
act_passscr_diff = df[df["Sentence type"] ==  "Act - PassScr"]

subframes = [active, passive, active_reversed, passive_reversed, scrambled_active, scrambled_passive, act_pass_diff, act_actrev_diff, act_actscr_diff, act_passscr_diff]
colours = ["red", "blue", "orange", "purple", "magenta", "cyan"]

def plot_PCA():
    for i, frame in enumerate(subframes):
        if i != 0 and i != 1:
            continue
        if i > 6:
            break
        x = frame["principal component 1"].to_numpy()
        y = frame["principal component 2"].to_numpy()
        plt.scatter(x, y, color = colours[i])
    plt.show()


def plot_differences():
    for i, frame in enumerate(subframes):
        if i == 0 or i == 1 or i == 6:
            x = frame["principal component 1"].to_numpy()
            y = frame["principal component 2"].to_numpy()
            plt.scatter(x, y)
    plt.show()

plot_differences()