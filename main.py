from dataset import CreateDatasetTask
from ground_truth import CreateGroundTruthTask
from blast import RunBlastTask
from evaluation import EvaluationTask
from logger import Logger

if __name__ == "__main__":
    task1 = CreateDatasetTask()
    task2 = CreateGroundTruthTask()
    task3 = RunBlastTask()
    task4 = EvaluationTask()
    
    task1.run()
    task2.run()
    task3.run()
    task4.run()

    Logger.log("Done.")
