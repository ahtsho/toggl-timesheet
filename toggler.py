import urllib, urllib2, json, sys
from dateutil.parser import parse
from datetime import timedelta
from timesheet import TimesheetEntry

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
    name = None
    cid = None
    if obj_id:
        resp = do_get_request_w_id(api['services']['p'], obj_id)
        data = get_value_if_key_exists('data', resp)
        if data:
            name = get_value_if_key_exists('name', data)
            cid = get_value_if_key_exists('cid', data)
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
    ts = []

    for entry in response:
        project, cid = get_project_info_by_id(get_value_if_key_exists('pid', entry))
        hours = convert_to_bridge_format(get_value_if_key_exists('duration', entry))
        timesheet_entry =  TimesheetEntry(parse(params['start_date']).strftime("%d/%m/%Y"),
                                          get_value_if_key_exists('tags', entry),
                                          get_client_name_by_id(cid),
                                          get_workspace_name_by_id(get_value_if_key_exists('wid', entry)),
                                          project,
                                          get_value_if_key_exists('description', entry),
                                          hours)
        TimesheetEntry.increment_tot_day_hours(hours.replace(",","."))
        ts.append(timesheet_entry)

    return ts

date_in = str(raw_input("Which day would you like to submit. Use format dd/mm/yyyy\n"))

ts_entries = get_timesheet_entries(str(date_in))

for ts in ts_entries:
    print ts.to_string()
print TimesheetEntry.get_tot_day_hours()