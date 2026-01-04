# Custom-Flight-Manager

This is a simple yet clear flight manager application for your trips.

The purpose of this APP is to provide users with comprehensive statistics of their flight data (unlike many commercial APPs which require payment to access complete data).

## How to open the APP

First, you need to setup the Python environment:
```bash
pip install -r requirements.txt
```

Then, you can start the server:
```bash
streamlit run main.py  
```

Finally, your own database will be created and updated during using the APP.


## Something to further improve
- [ ] Change the overlapping routes into arcs
- [ ] Directly import the data from existing apps (e.g., 航旅纵横) conveniently
- [ ] The trip to the United States should be changed to a trans-Pacific route