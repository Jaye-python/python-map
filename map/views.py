from django.views.generic.base import TemplateView
import folium
from folium import plugins
from map.models import Sensors, SensorReadings
from .utils import custom_tile_layers, INDUSTRIAL_SITE_LATITUDE, INDUSTRIAL_SITE_LONGITUDE
from datetime import date
from django.db.models import Avg, Max


class DailyReadingView(TemplateView):
    template_name = 'map/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sensors = Sensors.objects.all()
        context['today_date'] = date.today()
        
        # Here I grab the client's requests
        date_from_client = self.request.GET.get('day')
        aggregation_from_client = self.request.GET.get('aggregation')
        get_live_data = self.kwargs.get('live', False)
               
               
        # INDUSTRIAL SITE
        m = folium.Map(
            location=[INDUSTRIAL_SITE_LONGITUDE, INDUSTRIAL_SITE_LATITUDE], 
            tiles=None, 
            zoom_start=9, 
            control_scale=True,            
            )

        # Here, I am adding Custom tile layers
        for tile_layer in custom_tile_layers:
            folium.TileLayer(tile_layer["url"], name=tile_layer["name"], attr=tile_layer["attr"], control=True).add_to(m)

        # Here, I am adding LocateControl to find user's location
        plugins.LocateControl().add_to(m)

        # Here, I am adding Draw control for drawing on the map
        plugins.Draw(export=True, filename='data.geojson', position='topleft').add_to(m)

        # Here, I am adding MeasureControl for measuring distances and areas
        plugins.MeasureControl(position='topright', primary_length_unit='meters',
                              secondary_length_unit='miles', primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(m)
        
        # Here, I am checking if readings are available for the day requested by client
        readings_are_available_for_today = SensorReadings.objects.filter(reading_created__date=date_from_client)
        
        # Here, I am creating empty lists for the heatmaps
        heat_data_temperature = []
        heat_data_pressure = []
        heat_data_steam_injection = []
        
        if get_live_data:
            for sensor in sensors:
                try:
                    live_readings = SensorReadings.objects.filter(sensor=sensor).latest()
                    # Here, I am appending the data in the format [longitude, latitude, reading ]
                    heat_data_temperature.append([sensor.longitude, sensor.latitude, live_readings.temperature])
                    heat_data_pressure.append([ sensor.longitude, sensor.latitude, live_readings.pressure])
                    heat_data_steam_injection.append([sensor.longitude, sensor.latitude, live_readings.steam_injection])
                    
                    # Here, I am adding markers for the sensors
                    coordinates = (sensor.longitude, sensor.latitude)
                    folium.Marker(coordinates, popup=sensor.sensor, tooltip=sensor.sensor, draggable=True).add_to(m)
                    
                except SensorReadings.DoesNotExist:
                    pass
                
            # Here, I am adding heatmaps for temperature, pressure, and steam injection
            plugins.HeatMap(heat_data_temperature, name='Temperature Heatmap', min_opacity=0.0,
                gradient={0.4: 'green', 0.6: 'yellow', 1: 'red'}
                ).add_to(m)
            plugins.HeatMap(heat_data_pressure, name='Pressure Heatmap', min_opacity=0.0,
                gradient={0.4: 'blue', 0.6: 'lime', 1: 'red'}
                ).add_to(m)
            plugins.HeatMap(heat_data_steam_injection, name='Steam Injection Heatmap', min_opacity=0.0,
                gradient={0.4: 'orange', 0.6: 'red'}
                ).add_to(m)
    
        elif readings_are_available_for_today:

            for sensor in sensors:
                if aggregation_from_client == 'average':
                    today_readings = readings_are_available_for_today.filter(sensor=sensor).aggregate(Avg('temperature'), Avg('pressure'), Avg('steam_injection'))

                    # Here, I am appending the data in the format [longitude, latitude, reading ]
                    heat_data_temperature.append([sensor.longitude, sensor.latitude, today_readings['temperature__avg'] or 0])
                    heat_data_pressure.append([ sensor.longitude, sensor.latitude, today_readings['pressure__avg'] or 0])
                    heat_data_steam_injection.append([sensor.longitude, sensor.latitude, today_readings['steam_injection__avg'] or 0 ])
                
                    # Here, I am adding markers for the sensors
                    coordinates = (sensor.longitude, sensor.latitude)
                    folium.Marker(coordinates, popup=sensor.sensor, tooltip=sensor.sensor, draggable=True).add_to(m)
                
                elif aggregation_from_client == 'maximum':            
                    today_readings = readings_are_available_for_today.filter(sensor=sensor).aggregate(Max('temperature'), Max('pressure'), Max('steam_injection'))

                    # Here, I am appending the data in the format [longitude, latitude, reading ]
                    heat_data_temperature.append([sensor.longitude, sensor.latitude, today_readings['temperature__max'] or 0])
                    heat_data_pressure.append([ sensor.longitude, sensor.latitude, today_readings['pressure__max'] or 0])
                    heat_data_steam_injection.append([sensor.longitude, sensor.latitude, today_readings['steam_injection__max'] or 0 ])
                
                    # Here, I am adding markers for the sensors
                    coordinates = (sensor.longitude, sensor.latitude)
                    folium.Marker(coordinates, popup=sensor.sensor, tooltip=sensor.sensor, draggable=True).add_to(m)
            
            # Here, I am adding heatmaps for temperature, pressure, and steam injection
            plugins.HeatMap(heat_data_temperature, name='Temperature Heatmap', min_opacity=0.0,
                gradient={0.4: 'green', 0.6: 'yellow', 1: 'red'}
                ).add_to(m)
            plugins.HeatMap(heat_data_pressure, name='Pressure Heatmap', min_opacity=0.0,
                gradient={0.4: 'blue', 0.6: 'lime', 1: 'red'}
                ).add_to(m)
            plugins.HeatMap(heat_data_steam_injection, name='Steam Injection Heatmap', min_opacity=0.0,
                gradient={0.4: 'orange', 0.6: 'red'}
                ).add_to(m)

        else:
            context['no_reading_message_to_client'] = "No reading available for this day"
        
        # LayerControl switch
        folium.LayerControl().add_to(m)        
        
        context['map'] = m._repr_html_()
        
        return context


class LiveSignalView(TemplateView):
    template_name = 'map/livesignal.html'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sensors = Sensors.objects.all()
        context['today_date'] = date.today()
        
        # INDUSTRIAL SITE
        m = folium.Map(
            location=[INDUSTRIAL_SITE_LONGITUDE, INDUSTRIAL_SITE_LATITUDE], 
            tiles=None, 
            zoom_start=9, 
            control_scale=True,            
            )

        # Here, I am adding Custom tile layers
        for tile_layer in custom_tile_layers:
            folium.TileLayer(tile_layer["url"], name=tile_layer["name"], attr=tile_layer["attr"], control=True).add_to(m)

        # Here, I am adding LocateControl to find user's location
        plugins.LocateControl().add_to(m)

        # Here, I am adding Draw control for drawing on the map
        plugins.Draw(export=True, filename='data.geojson', position='topleft').add_to(m)

        # Here, I am adding MeasureControl for measuring distances and areas
        plugins.MeasureControl(position='topright', primary_length_unit='meters',
                              secondary_length_unit='miles', primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(m)
        
                
        # Here, I am creating empty lists for the heatmaps
        heat_data_temperature = []
        heat_data_pressure = []
        heat_data_steam_injection = []
        
        
        for sensor in sensors:
            try:
                live_readings = SensorReadings.objects.filter(sensor=sensor).latest()
                # Here, I am appending the data in the format [longitude, latitude, reading ]
                heat_data_temperature.append([sensor.longitude, sensor.latitude, live_readings.temperature])
                heat_data_pressure.append([ sensor.longitude, sensor.latitude, live_readings.pressure])
                heat_data_steam_injection.append([sensor.longitude, sensor.latitude, live_readings.steam_injection])
                
                # Here, I am adding markers for the sensors
                coordinates = (sensor.longitude, sensor.latitude)
                folium.Marker(coordinates, popup=sensor.sensor, tooltip=sensor.sensor, draggable=True).add_to(m)
                
            except SensorReadings.DoesNotExist:
                pass
            
        # Here, I am adding heatmaps for temperature, pressure, and steam injection
        plugins.HeatMap(heat_data_temperature, name='Temperature Heatmap', min_opacity=0.0,
            gradient={0.4: 'green', 0.6: 'yellow', 1: 'red'}
            ).add_to(m)
        plugins.HeatMap(heat_data_pressure, name='Pressure Heatmap', min_opacity=0.0,
            gradient={0.4: 'blue', 0.6: 'lime', 1: 'red'}
            ).add_to(m)
        plugins.HeatMap(heat_data_steam_injection, name='Steam Injection Heatmap', min_opacity=0.0,
            gradient={0.4: 'orange', 0.6: 'red'}
            ).add_to(m)
        
        # LayerControl switch
        folium.LayerControl().add_to(m)        
        
        context['map'] = m._repr_html_()
        
        return context
    
    
    
class HistoricalReadingView(TemplateView):
    template_name = 'map/historical.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        heatmap_data = []
        
        # Here I grab the client's requests
        sensor_from_client = self.request.GET.get('sensor')
        reading_from_client = self.request.GET.get('reading')
        
        heatmap_data = []
        index = []
        
        # HERE'S THE MAIN INDUSTRIAL SITE
        m = folium.Map(
            location=[INDUSTRIAL_SITE_LONGITUDE, INDUSTRIAL_SITE_LATITUDE], 
            tiles=None, 
            zoom_start=9, 
            control_scale=True,            
            )

        if reading_from_client and sensor_from_client:
            
            readings = SensorReadings.objects.filter(sensor__sensor=sensor_from_client).select_related('sensor')\
                        .values('pressure', 'temperature', 'steam_injection', 'reading_created', 'sensor__latitude', 'sensor__longitude', 'sensor__sensor')
            if readings:
                for reading in readings:
                    data_point = [reading['sensor__longitude'], reading['sensor__latitude'], reading[reading_from_client]]
                    heatmap_data.append([data_point])
                    index.append(reading['reading_created'].isoformat())
                    
                    # Here, I am adding markers for the sensors
                    coordinates = (reading['sensor__longitude'], reading['sensor__latitude'],)
                    folium.Marker(coordinates, popup=reading['sensor__sensor'], tooltip=reading['sensor__sensor'], draggable=True).add_to(m)

                #   I add the HeatMapWithTime plugin
                plugins.HeatMapWithTime(heatmap_data, radius=150, name=reading_from_client, index=index, auto_play=True,).add_to(m)
            else:
                context['no_reading_message_to_client'] = "No reading available for this sensor"               


        # Here, I am adding Custom tile layers
        for tile_layer in custom_tile_layers:
            folium.TileLayer(tile_layer["url"], name=tile_layer["name"], attr=tile_layer["attr"], control=True).add_to(m)

        # Here, I am adding LocateControl to find user's location
        plugins.LocateControl().add_to(m)

        # Here, I am adding Draw control for drawing on the map
        plugins.Draw(export=True, filename='data.geojson', position='topleft').add_to(m)

        # Here, I am adding MeasureControl for measuring distances and areas
        plugins.MeasureControl(position='topright', primary_length_unit='meters',
                            secondary_length_unit='miles', primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(m)

        # Here, I am adding LayerControl switch
        folium.LayerControl().add_to(m)         
        context['map'] = m._repr_html_()

        return context