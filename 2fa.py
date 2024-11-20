import json
from datetime import datetime

sec_path = "security_and_login_information"

## -----------------2FA-----------------
fa = open("2FA Status" , "w")
print("2FA Status:\n", file=fa)

with open(sec_path + "/two-factor_authentication.json") as f:
    data = json.load(f)


# Extract the state and enabled time if available
state = next((item['value'] for item in data['label_values'] if item['ent_field_name'] == 'State'), 'Disabled')
enabled_timestamp = next((item['timestamp_value'] for item in data['label_values'] if item['ent_field_name'] == 'EnabledTime'), None)

# Check if two-factor authentication is enabled and display the appropriate message
if state == 'Enabled' and enabled_timestamp:
    enabled_date = datetime.fromtimestamp(enabled_timestamp).strftime('%B %d, %Y')
    print(f"Two-factor authentication is enabled since {enabled_date}." , file=fa)
else:
    print("Two-factor authentication is not enabled." , file =fa)

fa.close()