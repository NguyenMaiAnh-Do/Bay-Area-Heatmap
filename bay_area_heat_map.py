import pandas as pd
import folium
from tokens import aqi_token
from folium.plugins import HeatMap 

# 1. Download data
# (lat, long)-> bottom left, (lat, long)-> top right
# For Bay Area from San Francisco to Morgan Hills
lat_long_box = '37.113,-122.534,37.805,-121.614' 
url=f'https://api.waqi.info/map/bounds/?latlng={lat_long_box}&token={aqi_token}' 
bayarea = pd.read_json(url) 

# 2. Create DataFrame: station_name, lat, lon, aqi
# For example, "Redwood City, San Mateo, California",  37.482930, -122.203480, 46    
all_rows = []
for row in bayarea['data']:
    all_rows.append([row['station']['name'],row['lat'],row['lon'],row['aqi']])
df = pd.DataFrame(all_rows,columns=['station_name', 'lat', 'lon','aqi'])
print(df)

# 3. Clean the DataFrame from invalid numbers
# Invalid entries are parsed to NaN and then dropped
df['aqi'] = pd.to_numeric(df.aqi,errors='coerce') 
df1 = df.dropna(subset = ['aqi'])

# 4. Make a heat map with Folium
df2 = df1[['lat', 'lon', 'aqi']]
init_loc = [37, -122] # Sunnyvale
m = folium.Map(location = init_loc, zoom_start = 8)
heat_aqi = HeatMap(df2, min_opacity = 0.1,radius = 20, blur = 20, max_zoom = 2)
m.add_child(heat_aqi)
# Show the map (only works in Jupiter Notebook)
m

# 5. Generate heatmap image using webdriver
import io
from PIL import Image
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

data_timestamp = bayarea.data[0]['station']['time']
image_name = data_timestamp[:10]
img_data = m._to_png(5)
img = Image.open(io.BytesIO(img_data))
img.save(image_name+".png")
img.save("image.png")

# 6. Upload the image to GoogleDrive
# Run script in google_drive_uploader.py
