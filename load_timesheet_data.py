__author__ = 'ahadu_tsegaye'

from dateutil.parser import parse
from datetime import timedelta
from timesheet import TimesheetEntry
import utils
from toggl_connector import TConnector


def get_timesheet_entries(date='09/09/2016'):
    start_date = parse(date)
    end_date = start_date + timedelta(hours=23, minutes=59)

    params = {'start_date': start_date.strftime('%Y-%m-%dT%H:%M:%S') + '+00:00',
              'end_date': end_date.strftime('%Y-%m-%dT%H:%M:%S') + '+00:00'}
    print "Building your timesheet for ", params

    response = TConnector().get_time_entries_json(params)

    ts = []

    for entry in response:
        project, cid = TConnector.get_project_info_by_id(utils.get_value_if_key_exists('pid', entry))
        hours = utils.convert_seconds_to_sexagesimals(utils.get_value_if_key_exists('duration', entry))
        timesheet_entry = TimesheetEntry(parse(params['start_date']).strftime("%d/%m/%Y"),
                                         utils.get_value_if_key_exists('tags', entry),
                                         TConnector.get_client_name_by_id(cid),
                                         TConnector.get_workspace_name_by_id(
                                             utils.get_value_if_key_exists('wid', entry)),
                                         project,
                                         utils.get_value_if_key_exists('description', entry),
                                         hours)
        TimesheetEntry.increment_tot_day_hours(hours.replace(",", "."))
        ts.append(timesheet_entry)

    return ts


date_in = str(raw_input("Which day would you like to submit. Use format dd/mm/yyyy\n"))

ts_entries = get_timesheet_entries(str(date_in))

for ts in ts_entries:
    print ts.to_string()
print TimesheetEntry.get_tot_day_hours()
