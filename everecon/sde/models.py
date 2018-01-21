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
    sun_type_id = models.IntegerField(db_column='sunTypeID')
    security = models.FloatField()

    @property
    def name(self):
        return self.solar_system_name

    def get_location(self, x, y, z):
        celestials = self.celestials.all() # .select_related('item', 'destination')
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

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(self, other.__class__):
            return self.solar_system_id == other.solar_system_id
        return False


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
    solar_system = models.ForeignKey(SolarSystem, on_delete=models.PROTECT, db_column='solarSystemID',
                                     related_name='celestials')
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
    def destination_name(self):
        return self.item.itemName[10:-1]


class Jump(models.Model):
    class Meta:
        managed = False
        db_table = 'mapJumps'

    stargateID = models.OneToOneField(Celestial, db_column='stargateID', on_delete=models.PROTECT, primary_key=True, related_name='destination')
    destinationID = models.OneToOneField(Celestial, db_column='destinationID', on_delete=models.PROTECT, related_name='destination+')


class SolarSystemJump(models.Model):
    class Meta:
        managed = False
        db_table = 'mapSolarSystemJumps'
        unique_together = (('from_system', 'to_system'),)

    from_system = models.ForeignKey(SolarSystem, on_delete=models.PROTECT, db_column='fromSolarSystemID',
                                        related_name='jumps')
    to_system = models.ForeignKey(SolarSystem, on_delete=models.PROTECT, db_column='toSolarSystemID',
                                      related_name='jumps_reverse')

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
