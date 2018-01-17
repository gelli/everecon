# Create your views here.
import json
import logging

import requests
from django.http import HttpResponse
from django.shortcuts import render

from everecon.navigate.forms import NavigationForm
from everecon.sde.models import SolarSystem, Celestial

# Get an instance of a logger
LOG = logging.getLogger(__name__)


def get_systems(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        systems = SolarSystem.objects.filter(solar_system_name__icontains=q).order_by('solar_system_name')
        results = []
        for system in systems[:20]:
            sys_json = {}
            sys_json['id'] = system.solar_system_id
            sys_json['label'] = "%s (%s)" % (system.solar_system_name, system.region.name)
            sys_json['value'] = system.solar_system_name
            results.append(sys_json)
        data = json.dumps(results)
    else:
        data = 'fail'

    return HttpResponse(data, 'application/json')


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
    system_ids = r.json()

    # prefetches all data needed, reduces query count
    prefetch = ['region', 'kill_set', 'kill_set__location', 'kill_set__location__destination',
                'kill_set__location__item']
    query = SolarSystem.objects.filter(solar_system_id__in=system_ids).prefetch_related(*prefetch)

    systems = list(query)
    systems.sort(key=lambda s: system_ids.index(s.solar_system_id))

    return get_kills(systems)


def get_kills(systems: list):
    waypoints = []

    for system in systems:
        waypoint = WayPoint(system)

        db_kills = system.kill_set.all()

        waypoint.kills = {
            'all': db_kills.count(),  # len(event.kills),
            'pods': 0,
            'latest': None,
            # 'db': db_kills
        }

        latest = None
        for kill in db_kills:

            LOG.debug(kill)
            location = kill.location
            time = kill.time

            if kill.ship_type_id == 670:
                waypoint.kills['pods'] += 1

            if latest is None or latest < time:
                latest = time

            if location.is_stargate():
                camp = waypoint.add_camp(GateCamp(location))
                camp.kills += 1
            else:
                LOG.debug("Not a stargate")
        waypoint.latest = latest if latest else None
        waypoints.append(waypoint)

    return waypoints


def index(request):
    LOG.info("Called request")
    if request.method == 'POST':
        form = NavigationForm(request.POST)
        waypoints = None
        if form.is_valid():
            waypoints = calc_route(form.from_system, form.to_system)

        return render(request, 'pages/index.html', {'form': form, 'waypoints': waypoints})
    else:
        form = NavigationForm()

    return render(request, 'pages/index.html', {'form': form})
