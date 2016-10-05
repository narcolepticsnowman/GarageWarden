from django.db import models


class Setting(models.Model):
    VALUE_TYPES = (
        ("B", "Bool"),
        ("S", "String"),
        ("N", "Number")
    )
    key = models.CharField(max_length=100, primary_key=True)
    value = models.CharField(max_length=2000)
    description = models.CharField(max_length=2000)
    type = models.CharField(max_length=10, choices=VALUE_TYPES, default="S")
    order = models.IntegerField(default=0)

    def get_value(self):
        if self.type == "B":
            return self.value == "True"
        elif self.type == "N":
            return float(self.value)
        else:
            return self.value
