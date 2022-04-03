# sentence-arithmetic

## Data generation:

1. Put .txt files in data/raw (can be in subfolders)

2. Run data/generate_dataset.py

3. New active/sentence pairs will be appended to data/processed/active_passive.tsv

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
   