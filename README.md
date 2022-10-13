# sentence-arithmetic

## Download ready data

1. `active_passive_full.tsv`. 345877 active/passive sentence pairs: https://emckclac-my.sharepoint.com/:u:/g/personal/k2149901_kcl_ac_uk/EaUhddafyjxHju8xYigPisgBYFWNavQzZIhrkHnR2sOvXg?e=lmfuun

2. `active_passive_full_cleaned.tsv`. 345555 active/passive sentence pairs where pairs from the previous table have been removed if at least one of their sentences generates an error when attempting to embed it: https://emckclac-my.sharepoint.com/:u:/g/personal/k2149901_kcl_ac_uk/EbhMHe657_1ClOvUghbswPoBo_iXf-T4Tv4huxz7QKKAMQ?e=xwwgYR

3. `active_passive_embedding_full.npy`. A numpy array of size `(2, 345555, 768)` containing all sentence embeddings: https://emckclac-my.sharepoint.com/:u:/g/personal/k2149901_kcl_ac_uk/Ea56oqCJsxBGtS20i8vUQy4B9dna46wLh6dH-Q8k6yiWiQ?e=V6zSvF

4. `preprocessed_embeddings.csv`. Two-dimensional embeddings together with sentences prepared for the web visualisation: https://emckclac-my.sharepoint.com/:u:/g/personal/k2149901_kcl_ac_uk/EVY5mgGg71xAqHuqAZoLhB0B-W42a3a0FOv6G2_NM-KX_Q?e=5BIHnx

5. `PCA_basis.json`. The basis of the 2-dimensional subspace of 768-dimensional space used in the generation of preprocessed_embeddings.csv: https://emckclac-my.sharepoint.com/:u:/g/personal/k2149901_kcl_ac_uk/ERx7d8DPd8VHhjwMNLRmaQcBroEUg7nW8m1KxqscMQcovg?e=6bJLaV

## Data generation:

1. Run https://github.com/pgcorpus/gutenberg to download Gutenberg books. (At time of writing, aleph.gutenberg.org doesn't work, and I used gutenberg.pglaf.org::gutenberg instead.)
   
2. Put .txt files in data/raw (can be in subfolders)

3. Run data/generate_dataset.py

4. New active/sentence pairs will be appended to data/processed/active_passive_full.tsv

5. Run beautify_sentences.py which generates active_passive_full_beautiful.tsv. It removes notoriously poorly parsed sentences containing semicolons, parentheses, and quotation marks. Also converts to truecase.

6. Run embedding.py, which will create the embeddings saved in active_passive_embedding_full.npy and will create a list of sentence pairs active_passive_full_cleaned.tsv, which has removed pairs of which at least one sentence can't be embedded

## Data analysis on simple example sentences

1. Run generator.py

2. Run embedding.py

3. Do your own stuff with the sentence embeddings

## Active-passive simple sentences results (by Daniel)

1. Run generator.py, embedding.py to generate the necessary data
2. Run PCA_alternative.py, make sure that the line emb = get_sentence_embeddings('data/simple_example_sentences_embedding.npy')#[:,:10000,:] is not commented out. This loads the simple example sentences. This generates the images results/img/active_passive_simple_sentences_individual_arrows_visualisation.png and active_passive_simple_sentences_visualisation.png:
   ![Visualisation of active-passive sentences in dimension 2](results/img/active_passive_simple_sentences_visualisation.png)
   ![Visualisation of active-passive sentences with individual difference vectorsin dimension 2](results/img/active_passive_simple_sentences_individual_arrows_visualisation.png)
   
## Active-passive real life sentences results (by Daniel)

1. Unzip the file data/processed/active_passive.tsv.zip in the same folder
2. Run PCA_alternative.py, make sure that the line emb = get_sentence_embeddings('../data/processed/active_passive_embedding.npy')[:,:10000,:] is not commented out. This loads the real life example sentences. This generates the images results/img/active_passive_real_life_sentences_visualisation.png and active_passive_real_life_sentences_individual_arrows_visualisation.png:
   ![Visualisation of active-passive sentences in dimension 2](results/img/active_passive_real_life_sentences_visualisation.png)
   ![Visualisation of active-passive sentences with individual difference vectorsin dimension 2](results/img/active_passive_real_life_sentences_individual_arrows_visualisation.png)
   
## Testing if the (active sentence)-(passive sentence) is roughly the same for all sentences for real life sentences

1. Unzip the file `data/processed/active_passive.tsv.zip` in the same folder
2. Run `jumble_sentences.py` and make sure the line 
`jumble_file('processed/active_passive.tsv', 'processed/active_passive_jumbled.tsv', csv_separator='\t')`
   is not commented out. This generates `active_passive_jumbled.tsv`.
