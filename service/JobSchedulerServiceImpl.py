from ion import Job, EDF
from functools import cmp_to_key


class JobSchedulerServiceImpl():
    def assignThreadsToJobs(self, threadNo, job):
        threads = dict()
        jobNames = list()
        thread = 0
        for j in job:
            if ((thread % threadNo) not in threads):
                jobNames = list()
                jobNames.append(j.getJobName())
                threads[thread % threadNo] = jobNames
            else:
                jobNames = threads[thread % threadNo]
                jobNames.append(j.getJobName())
            thread += 1
        return threads

    def displayScheduledJobs(self, threads):
        for entry in threads:

            print("Thread : {} - ".format(entry), end="")
            for name in threads[entry]:
                print(name, end=" ")
            print()

    def shortestJobFirst(self, threadNo, job):
        def comparator(j1, j2):
            if j1.getDuration() == j2.getDuration():
                return j1.getPriority()-j2.getPriority()
            return j1.getDuration()-j2.getDuration()
        print("Shortest Job First : ")
        jobs = job
        jobs.sort(key=cmp_to_key(comparator))
        threads = self.assignThreadsToJobs(threadNo, jobs)
        self.displayScheduledJobs(threads)

    def firstComeFirstServe(self, threadNo, job):
        print("FCFS")
        threads = self.assignThreadsToJobs(threadNo, job)
        self.displayScheduledJobs(threads)

    def fixedPriorityScheduling(self, threadNo, job):
        def comparator(j1, j2):
            if j1.getPriority() == j2.getPriority():
                if j1.getUserType() == j2.getUserType():
                    return int(j2.getDuration()-j1.getDuration())
                else:
                    return j1.getUserType()-j2.getUserType()
            return int(j1.getPriority()-j2.getPriority())
        print("FPS : ")
        jobs = job
        jobs.sort(key=cmp_to_key(comparator))
        threads = self.assignThreadsToJobs(threadNo, jobs)
        self.displayScheduledJobs(threads)

    def assignThreadsToJobsForEdf(self, threadNo, jobs):
        threads = dict()
        edf = None
        deadline = 0
        thread = 0
        for j in jobs:
            if ((thread % threadNo) not in threads):
                if j.getDuration() <= j.getDeadline():
                    edf = EDF.EDF()
                    edf.setJobNames(list())
                    edf.getJobNames().append(j.getJobName())
                    edf.setDeadline(j.getDuration())
                    threads[thread % threadNo] = edf
                    thread += 1
            else:
                edf = threads[thread % threadNo]
                if (edf.getDeadline()+j.getDuration() <= j.getDeadline()):
                    edf.setDeadline(edf.getDeadline()+j.getDuration())
                    edf.getJobNames().append(j.getJobName())
                    thread += 1
        return threads

    def displayScheduledJobsForEdf(self, threads):
        # print(threads)
        for entry in threads:
            print("Threads : {} - ".format(entry), end="")
            for name in threads[entry].getJobNames():
                print(name, end=" ")
            print()

    def earliestDeadlineFirst(self, threadNo, job):
        print("EDF : ")
        jobs = job

        def comparator(j1, j2):
            if j1.getDeadline() == j2.getDeadline():
                if j1.getPriority() == j2.getPriority():
                    return int(j1.getDuration()-j2.getDuration())
                else:
                    return j1.getPriority()-j2.getPriority()
            else:
                return int(j1.getDeadline()-j2.getDeadline())

        jobs.sort(key=cmp_to_key(comparator))
        threads = self.assignThreadsToJobsForEdf(threadNo, jobs)
        self.displayScheduledJobsForEdf(threads)
