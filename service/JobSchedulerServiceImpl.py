from ion import Job, EDF
from functools import cmp_to_key

import matplotlib.pyplot as plt

class JobSchedulerServiceImpl():
    
    def assignThreadsToJobs(self, threadNo, job,f_name:str):
        # Declaring a figure "gnt"
        fig, gnt = plt.subplots()

        # Setting Y-axis limits
        gnt.set_ylim(0, 50)

        # Setting X-axis limits
        gnt.set_xlim(0, 100)
        gnt.set_xlabel('seconds since start')
        gnt.set_ylabel('Machine(s)')
        gnt.set_yticks([10,20,30,40,50])
        # Labelling tickes of y-axis
        gnt.set_yticklabels(['1', '2', '3','4','5'])
        # If you want grid on the plot use
        # gnt.grid(True)
        gnt.grid(False)

        threads = dict()
        jobNames = list()
        machine_thread = dict()
        for th in range(threadNo):
            machine_thread[th]=list()
            machine_thread[th].append(tuple((0,0)))
        
        thread = 0
        for j in job:
            if ((thread % threadNo) not in threads):
                jobNames = list()
                jobNames.append(j.getJobName())
                last_mac = machine_thread[thread%threadNo]
                l = tuple((last_mac[-1][-1]+last_mac[-1][0],j.getDuration()))
                machine_thread[thread%threadNo].append(l)
                threads[thread % threadNo] = jobNames
            else:
                jobNames = threads[thread % threadNo]
                jobNames.append(j.getJobName())
                last_mac = machine_thread[thread%threadNo]
                l = tuple((last_mac[-1][-1]+last_mac[-1][0],j.getDuration()))
                machine_thread[thread%threadNo].append(l)
            thread += 1
        for th in range(threadNo):
            machine_thread[th].pop(0)

        for th in range(threadNo):
            gnt.broken_barh(machine_thread[th],(10*th+6,8),facecolors=('indigo', 'blue','red'))

        plt.title(f_name)
        plt.show()

        return threads

    def displayScheduledJobs(self, threads):
        for entry in threads:

            print("Machine : {} - ".format(entry+1), end="")
            for name in threads[entry]:
                print(name, end=" ")
            print()
     
    def shortestJobFirst(self, threadNo:int, job):
        def comparator(j1, j2):
            if j1.getDuration() == j2.getDuration():
                return j1.getPriority()-j2.getPriority()
            return j1.getDuration()-j2.getDuration()
        print("Shortest Job First : ")
        jobs = job
        jobs.sort(key=cmp_to_key(comparator))
        threads = self.assignThreadsToJobs(threadNo, jobs,"Shortest Job First")
        self.displayScheduledJobs(threads)

    def firstComeFirstServe(self, threadNo:int, job):
        print("FCFS : ")
        jobs = job
        threads = self.assignThreadsToJobs(threadNo, jobs,"First Come First Serve")
        self.displayScheduledJobs(threads)

    def fixedPriorityScheduling(self, threadNo:int, job):
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
        threads = self.assignThreadsToJobs(threadNo, jobs,"Fixed Priority Scheduling")
        self.displayScheduledJobs(threads)

    def assignThreadsToJobsForEdf(self, threadNo:int, jobs,f_name:str):
        threads = dict()
        edf = EDF.EDF()

        # Declaring a figure "gnt"
        fig, gnt = plt.subplots()

        # Setting Y-axis limits
        gnt.set_ylim(0, 50)

        # Setting X-axis limits
        gnt.set_xlim(0, 100)
        gnt.set_xlabel('seconds since start')
        gnt.set_ylabel('Machine(s)')
        gnt.set_yticks([10,20,30,40,50])
        # Labelling tickes of y-axis
        gnt.set_yticklabels(['1', '2', '3','4','5'])
        gnt.grid(False)

        machine_thread = dict()
        for th in range(threadNo):
            machine_thread[th]=list()
            machine_thread[th].append(tuple((0,0)))

        thread = 0
        for j in jobs:
            if ((thread % threadNo) not in threads):
                if j.getDuration() <= j.getDeadline():
                    edf = EDF.EDF()
                    edf.setJobNames(list())
                    edf.getJobNames().append(j.getJobName())
                    edf.setDeadline(j.getDuration())
                    threads[thread % threadNo] = edf
                    last_mac = machine_thread[thread%threadNo]
                    l = tuple((last_mac[-1][-1]+last_mac[-1][0],j.getDuration()))
                    machine_thread[thread%threadNo].append(l)
                    thread += 1
            else:
                edf = threads[thread % threadNo]
                if (edf.getDeadline()+j.getDuration() <= j.getDeadline()):
                    edf.setDeadline(edf.getDeadline()+j.getDuration())
                    edf.getJobNames().append(j.getJobName())
                    last_mac = machine_thread[thread%threadNo]
                    l = tuple((last_mac[-1][-1]+last_mac[-1][0],j.getDuration()))
                    machine_thread[thread%threadNo].append(l)
                    thread += 1
        for th in range(threadNo):
            machine_thread[th].pop(0)

        for th in range(threadNo):
            gnt.broken_barh(machine_thread[th],(10*th+6,8),facecolors=('indigo', 'blue','red'))

        plt.title(f_name)
        plt.show()
        return threads

    def displayScheduledJobsForEdf(self, threads):
        for entry in threads:
            print("Machine : {} - ".format(entry+1), end="")
            for name in threads[entry].getJobNames():
                print(name, end=" ")
            print()
        
    def earliestDeadlineFirst(self, threadNo:int, job):
        print("EDF : ")
        jobs = job

        def comparator(j1, j2):
            if j1.getDeadline() == j2.getDeadline():
                if j1.getPriority() == j2.getPriority():
                    return int(j1.getDuration()-j2.getDuration())
                else:
                    return int(j1.getPriority()-j2.getPriority())
            else:
                return int(j1.getDeadline()-j2.getDeadline())
        
        jobs.sort(key=cmp_to_key(comparator))
        threads = self.assignThreadsToJobsForEdf(threadNo, jobs,"Earliest Deadline First")
        self.displayScheduledJobsForEdf(threads)
