from io import Job

import JobSchedulerService


class JobSchedulerServiceImpl(JobSchedulerService):
    def shortestJobFirst(threadNo,job):
        print("Shortest Job First : ")
        jobs = job
        jobs.sort()
        threads = {}
        
