
# THIS FILE IS FOR DECOUPLING THE APP. IT CONTAINS OBJECTS THAT CAN BE SHARED AND USED BY SEVERAL FUNCTIONS

# INDUSTRIAL SITE COORDINATES
INDUSTRIAL_SITE_LONGITUDE = 41.5025
INDUSTRIAL_SITE_LATITUDE = -72.699997

# TILE LAYERS
custom_tile_layers = [
        {
        "name": "Esri Satellite",
        "url": 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        "attr": 'Esri',
    },
    {
        "name": "Google Satellite",
        "url": 'https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
        "attr": 'Google',
    },
    {
        "name": "Google Satellite2",
        "url": 'https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
        "attr": 'Google',
    },
    {
        "name": "Google Terrain",
        "url": 'https://mt1.google.com/vt/lyrs=p&x={x}&y={y}&z={z}',
        "attr": 'Google',
    },
    {
        "name": "Google Maps",
        "url": 'https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
        "attr": 'Google',
    },
]