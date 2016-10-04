from GarageWarden.models import Setting


def values_for_prefix(prefix):
    return {k.key.replace(prefix+".", ""): k.get_value() for k in Setting.objects.filter(key__startswith=prefix+".")}


def value(key):
    return Setting.objects.get(key=key).get_value()
