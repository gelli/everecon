# Create your views here.
import json
from django.http import HttpResponse

from api.models import SolarSystem


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
