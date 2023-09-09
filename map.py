import folium
import data
from streamlit_folium import st_folium, folium_static
import streamlit as st
import pandas as pd


# Create a map centered at a specific location
map_center = [21.0043061,105.8373198]
m = folium.Map(location=map_center, zoom_start=15)
# Add JavaScript code for interaction
popup_script = """
<script>
    // Function to show information on hover
    function showInfo(e) {
        e.target.openPopup();
    }
    
    // Function to hide information on mouseout
    function hideInfo(e) {
        e.target.closePopup();
    }
    
    // Attach functions to marker events
    var marker = L.DomUtil.get({0});
    marker.addEventListener('mouseover', showInfo);
    marker.addEventListener('mouseout', hideInfo);
</script>
"""

# Add the script to the map
m.get_root().html.add_child(folium.Element(popup_script))

# Display the map
map_plot = folium.Map(location=[21.0043061,105.8373198],zoom_start=13)  
folium.TileLayer('cartodbpositron').add_to(map_plot)
Lights = data.light

for i in range(Lights.shape[0]):
    #folium.CircleMarker([Lights.lat.iloc[i],Lights.lon.iloc[i]],radius = 5,color = '#a6cee3',fill = '#a6cee3' ).add_to(map_plot)

    light_location = [Lights.longtitude.iloc[i],Lights.latitude.iloc[i]]
    popup_content = "<strong>Street Light</strong><br>Location: {}, {}".format(Lights.latitude.iloc[i], Lights.longtitude.iloc[i])

    marker = folium.Marker(location=light_location, tooltip=popup_content,popup =popup_content, icon=folium.Icon(color='red', icon='lightbulb-cfl-on', prefix='fa'))
    marker.add_to(m)
folium.TileLayer('cartodbpositron').add_to(m)

def show():
    folium_static(m)
    st.divider()  # 👈 Draws a horizontal rule

    
