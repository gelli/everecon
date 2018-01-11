from django.db import models
import math


class Region(models.Model):
    class Meta:
        managed = False
        db_table = 'mapRegions'

    region_id = models.IntegerField(primary_key=True, db_column='regionID')
    name = models.CharField(max_length=100, db_column='regionName')


class SolarSystem(models.Model):
    class Meta:
        managed = False
        db_table = 'mapSolarSystems'

    solar_system_id = models.IntegerField(primary_key=True, db_column='solarSystemID')
    solar_system_name = models.CharField(max_length=100, db_column='solarSystemName')
    region = models.ForeignKey(Region, on_delete=models.PROTECT, db_column='regionID')
    security = models.FloatField()

    @property
    def name(self):
        return self.solar_system_name

    def get_location(self, x, y, z):
        celestials = Celestial.objects.filter(solar_system_id=self.solar_system_id)
        distance = None
        location = None
        for celestial in celestials:
            newDistance = math.sqrt(pow(celestial.x - x, 2) +
                                    pow(celestial.y - y, 2) +
                                    pow(celestial.z - z, 2))

            if distance is None or distance > newDistance:
                distance = newDistance
                location = celestial

        return location


class InvName(models.Model):
    class Meta:
        managed = False
        db_table = 'invNames'

    itemID = models.IntegerField(primary_key=True)
    itemName = models.CharField(max_length=200)


class Celestial(models.Model):
    class Meta:
        managed = False
        db_table = 'mapDenormalize'

    item = models.OneToOneField(InvName, db_column='itemID', primary_key=True, on_delete=models.PROTECT)
    type_id = models.IntegerField(db_index=True, db_column='typeID')
    group_id = models.IntegerField(db_column='groupID')
    solar_system = models.ForeignKey(SolarSystem, on_delete=models.PROTECT, db_column='solarSystemID')
    constellation_id = models.IntegerField(db_index=True, db_column='constellationID')
    region_id = models.IntegerField(db_index=True, db_column='regionID')
    orbit_id = models.IntegerField(db_column='orbitID')
    x = models.FloatField()
    y = models.IntegerField()
    z = models.IntegerField()
    radius = models.IntegerField()
    itemName = models.CharField(max_length=100)
    security = models.FloatField()
    celestial_index = models.IntegerField(db_column='celestialIndex')
    orbit_index = models.IntegerField(db_column='orbitIndex')

    def __init__(self, *args, **kwargs):
        super(Celestial, self).__init__(*args, **kwargs)
        if self.type_id:
            self.__class__ = CELESTIAL_TYPES.get(self.type_id, Celestial)

    @property
    def name(self):
        return self.itemName if self.itemName else self.item.itemName

    def is_stargate(self):
        return self.type_id in {k: v for k, v in CELESTIAL_TYPES.items() if v == StarGate}.keys()


class StarGate(Celestial):
    class Meta:
        proxy = True

    @property
    def destination(self):
        return Celestial.objects.raw("SELECT d.* FROM mapDenormalize d, mapJumps j "
                                     "WHERE d.itemID = j.destinationID "
                                     "AND j.stargateID = {}".format(self.item_id))[0]


CELESTIAL_TYPES = {
    16: StarGate,
    17: StarGate,
    3873: StarGate,
    3874: StarGate,
    3875: StarGate,
    3876: StarGate,
    3877: StarGate,
    12292: StarGate,
    29624: StarGate,
    29625: StarGate,
    29626: StarGate,
    29627: StarGate,
    29629: StarGate,
    29632: StarGate,
    29633: StarGate,
    29634: StarGate,
    29635: StarGate
}
