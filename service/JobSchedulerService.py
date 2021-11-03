from abc import ABC, abstractmethod
from io import Job


class JobSchedulerService(ABC):

    @abstractmethod
    def shortestJobFirst(threadCount, job):
        pass

    @abstractmethod
    def firstComeFirstServe(threadCount, job):
        pass

    @abstractmethod
    def fixedPriorityScheduling(threadCount, job):
        pass

    @abstractmethod
    def earliestDeadlineFirst(threadCount, job):
        pass
