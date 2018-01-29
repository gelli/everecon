# Create your views here.
import json
import logging
import requests
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.db import connection
from everecon.navigate.forms import NavigationForm
from everecon.sde.models import SolarSystem, Celestial, SolarSystemJump

# Get an instance of a logger
LOG = logging.getLogger('everecon')


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


def calc_route(sys_from, sys_to, flag):
    """
    :type sys_from: SolarSystem
    :type sys_to: SolarSystem
    """
    url = 'https://esi.tech.ccp.is/latest/route/{}/{}/?datasource=tranquility&flag={}'
    r = requests.get(url.format(sys_from.solar_system_id, sys_to.solar_system_id, flag))
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

            if kill.ship_id == 670:
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


def index(request: HttpRequest):
    if request.method == 'POST':
        form = NavigationForm(request.POST)
        waypoints = None
        if form.is_valid():
            waypoints = calc_route(form.from_system, form.to_system, form.prefer)

        return render(request, 'pages/index.html', {'form': form, 'waypoints': waypoints})
    else:
        form = NavigationForm()

    return render(request, 'pages/index.html', {'form': form})


@login_required(login_url='login')
def around(request: HttpRequest):
    headers = {"Authorization": "Bearer {}".format(request.session['token'])}
    r = requests.get('https://esi.tech.ccp.is/latest/characters/{}/location/'.format(request.user.id), headers=headers)

    location = r.json()

    system_id = int(location['solar_system_id'])
    system_id_list = [system_id]

    with connection.cursor() as cursor:
        cursor.execute('select s."solarSystemID" from "mapSolarSystems" s, "mapSolarSystemJumps" j '
                       'where s."solarSystemID" = j."toSolarSystemID" '
                       'and j."fromSolarSystemID" = {}'.format(system_id))

        [system_id_list.append(row[0]) for row in cursor.fetchall() ]

    prefetch = ['region', 'kill_set', 'kill_set__location', 'kill_set__location__destination',
                'kill_set__location__item']
    systems = SolarSystem.objects.filter(solar_system_id__in=system_id_list).prefetch_related(*prefetch)

    kills = get_kills(systems)

    current = next(filter(lambda sys: sys.solar_system_id == system_id,  systems))
    print(current)
    return render(request, 'pages/around.html', {'current': current, 'waypoints': kills})

def live(request: HttpRequest):
    return render(request, 'pages/live.html')
