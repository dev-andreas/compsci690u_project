from logger import Logger
from task import Task
import configuration
import matplotlib.pyplot as plt

import json

class EvaluationTask(Task):
    def run(self):
        Logger.log("Evaluating results...")
        arch_ground_truth, euk_ground_truth = EvaluationTask.load_ground_truth()

        arch_outputs = {}
        euk_outputs = {}

        for sub_matrix in configuration.SUBSTITUTION_MATRICES:
            arch_outputs[sub_matrix] = []
            euk_outputs[sub_matrix] = []
            for word_size in configuration.WORD_SIZES:
                arch_output, euk_output = EvaluationTask.load_output(sub_matrix, word_size)

                arch_map_at_5 = EvaluationTask.mean_average_precision_at_k(arch_ground_truth, arch_output, 5)
                euk_map_at_5 = EvaluationTask.mean_average_precision_at_k(euk_ground_truth, euk_output, 5)

                arch_outputs[sub_matrix].append(arch_map_at_5)
                euk_outputs[sub_matrix].append(euk_map_at_5)

        print(f"Archaea MAP@5: {arch_outputs}")
        print(f"Eukaryote MAP@5: {euk_outputs}")

        for label, y in arch_outputs.items():
            plt.plot(configuration.WORD_SIZES, y, label=label)

        # Add labels and legend
        plt.xlabel('Word Size')
        plt.ylabel('MAP@5')
        plt.title('Archaea Retrieval Results')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

        for label, y in euk_outputs.items():
            plt.plot(configuration.WORD_SIZES, y, label=label)

        # Add labels and legend
        plt.xlabel('Word Size')
        plt.ylabel('MAP@5')
        plt.title('Eukaryote Retrieval Results')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()


    @staticmethod
    def precision_at_k(actual, predicted, k):
        predicted_at_k = predicted[:k]

        tp = 0
        for prediction in predicted_at_k:
            if prediction["seqid"] in actual:
                tp += 1
        
        return tp / len(predicted_at_k)

    @staticmethod
    def average_precision_at_k(actual, predicted, k):
        precision_at_k_acc = 0
        adjusted_k = min(k, len(predicted))
        for i in range(adjusted_k):
            precision_at_k_acc += EvaluationTask.precision_at_k(actual, predicted, i+1)

        return precision_at_k_acc / adjusted_k

    @staticmethod
    def mean_average_precision_at_k(ground_truth, results, k):
        average_precision_at_k_acc = 0

        for seqid in results:
            average_precision_at_k_acc += EvaluationTask.average_precision_at_k(ground_truth[seqid], results[seqid], k)

        return average_precision_at_k_acc / len(results)

    @staticmethod
    def load_output(sub_matrix, word_size):
        archaea_blast_output_file = open(f"results/archaea_{sub_matrix}_{word_size}.json", "r")
        arch_blast_output = json.load(archaea_blast_output_file)
        archaea_blast_output_file.close()

        eukaryote_blast_output_file = open(f"results/eukaryote_{sub_matrix}_{word_size}.json", "r")
        euk_blast_output = json.load(eukaryote_blast_output_file)
        eukaryote_blast_output_file.close()

        return arch_blast_output, euk_blast_output
    
    @staticmethod
    def load_ground_truth():
        archaea_ground_truth_file = open(configuration.ARCH_GROUND_TRUTH_FILENAME, "r")
        arch_ground_truth = json.load(archaea_ground_truth_file)
        archaea_ground_truth_file.close()

        eukaryote_ground_truth_file = open(configuration.EUK_GROUND_TRUTH_FILENAME, "r")
        euk_ground_truth = json.load(eukaryote_ground_truth_file)
        eukaryote_ground_truth_file.close()

        return arch_ground_truth, euk_ground_truth

##############
# test cases #
##############
if __name__ == "__main__":

    a1 = [1,2,3,4]
    p1 = [{'seqid': 1}, {'seqid': 2}, {'seqid': 3}, {'seqid': 4}]

    a2 = [1,2,3,4]
    p2 = [{'seqid': 5}, {'seqid': 6}, {'seqid': 7}, {'seqid': 8}]

    a3 = [1,2,3,4]
    p3 = [{'seqid': 3}, {'seqid': 4}, {'seqid': 5}, {'seqid': 6}]

    a4 = [1,2]
    p4 = [{'seqid': 2}, {'seqid': 3}]
    

    def test_precision_at_k():
        assert EvaluationTask.precision_at_k(a1,p1,1) == 1
        assert EvaluationTask.precision_at_k(a1,p1,2) == 1
        assert EvaluationTask.precision_at_k(a1,p1,3) == 1
        assert EvaluationTask.precision_at_k(a1,p1,4) == 1

        assert EvaluationTask.precision_at_k(a2,p2,1) == 0
        assert EvaluationTask.precision_at_k(a2,p2,2) == 0
        assert EvaluationTask.precision_at_k(a2,p2,3) == 0
        assert EvaluationTask.precision_at_k(a2,p2,4) == 0

        assert EvaluationTask.precision_at_k(a3,p3,1) == 1
        assert EvaluationTask.precision_at_k(a3,p3,2) == 1
        assert EvaluationTask.precision_at_k(a3,p3,3) == 2/3
        assert EvaluationTask.precision_at_k(a3,p3,4) == 1/2

        assert EvaluationTask.precision_at_k(a4,p4,1) == 1
        assert EvaluationTask.precision_at_k(a4,p4,2) == 1/2
        assert EvaluationTask.precision_at_k(a4,p4,3) == 1/2
        assert EvaluationTask.precision_at_k(a4,p4,4) == 1/2

    def test_average_precision_at_k():
        assert EvaluationTask.average_precision_at_k(a1,p1,1) == 1
        assert EvaluationTask.average_precision_at_k(a1,p1,2) == 1
        assert EvaluationTask.average_precision_at_k(a1,p1,3) == 1
        assert EvaluationTask.average_precision_at_k(a1,p1,4) == 1

        assert EvaluationTask.average_precision_at_k(a2,p2,1) == 0
        assert EvaluationTask.average_precision_at_k(a2,p2,2) == 0
        assert EvaluationTask.average_precision_at_k(a2,p2,3) == 0
        assert EvaluationTask.average_precision_at_k(a2,p2,4) == 0

        assert EvaluationTask.average_precision_at_k(a3,p3,1) == 1
        assert EvaluationTask.average_precision_at_k(a3,p3,2) == 1
        assert EvaluationTask.average_precision_at_k(a3,p3,3) == 8/9
        assert EvaluationTask.average_precision_at_k(a3,p3,4) == 19/24

        assert EvaluationTask.average_precision_at_k(a4,p4,1) == 1
        assert EvaluationTask.average_precision_at_k(a4,p4,2) == 3/4
        assert EvaluationTask.average_precision_at_k(a4,p4,3) == 3/4
        assert EvaluationTask.average_precision_at_k(a4,p4,4) == 3/4

    def test_mean_average_precision_at_k():
        ground_truth = {'a': a1, 'b': a2, 'c': a3, 'd': a4}
        results = {'a': p1, 'b': p2, 'c': p3, 'd': p4}

        assert EvaluationTask.mean_average_precision_at_k(ground_truth,results,1) == 3/4
        assert EvaluationTask.mean_average_precision_at_k(ground_truth,results,2) == 11/16
        assert EvaluationTask.mean_average_precision_at_k(ground_truth,results,3) == 95/144
        assert EvaluationTask.mean_average_precision_at_k(ground_truth,results,4) == 61/96

    test_precision_at_k()
    test_average_precision_at_k()
    test_mean_average_precision_at_k()