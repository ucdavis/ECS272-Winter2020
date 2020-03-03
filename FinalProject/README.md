### NOTE: All embeddings need to be normalized, i.e., same length vectors (within each embedding method) and all elements of those vectors are in the range [0,1]. Functions that generate embeddings should be in their own module, take the whole dataframe as input, output the whole dataframe with a new column containing the generated embeddings. See the `pixel_embedding.py` module in the `embeddings` directory for an example

# Components and task breakdown

### Visualization
  - Collab View (scatter plot with clustering)
    - Chitrabhanu leads
  - Data Coverage Panel (tree map of dimensions)
    - Pouneh leads
  - Overall Dashboard
    - Jackson leads
  - Control Panels
    - Pouneh leads

### Preprocessing
  - Dataset of charts
    - even split
    - **Done ASAP**
  - Embedding of Images (via Frequency Information)
    - Matt leads
    - **Done ASAP, will use dummy pixel embedding in the meantime**
  - Embedding of Keywords and other strings (via `word2vec`)
    - Pouneh leads
    - **Done night of 3/4**
  - Dimensional Intersection Distance metric (via One-Hot Vectors)
    - Jackson leads
    - **Done night of 3/4**
  - Concatenating Embeddings w/ Different Weights
    - Chitrabhanu leads
    - **Done night of 3/4**
  - Clustering based on concatenated embeddings (via kmeans)
    - Matt leads
    - **Done by 3/9** 
  - Dimensionality Reduction (via PCA)
    - Matt leads
    - **Done by 3/9**

### Paperwork
  - Final Report
    - Jackson leads