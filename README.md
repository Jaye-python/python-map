# Python-Map-Application Based on Folium

### Logic implemented:
1. **Django** was used as backend
2. **Folium** was used to build the interactive map to display surfaces and satellite imagery of the industrial site's geographical data
3. **Django-Channels** was used to built a **websocket** to receive real-time data containing temperature, pressure, and steam injection readings from sensors located at various points within the industrial site
4. **Folium Heatmap plugin** was used to generate heatmaps from sensors
5. To implement **real-time update of heatmaps**: the received data from the websocket is saved to the DB then a webpage that serves heatmaps is being refreshed every 10 seconds with **JavaScript** to show the latest data from the DB



### To launch this app on your system:
1. Navigate to your desktop
```
cd Desktop
```
2. Create a new folder/directory called `usecase`
```
mkdir usecase
```
3. Navigate into this new folder
```
cd usecase
```
4. Create a new Python Virtual environment in the `usecase` folder.
```
python3 -m venv ./venv
```
5. Activate this new virtual environment
```
source venv/bin/activate
```
6. Clone this git repo
```
git clone https://github.com/Jaye-python/python-map.git
```
7. Move into the `python-map` folder 
```
cd python-map
```
8. Install dependencies
```
pip install -r pdo_project/requirements/base.txt
```
9. Create your Database
10. Input the following environment variables in your environment file. Your `environment` file is the `\usecase\venv\bin\activate` (for Linux OS)
```
export IS_LOCAL=True
export SECRET_KEY='mydjango-secure-az&m%41ft*^47trh@m2ppc&ywxx@rf#d82lv^z11-)6(ug#ua0'
export DATABASE_NAME='your-db-name'
export DATABASE_USER='your-db-username'
export DATABASE_PASS='your-db-password'
```
12. Deactivate the environment and reactivate it to load your changes
```
deactivate
```
```
source venv/bin/activate
```
11. Migrate
```
python manage.py migrate
```
12. Run code below to seed the DB with seed data located in: `map/fixtures/data.json`:
```
python manage.py loaddata data.json
```
13. Launch
```
python manage.py runserver
```
14. Navigate to the app
```
http://127.0.0.1:8000
```


