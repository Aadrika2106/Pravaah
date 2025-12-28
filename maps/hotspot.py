import folium

def create_hotspot_map(weather, pollution, river, user_data):
    m = folium.Map(location=[20.5937, 78.9629], zoom_start=5)
    
    hotspots = [
        [28.6139, 77.2090, 85],  # Delhi
        [19.0760, 72.8777, 62],  # Mumbai
        [13.0827, 80.2707, 55],  # Chennai
    ]
    
    for lat, lon, conc in hotspots:
        color = 'red' if conc > 70 else 'orange' if conc > 50 else 'green'
        folium.CircleMarker(
            [lat, lon],
            radius=10,
            color=color,
            fill=True,
            fillColor=color,
            popup=f"Concentration: {conc}"
        ).add_to(m)
    
    return m