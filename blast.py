from logger import Logger
from task import Task
import configuration

import subprocess
import json

class RunBlastTask(Task):
    '''
    This class runs the blastp command and stores the results in a text file.
    '''


    def run(self):
        Logger.log("Running Blast...")

        for sub_matrix in configuration.SUBSTITUTION_MATRICES:
            for word_size in configuration.WORD_SIZES:

                #################
                # archaea blast #
                #################

                Logger.small_log(f"Searching archaea database ({sub_matrix}, {word_size})...")
                RunBlastTask.blastp(configuration.ARCH_QUERY_FILENAME, configuration.ARCH_BLASTDB_DIR, f"results/archaea_{sub_matrix}_{word_size}.txt", sub_matrix, word_size)
                Logger.small_log(f"Searching eukaryote database ({sub_matrix}, {word_size})...")
                RunBlastTask.blastp(configuration.EUK_QUERY_FILENAME, configuration.EUK_BLASTDB_DIR, f"results/eukaryote_{sub_matrix}_{word_size}.txt", sub_matrix, word_size)

                ###################
                # eukaryote blast #
                ###################

                Logger.small_log(f"Writing archaea blast results to JSON file ({sub_matrix}, {word_size})...")
                RunBlastTask.blast_to_json(f"results/archaea_{sub_matrix}_{word_size}.txt", f"results/archaea_{sub_matrix}_{word_size}.json")
                Logger.small_log(f"Writing eukaryote blast results to JSON file ({sub_matrix}, {word_size})...")
                RunBlastTask.blast_to_json(f"results/eukaryote_{sub_matrix}_{word_size}.txt", f"results/eukaryote_{sub_matrix}_{word_size}.json")

    @staticmethod
    def blastp(query_file, db_name, out_file, matrix="BLOSUM62", word_size=3):
        '''
        This method runs the blastp command
        '''
        subprocess.run(["blastp", "-query", query_file, "-db", db_name, "-out", out_file, "-matrix", matrix, "-word_size", str(word_size), "-outfmt", "6 qseqid sseqid bitscore"])

    @staticmethod
    def blast_to_json(blast_filename, json_filename):
        '''
        This method converts the blast output to a json file.
        '''
        f = open(blast_filename, "r")
        result = {}
        for line in f:
            line_args = line.strip().split("\t")
            if line_args[0] in result:
                result[line_args[0]].append({ "seqid": line_args[1], "bitscore": float(line_args[2])})
            else:
                result[line_args[0]] = [{ "seqid": line_args[1], "bitscore": float(line_args[2])}]
        f.close()
        
        # sort elements by bitscore
        for qseqid in result:
            result[qseqid].sort(key=lambda x: x["bitscore"], reverse=True)

        f = open(json_filename, "w")
        json.dump(result, f)
        f.close()
