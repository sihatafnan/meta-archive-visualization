import json
import matplotlib.pyplot as plt
from collections import Counter
import folium
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import networkx as nx

adds_path = "ads_information/"

sec_path = "security_and_login_information"

##---------------current logged in devices----------------------
"""
Identify which devices are most frequently used to access the account. 
A large number of sessions from unknown devices could indicate potential security risks.
"""
with open(sec_path + "/where_you're_logged_in.json") as f:
    data = json.load(f)

# Dictionary to track devices by IP, device, and location
device_sessions = {}
sessions = []
# Process each session in active_sessions_v2
for session in data["active_sessions_v2"]:
    device = session["device"]
    app = session["app"]
    ip_address = session["ip_address"]
    location = session["location"]

    # Create a unique key for each device-location combination
    key = (device, location)

    # If this device-location pair hasn't been added yet, initialize it
    if key not in device_sessions:
        device_sessions[key] = {
            "apps": set(),  # Use a set to avoid duplicates
            "location": location,
            "Device": device,
        }
    
    # Add the app to this device's app list
    device_sessions[key]["apps"].add(app)
    sessions.append(device_sessions[key])


device_counts = Counter(session["Device"] for session in sessions)

# Bar chart
plt.figure(figsize=(8, 6))
plt.bar(device_counts.keys(), device_counts.values(), color="skyblue")
plt.title("Active Device Sessions by Type")
plt.xlabel("Device")
plt.ylabel("Number of Active Sessions")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('active_device_sessions_bar_chart.png')  # Save the bar chart as PNG

"""
Geographic map of logged in locations
"""
geolocator = Nominatim(user_agent="geo_mapper")

# Function to fetch coordinates
def get_coordinates(location):
    try:
        geo_location = geolocator.geocode(location, timeout=10)
        if geo_location:
            return (geo_location.latitude, geo_location.longitude)
        else:
            print(f"Could not find coordinates for {location}")
            return None
    except GeocoderTimedOut:
        print(f"Timed out while fetching {location}")
        return None

for session in sessions:
    session["coordinates"] = get_coordinates(session["location"])
    # print(f"Location: {session['location'] , session['coordinates']}")

location_counts = Counter((session["location"], session["coordinates"]) for session in sessions)

# Create a folium map
login_map = folium.Map(location=[33.6846, -117.8265], zoom_start=6)  # Centered near Irvine

# Add markers for each location
for (location, coords), count in location_counts.items():
    folium.CircleMarker(
        location=coords,
        radius=5 + count,  # Marker size proportional to login frequency
        color="blue",
        fill=True,
        fill_color="blue",
        fill_opacity=0.6,
        tooltip=f"{location}: {count} logins"
    ).add_to(login_map)

# Save the map to an HTML file
login_map.save("login_locations_map.html")

"""
Network Graph: Device-App Relationship
Nodes represent devices and apps.
Edges represent the connection between devices and the apps they access.
Helps users see which apps are accessed from multiple devices or shared between locations.
"""
# Create a network graph
G = nx.Graph()

# Add nodes and edges
for session in sessions:
    device = session["Device"]
    for app in session["apps"]:
        G.add_node(device, type="Device")
        G.add_node(app, type="App")
        G.add_edge(device, app)  # Connect device to the app

pos = nx.spring_layout(G, k=0.8)  # Smaller 'k' results in shorter edges

# Visualize the graph
plt.figure(figsize=(10, 8))
pos = nx.spring_layout(G)  # Layout for better visual spacing

# Get node types for coloring
node_colors = ["skyblue" if G.nodes[node]["type"] == "Device" else "lightgreen" for node in G.nodes]

# Draw the network
nx.draw(
    G, pos,
    with_labels=True,
    node_color=node_colors,
    node_size=1500,
    font_size=10,
    font_weight="bold",
    edge_color="gray",
    
)

# Add legend
legend_labels = {"Devices": "skyblue", "Apps": "lightgreen"}
for label, color in legend_labels.items():
    plt.scatter([], [], color=color, label=label)
plt.legend(scatterpoints=1, loc="upper right", fontsize=12)

plt.title("Network Graph: Device-App Relationship")
# plt.tight_layout()
plt.savefig("device_app_network_graph.png")  # Save the graph as PNG
