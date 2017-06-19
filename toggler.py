import urllib, urllib2, json
from dateutil.parser import parse
from datetime import timedelta

api = json.loads(open('config/toggl.api.json', 'r').read())
authHeader = open('config/api.key', 'r').read().strip() + ":" + "api_token"
authHeader = "Basic %s" % authHeader.encode("base64").rstrip()


def do_get_request_w_id(service, obj_id):
    req = urllib2.Request(api['base_url'] + service + '/' + str(obj_id),
                          headers={"Authorization": authHeader})
    return json.loads(urllib2.urlopen(req).read())


def get_workspace_name_by_id(obj_id):
    return do_get_request_w_id(api['services']['w'], obj_id)['data']['name']


def get_project_info_by_id(obj_id):
    name = ''
    cid = None
    if obj_id:
        resp = do_get_request_w_id(api['services']['p'], obj_id)
        if 'data' in resp:
            if 'name' in resp['data']:
                name = resp['data']['name']
            if 'cid' in resp['data']:
                cid = resp['data']['cid']
    return name, cid


def get_client_name_by_id(obj_id):
    resp = None
    if obj_id:
        resp = do_get_request_w_id(api['services']['c'], obj_id)['data']['name']
    return resp


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


def get_value_if_key_exists(akey, amap):
    value = None
    if akey in amap:
        value = amap[akey]
    return value

def get_timesheet_entries(date='09/09/2016'):
    start_date = parse(date)
    end_date = start_date + timedelta(hours=23, minutes = 59)

    params = {'start_date': start_date.strftime('%Y-%m-%dT%H:%M:%S')+'+00:00',
              'end_date': end_date.strftime('%Y-%m-%dT%H:%M:%S')+'+00:00'}
    print "Building your timesheet for ", params

    request = urllib2.Request(
        api['base_url'] + api['services']['t_e'] + '?%s' % urllib.urlencode(params),
        headers={"Authorization": authHeader})

    response = json.loads(urllib2.urlopen(request).read())

    timesheet = []

    for entry in response:
        tags = get_value_if_key_exists('tags', entry)
        wid = get_value_if_key_exists('wid', entry)
        pid = get_value_if_key_exists('pid', entry)
        duration = get_value_if_key_exists('duration', entry)
        description = get_value_if_key_exists('description', entry)

        workspace = get_workspace_name_by_id(wid)
        project, cid = get_project_info_by_id(pid)
        client = get_client_name_by_id(cid)
        timesheet_entry = {'date': parse(params['start_date']).strftime("%d/%m/%Y"),
                           'activity': tags,
                           'company': client,
                           'job_order': workspace,
                           'sub_job_order': project,
                           'description': description,
                           'numberOfHours': convert_to_bridge_format(duration)}
        timesheet.append(timesheet_entry)

    return timesheet

date_in = str(raw_input("Which day would you like to submit. Use format dd/mm/yyyy\n"))
print date_in
print get_timesheet_entries(str(date_in))