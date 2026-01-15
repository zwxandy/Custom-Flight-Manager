# SkyLink-Flight-Manager

This is a simple yet clear flight application for your trip managenment.

The purpose of this APP is to provide users with comprehensive statistics of their flight data (unlike many commercial APPs which require payment to access complete data).


## APP Design

```bash
Python version: Python 3.8
GUI: Streamlit
Visualization: Folium + Leaflet (interactive world map)
Distance computation: Haversine / geopy
Front-end beautification: CSS
```


## How to open the APP

First, you need to setup the Python environment:
```bash
pip install -r requirements.txt
```

Then, you can start the server with a webpage opened automatically:
```bash
streamlit run main.py
```

Finally, your own database will be created and updated during using the APP.

To specify the database file, you can modify in `database_utils.py`:
```python
DB_FILE = 'database_name.db'
```


## Something to further improve
- [x] Counting the number of times in different cities
- [ ] Change the overlapping routes into arcs
- [ ] Directly import the data from existing apps (e.g., 航旅纵横) conveniently
- [ ] The trip to the United States should be changed to a trans-Pacific route

BTW, if you have any suggestions or PR, please let me know :)