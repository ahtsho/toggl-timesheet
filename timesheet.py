class TimesheetEntry:

    _total_daily_hours= 0.0

    def __init__(self,  date='09/09/2016', activity='NO_ACTIVITY', company='NO_COMPANY',
                 job_order='NO_JOB_ORDER', sub_job_order='NO_SUB_JOB_ORDER', description='NO_DESCRIPTION',
                 number_of_hours='0,0'):
        self.date = date
        self.activity = activity
        self.company = company
        self.job_order = job_order
        self.sub_job_order = sub_job_order
        self.description = description
        self.number_of_hours = number_of_hours

    @staticmethod
    def increment_tot_day_hours(more_hrs):
        TimesheetEntry._total_daily_hours += float(more_hrs)

    @staticmethod
    def get_tot_day_hours():
        return str(TimesheetEntry._total_daily_hours).replace(".",",")

    def to_string(self):
        return 'date: {}, ' \
               'activity: {}, ' \
               'company: {}, ' \
               'joborder: {}, ' \
               'subjoborder: {}, ' \
               'description: {}, ' \
               'hours: {}'.format(self.date,
                                  self.activity,
                                  self.company,
                                  self.job_order,
                                  self.sub_job_order,
                                  self.description,
                                  self.number_of_hours)
