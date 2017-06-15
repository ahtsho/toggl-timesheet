import urllib, urllib2, json
from dateutil.parser import parse

configs = json.loads(open('app.cfg', 'r').read())


def do_get_request_w_id(service, obj_id):
    req = urllib2.Request(configs['time_tracker_url'] + service + '/' + str(obj_id),
                          headers={"Authorization": authHeader})
    return json.loads(urllib2.urlopen(req).read())


def get_workspace_name_by_id(obj_id):
    return do_get_request_w_id(configs['workspace_service'], obj_id)['data']['name']


def get_project_info_by_id(obj_id):
    resp = do_get_request_w_id(configs['project_service'], obj_id)
    return resp['data']['name'], response['data']['cid']


def get_client_name_by_id(obj_id):
    return do_get_request_w_id(configs['client_service'], obj_id)['data']['name']


def convert_to_bridge_format(duration_sec):
    h, m_tmp = divmod(float(duration_sec) / 3600, 1)
    m = convert_to_quarters(m_tmp * 60)
    return '{},{}'.format(int(h), int(m))


def convert_to_quarters(minutes):
    m = -1
    if minutes < 15:
        m = 0
    elif minutes < 30:
        m = 25
    elif minutes < 45:
        m = 50
    elif minutes < 60:
        m = 75
    return m


configs = json.loads(open('app.cfg', 'r').read())
authHeader = configs['API_KEY'] + ":" + "api_token"
authHeader = "Basic %s" % authHeader.encode("base64").rstrip()

params = {'start_date': '2017-06-01T07:00:00+00:00', 'end_date': '2017-06-01T20:00:00+00:00'}

request = urllib2.Request(
    configs['time_tracker_url'] + configs['time_entries_service'] + '?%s' % urllib.urlencode(params),
    headers={"Authorization": authHeader})

response = json.loads(urllib2.urlopen(request).read())

timesheet = []

for entry in response:

    if entry['tags']:
        tags = entry['tags']

    wid = entry['wid']
    pid = entry['pid']
    duration = entry['duration']
    description = entry['description']
    workspace = get_workspace_name_by_id(wid)
    project, cid = get_project_info_by_id(pid)
    client = get_client_name_by_id(cid)
    timesheet_entry = {'date': parse(params['start_date']).strftime("%d/%m/%Y"),
                       'activity': tags,
                       'company': client,
                       'job_order': workspace,
                       'sub_job_order': project,
                       'numberOfHours': convert_to_bridge_format(duration)}
    timesheet.append(timesheet_entry)

print timesheet
