__author__ = 'ahadu_tsegaye'

import urllib, urllib2, json, sys
from dateutil.parser import parse
from datetime import timedelta
from timesheet import TimesheetEntry
import utils


class Connector():

    @staticmethod
    def get_api():
        return json.loads(open('config/toggl.api.json', 'r').read())

    @staticmethod
    def get_header():
        authHeader = open('config/api.key', 'r').read().strip() + ":" + "api_token"
        return "Basic %s" % authHeader.encode("base64").rstrip()

    @staticmethod
    def do_get_request_w_id(service, obj_id):
        req = urllib2.Request(Connector.get_api()['base_url'] + service + '/' + str(obj_id),
                          headers={"Authorization": Connector.get_header()})
        return json.loads(urllib2.urlopen(req).read())

    @staticmethod
    def get_workspace_name_by_id(obj_id):
        return Connector.do_get_request_w_id(Connector.get_api()['services']['w'], obj_id)['data']['name']

    @staticmethod
    def get_project_info_by_id(obj_id):
        name = None
        cid = None
        if obj_id:
            resp = Connector.do_get_request_w_id(Connector.get_api()['services']['p'], obj_id)
            data = utils.get_value_if_key_exists('data', resp)
            if data:
                name = utils.get_value_if_key_exists('name', data)
                cid = utils.get_value_if_key_exists('cid', data)
        return name, cid

    @staticmethod
    def get_client_name_by_id(obj_id):
        resp = None
        if obj_id:
            resp = Connector.do_get_request_w_id(Connector.get_api()['services']['c'], obj_id)['data']['name']
        return resp


def get_timesheet_entries(date='09/09/2016'):
    start_date = parse(date)
    end_date = start_date + timedelta(hours=23, minutes = 59)

    params = {'start_date': start_date.strftime('%Y-%m-%dT%H:%M:%S')+'+00:00',
              'end_date': end_date.strftime('%Y-%m-%dT%H:%M:%S')+'+00:00'}
    print "Building your timesheet for ", params

    request = urllib2.Request(
        Connector.get_api()['base_url'] + Connector.get_api()['services']['t_e'] + '?%s' % urllib.urlencode(params),
        headers={"Authorization": Connector.get_header()})

    response = json.loads(urllib2.urlopen(request).read())
    ts = []

    for entry in response:
        project, cid = Connector.get_project_info_by_id(utils.get_value_if_key_exists('pid', entry))
        hours = utils.convert_seconds_to_sexagesimals(utils.get_value_if_key_exists('duration', entry))
        timesheet_entry =  TimesheetEntry(parse(params['start_date']).strftime("%d/%m/%Y"),
                                          utils.get_value_if_key_exists('tags', entry),
                                          Connector.get_client_name_by_id(cid),
                                          Connector.get_workspace_name_by_id(utils.get_value_if_key_exists('wid', entry)),
                                          project,
                                          utils.get_value_if_key_exists('description', entry),
                                          hours)
        TimesheetEntry.increment_tot_day_hours(hours.replace(",","."))
        ts.append(timesheet_entry)

    return ts

date_in = str(raw_input("Which day would you like to submit. Use format dd/mm/yyyy\n"))

ts_entries = get_timesheet_entries(str(date_in))

for ts in ts_entries:
    print ts.to_string()
print TimesheetEntry.get_tot_day_hours()