

from celery import Celery
from celery.schedules import crontab
from celery.task import PeriodicTask,  periodic_task
from Kolesa import Avto, bus, spec_technics, truck

from Krisha import ParseKrisha, KrishaHouse, KrishaOffice, KrishaShop, Krishaplacement, KrishaBuildings, Krisha_uchastok, Krishafactory


app = Celery('tasks', broker='redis://localhost:6379/0')
#app = Celery('avto', broker='amqp://guest:guest@localhost:5672//')

'''
@periodic_task(run_every=crontab(minute='*/5'))
def test():
    print("Evey 1 minute")
'''

#---------------------------------------------------------------------------
#  AVTO
'''
@periodic_task(bind=False,run_every=crontab( ))
def every_monday_test2():
    print("test runs every minute")

@periodic_task(bind=False,run_every=crontab(minute='*/2' ))
def every_monday_test3():
    print("test runs every minute2")
'''

@periodic_task(bind=False,run_every=crontab(hour=10, minute=45, day_of_week=1))
def every_monday_test():
    print("test runs every Monday morning at 7:31a.m.")


@periodic_task(bind=False,run_every=crontab(hour=8, minute=0, day_of_week=2)) #
def every_monday_bus():
    print("bus runs every Monday morning at 7:31a.m.")
    bus.bus_start()


@periodic_task(bind=False,run_every=crontab( hour=8, minute=31,day_of_week=2))
def every_monday_Avto():
    print("AVTO runs every Monday morning at 7:30a.m.")
    Avto.avto_start()




#-------------------------------------------------------------------
#     KRISHA


@periodic_task(bind=False,run_every=crontab(hour=12, minute=0, day_of_week=1))
def every_monday_ParseKrisha():
    print("apartments runs every Monday morning at 7:33a.m.")
    ParseKrisha.apartments()

@periodic_task(bind=False,run_every=crontab(hour=12, minute=1, day_of_week=1))
def every_monday_Krishafactory():
    print("factory runs every Monday morning at 7:33a.m.")
    Krishafactory.factory()

@periodic_task(bind=False,run_every=crontab(hour=12, minute=2, day_of_week=1))
def every_monday_Krisha_uchastok():
    print("uchastok runs every Monday morning at 7:33a.m.")
    Krisha_uchastok.uchastok()




