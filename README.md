# RaySearch Search Engine

A simple information retrieval system that indexes and searches through the CACM (Communications of the ACM) document collection using TF-IDF and cosine similarity, with a simple GUI to make it user-friendly on the file interface_graphique_recherche.py

## Features

- **Document Indexing**: Automatically processes and indexes documents from the CACM collection
- **Inverted Index**: Builds an efficient inverted index for fast retrieval
- **Text Processing**: Includes tokenization, stemming (Porter stemmer), and stop words filtering
- **TF-IDF Weighting**: Implements Term Frequency-Inverse Document Frequency for document ranking
- **Cosine Similarity**: Ranks documents based on vector space model similarity
- **Graphical Interface**: User-friendly GUI for searching and viewing results

## Project Structure

```
├── data_to_modify.py                     # File path, you have to update it to match your local setup
├── indexer_gendico.py                    # Vocabulary generation
├── indexer_genindex.py                   # Inverted index generation
├── recherche.py                          # Search engine core
├── interface_graphique_recherche.py      # Search GUI
├── interface_graphique_dictionnaire_inversé.py  # Dictionary viewer GUI
├── Voc.json                              # Generated vocabulary
├── Index_Inversee.json                   # Generated inverted index
├── dictionnaire_normes.json              # Document norms
├── fetch.txt                             # Stop words list
└── cacm/                                 # CACM document collection
```

## Requirements

- Python 3.x
- NLTK (Natural Language Toolkit)
- tkinter (for GUI)
- matplotlib

```bash
pip install nltk matplotlib
```

## Setup

1. **Configure paths**: Update the file paths in the Python scripts to match your local setup on the data_to_modify.py path.

2. **Generate the vocabulary**:
   ```bash
   python indexer_gendico.py
   ```

3. **Generate the inverted index**:
   ```bash
   python indexer_genindex.py
   ```

## Usage

### Search Interface

Launch the graphical search interface:
```bash
python interface_graphique_recherche.py
```

Enter your search query and the system will return ranked documents based on relevance.

### Dictionary Viewer

View the inverted index:
```bash
python interface_graphique_dictionnaire_inversé.py
```

## How It Works

1. **Indexing Phase**:
   - Documents are tokenized and converted to lowercase
   - Stop words are filtered out
   - Terms are stemmed using Porter stemmer
   - TF-IDF weights are calculated
   - An inverted index is built mapping terms to documents

2. **Search Phase**:
   - Query is processed using the same pipeline as documents
   - Query vector is created with TF-IDF weights
   - Cosine similarity is calculated between query and each document
   - Results are ranked by similarity score

## Author

Rayane LABZIZI and Philippe Mulhem (Original framework)

## License

Educational project
