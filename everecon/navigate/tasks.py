import datetime
from celery.schedules import crontab

from everecon import celery_app as app
from celery import task
import requests

from everecon.navigate.models import Kill

UUID = 'c598d921-3bc0-40ad-846d-bd6c24823b08'


@app.on_after_finalize.connect
def setup(sender, **kwargs):
    killboard_redisq.apply_async(countdown=10)
    sender.add_periodic_task(crontab(minute='*/5'), clear_kills.s())


@task
def clear_kills():
    time = datetime.datetime.now() - datetime.timedelta(minutes=60)
    Kill.objects.filter(time__lt=time).delete()

@task
def killboard_redisq():
    while True:
        r = requests.get('https://redisq.zkillboard.com/listen.php?queueID={}&ttw=1'.format(UUID))

        # todo: check statuscode
        try:
            kill = Kill.from_json(r.json())
        except ValueError as e:
            print(e)
            break

        if kill is None:
            print('package was empty.. exiting')
            break


        # Handle the data we received
        print(kill)
        kill.save()

    killboard_redisq.apply_async(countdown=30)
