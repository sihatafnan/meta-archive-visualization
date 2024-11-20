import json
from datetime import datetime
import matplotlib.pyplot as plt
from collections import Counter
import matplotlib.dates as mdates


##------------------off facebook activity----------------
off_facebook_activity = []
with open('apps_and_websites_off_of_facebook/your_activity_off_meta_technologies.json', 'r') as file:
    data = json.load(file)
    off_facebook_activity = data.get('off_facebook_activity_v2', [])

# Aggregate events by platform
platform_event_counts = Counter()
event_type_counts = Counter()

for entry in off_facebook_activity:
    platform_event_counts[entry["name"]] += len(entry["events"])
    for event in entry["events"]:
        event_type_counts[event["type"]] += 1

#remove those events whose count is less than 5
platform_event_counts = {platform: count for platform, count in platform_event_counts.items() if count >= 5}
# Bar Chart: Events by Platform
"""
Count the total number of events for each platform (name) and display them in a bar chart.
This gives a quick overview of which platforms the user interacts with the most.
"""
plt.figure(figsize=(8, 6))
plt.bar(platform_event_counts.keys(), platform_event_counts.values(), color='skyblue')
plt.title('Number of Events by Platform')
plt.xlabel('Platform')
plt.ylabel('Number of Events')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('events_by_platform_bar_chart.png')  # Save bar chart as PNG


##------------------connected apps----------------
"""
The data in connected_apps_and_websites.json provides insights into apps and websites 
connected to the user's Facebook account. These visualizations can help users understand 
their privacy exposure and take action if needed.
"""

installed_apps = []
with open('apps_and_websites_off_of_facebook/connected_apps_and_websites.json', 'r') as file:
    data = json.load(file)
    installed_apps = data.get('installed_apps_v2', [])

# Convert timestamps to datetime
def convert_timestamp(timestamp):
    if timestamp == 0:
        return None  # No timestamp provided
    return datetime.fromtimestamp(int(timestamp))  # Ensure it's converted to int

# Prepare data for plotting
app_names = []
durations = []
colors = []

for app in installed_apps:
    added_time = convert_timestamp(app["added_timestamp"]) or datetime.now()  # Use current date if no added_timestamp
    removed_time = convert_timestamp(app["removed_timestamp"]) or datetime.now()  # Use current date if active
    duration = (added_time, removed_time)
    
    app_names.append(app["name"])
    durations.append(duration)
    
    # Assign color based on category
    if app["category"] == "active":
        colors.append("green")
    elif app["category"] == "inactive":
        colors.append("orange")
    elif app["category"] == "removed":
        colors.append("red")

# Create the plot
plt.figure(figsize=(12, 6))
for i, (name, duration, color) in enumerate(zip(app_names, durations, colors)):
    plt.barh(name, (duration[1] - duration[0]).days, left=mdates.date2num(duration[0]), color=color)

# Format the x-axis with readable dates
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %d, %Y'))
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=3))
plt.xlabel("Date")
plt.ylabel("Apps")
plt.title("Connected App Duration and Status")
plt.grid(axis="x", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.legend(["Active", "Inactive", "Removed"], loc="upper right")
plt.savefig('Connected_app_duration_status.png')  # Save the plot as PNG