3. Run `embedding.py` and make sure the lines 
 `compute_active_passive_literature_embeddings()` and 
 `compute_active_passive_literature_jumbled_embeddings()`
are not commented out. This generates the files `active_passive_embedding.npy` and `active_passive_jumbled_embedding.npy`.
4. `Run nearest_embedding_experiment.py` and make sure the lines `    run_experiment_suite(
        '../data/processed/active_passive_embedding.npy',
        '../data/processed/active_passive_jumbled_embedding.npy',
        truncate=10000
    )` are not commented out. This generates the following output:
```
Experiment 1: Original passive-Original active
Now computing for how many sentences A_i+avgerage_diff is closest to B_i:
100%|██████████| 9977/9977 [43:43<00:00,  3.80it/s]
For 9945/9977 (99.68%) sentences A_i+avgerage_diff is closest to B_i.
------------------
Experiment 2: Original passive-Jumbled active
  0%|          | 0/9977 [00:00<?, ?it/s]Now computing for how many sentences A_i+avgerage_diff is closest to B_i:
100%|██████████| 9977/9977 [43:55<00:00,  3.79it/s]
For 9844/9977 (98.67%) sentences A_i+avgerage_diff is closest to B_i.
------------------
Experiment 3: Original passive-Jumbled passive
Now computing for how many sentences A_i+avgerage_diff is closest to B_i:
100%|██████████| 9977/9977 [43:42<00:00,  3.80it/s]
For 9886/9977 (99.09%) sentences A_i+avgerage_diff is closest to B_i.
```

Explanation of output:
in experiment 1, we have set {A1, A2, ..., A9977} of passive voice sentences and the set of {B1, B2, ..., B9977} of corresponding active voice sentences. I.e., A1 and B1 have the same meaning, just one is in active voice, one is in passive voice. average_diff is the average of B_i-A_i for i=1,...,9977. It is then checked if B1 is the sentence closest to the vector A1+average_diff, and if B2 is the sentence closest to the vector A2+average_diff, and similarly up to A9977+average_diff and B9977. This is the case for 9945/9977 of sentences. 

Experiments 2 and 3 are analogues of this, were the set {A1, A2, ..., A9977} is the same, but the set {B1, B2, ..., B9977} is different. In experiment 2, the latter set is jumbled active voice sentences, in experiment 3, the latter set is jumbled passive voice sentences.

Interpretation of results:
the success rate is highest if {B1, B2, ..., B9977} are the corresponding passive voice vectors. This is evidence for the fact that the average_diff does not just detect the removal of the word "by", but contains the a style difference of sentences.

## Testing (active sentence)-(passive sentence) for simple example sentences

1. Run `generator.py`. This generates the file `simple_example_sentences.csv`.
   
2. Run `jumble_sentences.py` and make sure the line 
`jumble_file(
        '../PCAetc/data/simple_example_sentences.csv',
        '../PCAetc/data/simple_example_sentences_jumbled.csv',
        csv_separator=',')`
   is not commented out. This generates the file `simple_example_sentences_jumbled.csv`.

3. Run `embedding.py` and make sure the lines     `compute_active_passive_literature_embeddings()` and `compute_active_passive_literature_jumbled_embeddings()` are not commented out. This generates the files `simple_example_sentences_embedding.npy` and `simple_example_sentences_jumbled_embedding.npy`.

4. Run `nearest_embedding_experiment.py` and make sure the lines `run_experiment_suite(
        'data/simple_example_sentences_embedding.npy',
        'data/simple_example_sentences_jumbled_embedding.npy',
        truncate=50000
    )`
   are not commented out. This generates the output:
```   
Experiment 1: Original passive-Original active
Now computing for how many sentences A_i+avgerage_diff is closest to B_i:
100%|██████████| 50000/50000 [18:33:57<00:00,  1.34s/it]
For 49493/50000 (98.99%) sentences A_i+avgerage_diff is closest to B_i.
------------------
Experiment 2: Original passive-Jumbled active
Now computing for how many sentences A_i+avgerage_diff is closest to B_i:
100%|██████████| 50000/50000 [19:43:14<00:00,  1.42s/it]
For 47440/50000 (94.88%) sentences A_i+avgerage_diff is closest to B_i.
------------------
Experiment 3: Original passive-Jumbled passive
Now computing for how many sentences A_i+avgerage_diff is closest to B_i:
100%|██████████| 50000/50000 [20:47:28<00:00,  1.50s/it]
For 48411/50000 (96.82%) sentences A_i+avgerage_diff is closest to B_i.
```
