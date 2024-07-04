# Python-Map-Application Based on Folium
This app is a geo-spatial app showing coordinates of a site with several points where heat sensors are placed which show readings in real-time via heat maps so that important information about those sensors get flagged in realtime

### Logic implemented:
1. **Django** was used as backend
2. **Folium** was used to build the interactive map to display surfaces and satellite imagery of the industrial site's geographical data
3. **Django-Channels** was used to built a **websocket** to receive real-time data containing temperature, pressure, and steam injection readings from sensors located at various points within the industrial site
4. **Folium Heatmap plugin** was used to generate heatmaps from sensors
5. To implement **real-time update of heatmaps**: the received data from the websocket is saved to the DB then a webpage that serves heatmaps is being refreshed every 10 seconds (using **JavaScript**) to show the latest data from the DB


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
10. Input the following environment variables in your environment file. Your `environment` file is the `\usecase\venv\bin\activate` (for Linux OS). Only change values for `'your-db-name'`, `'your-db-username'`, `'your-db-password'`
```
export IS_LOCAL=True
export SECRET_KEY='mydjango-secure-az&m%41ft*^47trh@m2ppc&ywxx@rf#d82lv^z11-)6(ug#ua0'
export DATABASE_NAME='your-db-name'
export DATABASE_USER='your-db-username'
export DATABASE_PASS='your-db-password'
```
11. You may deactivate the virtual environment
```
deactivate
```
12. Now, open this folder in VS Code (or your preferred editor). **note the trailing point**
```
code .
```
13. Open a new VS Code terminal and activate your environment (if not activated)
```
source ~/Desktop/usecase/venv/bin/activate
```
14. Run migrate code that will create all required database tables
```
python manage.py migrate
```
15. Run code below to seed the DB with seed data located in: `map/fixtures/data.json`:
```
python manage.py loaddata data.json
```
16. Launch the app
```
python manage.py runserver
```
17. Navigate to the app
```
http://127.0.0.1:8000
```
18. To run the Jupyter notebook, **Open a new terminal** while the app is running and **run below code**. Click the URL provided which looks like this: `http://localhost:8888/tree?token=b9b1fe9bfadf347146e04b203631ddfce3005033bfeb46f4`; then open the `pdo.ipynb` file
```
jupyter notebook
```
19. To send a sample payload to the websocket via the opened Jupyter notebook: update the **PROJECTPATH** variable in the first cell to your correct path, **then run the first cell**, then **run the second cell**
20. In the app (from your browser), go to the **Daily Reading** link to see an interactive map
21. In the app, click on the `Click for latest data` button to get the latest data for all sensors
22. In the app, go to the **Historical Reading** link, click on **Submit** to get the historical reading for `Temperature` for `Sensor 8`. You may use the form to get data for other sensors
23. In the app, go to the **Live Signal** link to get live signals that gets updated every 10 seconds
24. Go to the `map/static/map/mains.js` file to see sample JavaScript code to send to the websocket

