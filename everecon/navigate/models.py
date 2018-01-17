import maya
from django.db import models

from everecon.sde.models import Celestial, SolarSystem


class Kill(models.Model):
    """
    {
      'package': {
        'killID': 67346342,
        'killmail': {
          'killmail_id': 67346342,
          'killmail_time': '2018-01-16T16:07:00Z',
          'victim': {
            'damage_taken': 7414,
            'ship_type_id': 11961,
            'character_id': 692642015,
            'corporation_id': 692758987,
            'alliance_id': 1301367357,
            'items': [
              {
                'item_type_id': 12771,
                'singleton': 0,
                'flag': 27,
                'quantity_dropped': 40
              },
              ...
            ],
            'position': {
              'x': 2571129707848.6,
              'y': -317028560701.03,
              'z': 1843986330952.8
            }
          },
          'attackers': [
            {
              'security_status': 3,
              'final_blow': False,
              'damage_done': 1679,
              'character_id': 93909261,
              'corporation_id': 98043060,
              'alliance_id': 99006327,
              'ship_type_id': 17922,
              'weapon_type_id': 2185
            },
            ...
          ],
          'solar_system_id': 30001987
        },
        'zkb': {
          'locationID': 50004088,
          'hash': 'a5b12642df7b92261628cc1e545e8b1782f0cf6c',
          'fittedValue': 279051245.99,
          'totalValue': 285282769.93,
          'points': 1,
          'npc': False,
          'solo': False,
          'awox': False,
          'href': 'https://esi.tech.ccp.is/v1/killmails/67346342/a5b12642df7b92261628cc1e545e8b1782f0cf6c/'
        }
      }
    }
    """
    kill_id = models.IntegerField(primary_key=True)
    time = models.DateTimeField(db_index=True)
    location = models.ForeignKey(Celestial, db_index=True, on_delete=models.PROTECT)
    solar_system = models.ForeignKey(SolarSystem, db_index=True, on_delete=models.PROTECT)
    ship_type_id = models.IntegerField()

    @classmethod
    def from_json(cls, json):
        if json['package'] is None:
            return None

        kill = Kill()
        kill.kill_id = json['package']['killID']
        kill.time = maya.parse(json['package']['killmail']['killmail_time']).datetime()
        kill.location_id = json['package']['zkb']['locationID']
        kill.solar_system_id = json['package']['killmail']['solar_system_id']
        kill.ship_type_id = json['package']['killmail']['victim']['ship_type_id']
        return kill

    def __str__(self):
        return 'Kill<id=%d, time=%s, location=%s, solar_system=%s, ship_type=%s>' % (self.kill_id, self.time, self.location_id, self.solar_system_id, self.ship_type_id)
