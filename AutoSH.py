from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

def Autotask1():

sched.add_job(Autotask1, "cron",hour='12' )
sched.start()