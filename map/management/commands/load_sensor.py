from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from map.models import Sensors
import csv
from django.db import transaction
from datetime import date # date.today()


class Command(BaseCommand):
    help = "Load sensor data from CSV file. Required Header Columns: sensor, longitude, latitude, color"

    def handle(self, *args, **options):
        data_file = settings.BASE_DIR / "data" / "sensors.csv"
        keys = ["sensor", "longitude", "latitude", "color",]

        with open(data_file, "r") as f:
            reader = csv.DictReader(f)
            sensor_list = [
                Sensors(**{k: row[k] for k in keys}) for row in reader
            ]

            with transaction.atomic():
                Sensors.objects.bulk_create(sensor_list)

        self.stdout.write(self.style.SUCCESS('Successfully created'))