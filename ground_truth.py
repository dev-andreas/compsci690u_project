from logger import Logger
from task import Task
import configuration

from datasets import load_dataset
import json

class CreateGroundTruthTask(Task):

    def run(self):
        Logger.log("Generating ground truth...")

        #################
        # archaea qrels #
        #################

        Logger.small_log("Downloading arch_retrieval_qrels dataset...")
        arch_qrels = load_dataset("tattabio/arch_retrieval_qrels")
        Logger.small_log("Creating JSON file...")
        CreateGroundTruthTask.qrels_to_json(arch_qrels["train"], configuration.ARCH_GROUND_TRUTH_FILENAME)


        ###################
        # eukaryote qrels #
        ###################

        Logger.small_log("Downloading euk_retrieval_qrels dataset...")
        euk_qrels = load_dataset("tattabio/euk_retrieval_qrels")
        Logger.small_log("Creating JSON file...")
        CreateGroundTruthTask.qrels_to_json(euk_qrels["train"], configuration.EUK_GROUND_TRUTH_FILENAME)

    @staticmethod
    def qrels_to_json(qrels, filename):
        result = {}
        for entry in qrels:
            if entry["query_id"] in result:
                result[entry["query_id"]].append(entry["corpus_id"])
            else:
                result[entry["query_id"]] = [entry["corpus_id"]]
        f = open(filename, "w")
        json.dump(result, f)
        f.close()