from django.db import models
import humanize
from django.utils import timezone



class ShortURL(models.Model):
    short_url = models.CharField(null=False, max_length=255, unique=True)
    target_url = models.CharField(null=False, max_length=1000)
    redirects = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def as_dict(self):
        return {
            'short_url': self.short_url,
            'target_url': self.target_url,
            'redirects': self.redirects,
            'created': self.created,
            'created_ago': humanize.naturaltime(timezone.now() - self.created),
            'target_devices': [obj.as_dict() for obj in self.target_devices.all()]
        }


class TargetDevice(models.Model):
    MOBILE = 1
    TABLET = 2

    DEVICE_TYPES = (
        (MOBILE, 'Mobile'),
        (TABLET, 'Tablet'),
    )

    url = models.CharField(null=False, max_length=1000)
    device_type = models.PositiveSmallIntegerField(choices=DEVICE_TYPES, db_index=True)
    short_url = models.ForeignKey(ShortURL, related_name="target_devices", null=False)

    @staticmethod
    def device_name_to_id(device_name):
        device_type = device_name.lower().capitalize()
        types = dict((y, x) for x, y in TargetDevice.DEVICE_TYPES)

        if device_type not in types:
            return None
        return types[device_type]

    @staticmethod
    def device_id_to_name(device_id):
        types = dict((x, y) for x, y in TargetDevice.DEVICE_TYPES)

        if device_id not in types:
            return None
        return types[device_id]

    def as_dict(self):
        return {
            'url': self.url,
            'device_type': TargetDevice.device_id_to_name(self.device_type),
        }
