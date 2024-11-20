import json
import matplotlib.pyplot as plt
from collections import Counter

adds_path = "ads_information/"

##--------------advertisers using your info-----------------
with open(adds_path + 'advertisers_using_your_activity_or_information.json', 'r') as file:
    data = json.load(file)

advertisers_info = data.get("custom_audiences_all_types_v2", [])

# Pie Chart: Advertisers using one, two, or all three methods
targeting_combination_counts = Counter(
    (
        advertiser.get("has_data_file_custom_audience", False),
        advertiser.get("has_remarketing_custom_audience", False),
        advertiser.get("has_in_person_store_visit", False)
    )
    for advertiser in advertisers_info
)

# Label combinations for the pie chart
combination_labels = {
    (True, False, False): 'Only Custom Audience',
    (False, True, False): 'Only Remarketing',
    (False, False, True): 'Only In-Person Visit',
    (True, True, False): 'Custom Audience & Remarketing',
    (True, False, True): 'Custom Audience & In-Person Visit',
    (False, True, True): 'Remarketing & In-Person Visit',
    (True, True, True): 'All Three'
}

# Prepare labels and sizes for the pie chart
labels = []
sizes = []

for combination, count in targeting_combination_counts.items():
    label = combination_labels.get(combination, 'Unknown')
    labels.append(label)
    sizes.append(count)

# Plot the Pie Chart
plt.figure(figsize=(8, 6))
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
title = "You are being tracked by " + str(len(advertisers_info)) + " advertisors.\nProportion of Advertisers Using Different Combinations of Targeting Methods"
plt.title(title)
plt.savefig('targeting_methods_pie_chart.png')  # Save pie chart as PNG
plt.close()