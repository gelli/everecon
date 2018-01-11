import logging

import requests
from django.shortcuts import render

from api.models import SolarSystem, Celestial
from noflyzone.forms import NavigationForm
from services import killboard
import maya

# Get an instance of a logger
LOG = logging.getLogger(__name__)


class GateCamp(object):

    def __init__(self, location: Celestial):
        self.location = location
        self.name = location.name
        self.kills = 0


class WayPoint(object):

    def __init__(self, system):
        """
        :type system: SolarSystem
        """
        self.system = system
        self.camps = {}
        self.kills = 0
        self.latest = None

    def add_camp(self, camp: GateCamp):
        return self.camps.setdefault(camp.location.item_id, camp)


def calc_route(sys_from, sys_to):
    """
    :type sys_from: SolarSystem
    :type sys_to: SolarSystem
    """
    url = 'https://esi.tech.ccp.is/latest/route/{}/{}/?datasource=tranquility&flag=shortest'

    r = requests.get(url.format(sys_from.solar_system_id, sys_to.solar_system_id))
    systems = [SolarSystem.objects.get(solar_system_id=system_id) for system_id in r.json()]

    return get_kills(systems)


"""
https://zkillboard.com/api/solarSystemID/30001155/solarSystemID/30001156/pastSeconds/7200/kills/
1
Fining celestials
30001155
location is a stargate!Celestial object (50013602)
https://zkillboard.com/api/solarSystemID/30001156/pastSeconds/7200/kills/
0
https://zkillboard.com/api/solarSystemID/30001162/pastSeconds/7200/kills/
0
https://zkillboard.com/api/solarSystemID/30001198/pastSeconds/7200/kills/
"""


def get_kills(systems: list):

    events = killboard.get_kills_in_systems(systems)
    waypoints = []

    for system in systems:
        waypoint = WayPoint(system)
        event = events[system.solar_system_id]
        waypoint.kills = {
            'all': len(event.kills),
            'pods': 0,
            'latest': None
        }

        latest = None
        for kill in event.kills:

            LOG.debug(kill)
            coords = kill['victim']['position']
            location = system.get_location(coords['x'], coords['y'], coords['z'])

            time = maya.parse(kill['killmail_time'])

            if kill['victim']['ship_type_id'] == 670:
                waypoint.kills['pods'] += 1

            if latest is None or latest < time:
                latest = time

            if location.is_stargate():
                camp = waypoint.add_camp(GateCamp(location))
                camp.kills += 1
            else:
                LOG.debug("Not a stargate")
        waypoint.latest = latest.datetime() if latest else None
        waypoints.append(waypoint)

    return waypoints


def index(request):
    LOG.info("Called request")
    if request.method == 'POST':
        form = NavigationForm(request.POST)
        waypoints = None
        if form.is_valid():
            waypoints = calc_route(form.from_system, form.to_system)

        return render(request, 'noflyzone/index.html', {'form': form, 'waypoints': waypoints})
    else:
        form = NavigationForm()

    return render(request, 'noflyzone/index.html', {'form': form })
