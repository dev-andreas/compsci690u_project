# This file contains the configuration variables.

# corpus files
EUK_CORPUS_FILENAME = "datasets/euk_corpus.fasta"
ARCH_CORPUS_FILENAME = "datasets/arch_corpus.fasta"

# query files
EUK_QUERY_FILENAME = "datasets/euk_query.fasta"
ARCH_QUERY_FILENAME = "datasets/arch_query.fasta"

# blastdb directories
EUK_BLASTDB_DIR = "blast_databases/eukaryote"
ARCH_BLASTDB_DIR = "blast_databases/archaea"

# ground truth files
EUK_GROUND_TRUTH_FILENAME = "ground_truth/eukaryote_gt.json"
ARCH_GROUND_TRUTH_FILENAME = "ground_truth/archaea_gt.json"

# blast
SUBSTITUTION_MATRICES = ["PAM30", "PAM70", "PAM250", "BLOSUM45", "BLOSUM50", "BLOSUM62", "BLOSUM80", "BLOSUM90"]
WORD_SIZES = range(2,8)