REQUIRED SOFTWARE:
# python2

TOGGL CONFIGURATION
# Open a www.toggl.com account with your Bridge gmail account.
# Get your API token from https://www.toggl.com/app/profile and save it into config/api.key
# Create a workspace for each Job Order you're working on. The workspaces have to be named exactly as on Bridge portal's timesheet input "Commessa"
# Associate a Client to each of your workspaces. The clients have to be named exactly as on Bridge portal's timesheet input "Azienda"
# Form within each workspace create all your Projects and associate them with a client. The projects have to be named exactly as on Bridge portal's timesheet input "Sottocommessa"
# Run add_bridge_activities_as_toggle_tags.py to create tags (Activities) in all your workspaces.

SUBMIT TIMESHEET
# Run toggler.py passing it the date.