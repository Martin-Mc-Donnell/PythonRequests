import urllib.request
import json

# Fetching the data from the URL
with urllib.request.urlopen("https://raw.githubusercontent.com/datasets/geo-boundaries-world-110m/master/countries.geojson") as url:
    data = json.load(url)
    
    # Extracting country names
    country_names = [feature['properties']['name'] for feature in data['features']]
    print(len(country_names))
