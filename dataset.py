from logger import Logger
from task import Task
import configuration

from datasets import load_dataset
import subprocess

class CreateDatasetTask(Task):
    '''
    This class downloads the necessary datasets from Hugging Face Hub, creates fasta files, and generates the BLAST database.
    '''

    def run(self):
        Logger.log("Generating datasets...")

        ###################
        # archaea dataset #
        ###################

        Logger.small_log("Downloading arch_retrieval dataset...")
        arch_ds = load_dataset("tattabio/arch_retrieval")

        arch_corpus_ds = arch_ds["train"]
        arch_query_ds = arch_ds["test"]
        Logger.log(f"arch corpus size: {len(arch_corpus_ds)}")
        Logger.log(f"arch query size: {len(arch_query_ds)}")

        Logger.small_log("Creating archaea fasta files...")
        CreateDatasetTask.create_fasta_file_from_dataset(arch_corpus_ds, configuration.ARCH_CORPUS_FILENAME)
        CreateDatasetTask.create_fasta_file_from_dataset(arch_query_ds, configuration.ARCH_QUERY_FILENAME)
        
        Logger.small_log("Creating archaea database...")
        CreateDatasetTask.makeblastdb(configuration.ARCH_CORPUS_FILENAME, configuration.ARCH_BLASTDB_DIR)

        #####################
        # eukaryote dataset #
        #####################

        Logger.small_log("Downloading euk_retrieval dataset...")
        euk_ds = load_dataset("tattabio/euk_retrieval")

        euk_corpus_ds = euk_ds["train"]
        euk_query_ds = euk_ds["test"]
        Logger.log(f"euk corpus size: {len(euk_corpus_ds)}")
        Logger.log(f"euk query size: {len(euk_query_ds)}")

        Logger.small_log("Creating eukaryote fasta files...")
        CreateDatasetTask.create_fasta_file_from_dataset(euk_corpus_ds, configuration.EUK_CORPUS_FILENAME)
        CreateDatasetTask.create_fasta_file_from_dataset(euk_query_ds, configuration.EUK_QUERY_FILENAME)

        Logger.small_log("Creating eukaryote database...")
        CreateDatasetTask.makeblastdb(configuration.EUK_CORPUS_FILENAME, configuration.EUK_BLASTDB_DIR)

    @staticmethod
    def create_fasta_file_from_dataset(dataset, filename):
        '''
        Creates the fasta file from dataset.
        '''
        f = open(filename, "w")
        for entry in dataset:
            f.write(f">{entry['Entry']} [name={entry['Protein names']}]\n{entry['Sequence']}\n")
        f.close()

    @staticmethod
    def makeblastdb(fasta_filename, database_dir):
        '''
        Creates the blast database from fasta files.
        '''
        subprocess.run(["makeblastdb", "-dbtype", "prot", "-in", fasta_filename, "-out", database_dir])