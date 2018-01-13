import asyncio
import logging
import timeit

import aiohttp
import hermes.backend.dict
from everecon.sde.models import SolarSystem

cache = hermes.Hermes(hermes.backend.dict.Backend)

BASE_URL = 'https://zkillboard.com/api'

# Get an instance of a logger
LOG = logging.getLogger(__name__)


class SystemEvents(object):
    def __init__(self, system: SolarSystem):
        self.system_id = system.solar_system_id
        self.kills = []


# @cache(ttl=300)
async def get_kills_in_system(system):
    url = '{}/solarSystemID/{}/pastSeconds/3600/kills/'.format(BASE_URL, system.solar_system_id)
    LOG.info('Calling %s', url.format(system.solar_system_id))
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:

            events = SystemEvents(system)
            events.kills = await response.json()
            return events

            #    r = requests.get(url.format(system.solar_system_id))
            #    return r.json()


def get_kills_in_systems(systems: list):

    start_time = timeit.default_timer()

    loop = asyncio.SelectorEventLoop()
    asyncio.set_event_loop(loop)

    futures = []

    for system in systems:
        futures.append(asyncio.ensure_future(get_kills_in_system(system)))

    result = loop.run_until_complete(asyncio.gather(*futures))
    loop.close()

    events = {}
    for entry in result:
        events[entry.system_id] = entry

    print("Getting data took %.2f secs" % (timeit.default_timer() - start_time))

    return events
