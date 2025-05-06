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
    
    '''
    Running the BLAST retrieval takes a lot of time.
    Only uncomment the first three tasks if necessary!
    '''

    # task1.run()
    # task2.run()
    # task3.run()
    task4.run()

    Logger.log("Done.")
