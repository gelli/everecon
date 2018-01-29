import datetime
import json

import maya
from celery.schedules import crontab
from channels import Group
from django.db import IntegrityError

from everecon import celery_app as app
from celery import task
import requests

from everecon.navigate.models import Kill

UUID = 'c598d921-3bc0-40ad-846d-bd6c24823b08'


@app.on_after_finalize.connect
def setup(sender, **kwargs):
    killboard_redisq.apply_async(countdown=10)
    sender.add_periodic_task(crontab(minute='*/5'), clear_kills.s())


def get_character(character_id):
    url = 'https://esi.tech.ccp.is/v4/characters/{}/'
    r = requests.get(url.format(character_id))
    return r.json()


def get_names(ids: list):
    data = [x for x in ids if x is not None]
    url = 'https://esi.tech.ccp.is/latest/universe/names/'
    r = requests.post(url, json=data)
    return r.json()


@task
def clear_kills():
    time = datetime.datetime.now() - datetime.timedelta(minutes=60)
    Kill.objects.filter(time__lt=time).delete()

@task
def killboard_redisq():

    while True:

        try:
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

            print(kill)
            kill.save()

            names = get_names([kill.victim_character_id, kill.victim_corporation_id , kill.victim_alliance_id])

            print(names)

            victim_name = victim_corp = victim_alliance = None

            for name in names:

                if name['category'] == 'character':
                    victim_name = name['name']
                elif name['category'] == 'corporation':
                    victim_corp = name['name']
                elif name['category'] == 'alliance':
                    victim_alliance = name['name']

            if maya.now().subtract(minutes=5).datetime() < kill.time:
                print('sending kill to websocket')
                Group('users').send({
                    'text': json.dumps({
                        'id': kill.kill_id,
                        'time': str(kill.time),
                        'location': kill.location.name,
                        'system': kill.solar_system.name,
                        'ship_id': kill.ship_id,
                        'ship': kill.ship.name,
                        'victim': {
                            'id': kill.victim_character_id,
                            'name': victim_name,
                            'corp_id': kill.victim_corporation_id,
                            'corp': victim_corp,
                            'alliance_id': kill.victim_alliance_id,
                            'alliance': victim_alliance
                        }
                    })
                })
        except (KeyError, IntegrityError) as e:
            # ship_type_id was null once
            print(e)

    killboard_redisq.apply_async(countdown=30)
