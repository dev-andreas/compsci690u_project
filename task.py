from abc import ABC, abstractmethod


class Task(ABC):
    @abstractmethod
    def run(self):
        """This is what needs to be run in the task"""
        pass