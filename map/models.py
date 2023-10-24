from django.db import models

    
class Sensors(models.Model):
    sensor = models.CharField(max_length=122)
    latitude = models.FloatField()
    longitude = models.FloatField()
    color = models.CharField(max_length=50, default='red')
    sensor_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.sensor}_{self.color}:{self.longitude}_{self.latitude}'
    
    class Meta:
        ordering = ['-sensor_created']
        get_latest_by = ['sensor_created']
        
    
class SensorReadings(models.Model):
    sensor = models.ForeignKey(Sensors, on_delete=models.CASCADE)
    temperature = models.FloatField()
    pressure = models.FloatField()
    steam_injection = models.FloatField()
    reading_created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.sensor}'
    
    class Meta:
        ordering = ['-reading_created']
        get_latest_by = ['reading_created']