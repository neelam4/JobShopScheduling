from ion import Job
from service import JobSchedulerServiceImpl


def main():
    print("JOB SCHEDULER")
    print()
    jobScheduler = JobSchedulerServiceImpl.JobSchedulerServiceImpl()
    # job1 = Job.Job("J1", 10, 0, 10, 1)
    # job2 = Job.Job("J2", 20, 0, 40, 1)
    # job3 = Job.Job("J3", 15, 2, 40, 2)
    # job4 = Job.Job("J4", 30, 1, 40, 2)
    # job5 = Job.Job("J5", 10, 2, 30, 2)
    # job6 = Job.Job("J6", 30, 2, 30, 2)
    jobs = list()
    job = Job.Job()
    no_machines = 1
    no_machines = int(input("Enter number of machine(s) :"))
    input_file_name = input("Select a '.txt' file : ")
    print()
    input_file = open(input_file_name,"r")
    for line in input_file:
        name,duration,priority,deadline,user_type = line.split(',')
        job = Job.Job()
        job.setDeadline(int(deadline))
        job.setJobName(name)
        job.setDuration(int(duration))
        job.setPriority(int(priority))
        job.setUserType(int(user_type))
        jobs.append(job)
    
    # jobs.append(job1)
    # jobs.append(job2)
    # jobs.append(job3)
    # jobs.append(job4)
    # jobs.append(job5)
    # jobs.append(job6)
    jobScheduler.firstComeFirstServe(no_machines, jobs)
    print()
    jobScheduler.shortestJobFirst(no_machines, jobs)
    print()
    jobScheduler.fixedPriorityScheduling(no_machines, jobs)
    print()
    jobScheduler.earliestDeadlineFirst(no_machines, jobs)


if __name__ == '__main__':
    main()
