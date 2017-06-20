__author__ = 'Ahadu Tsegaye Abebe - 20/06/17'


from toggl_connector import TConnector
import utils

wids = TConnector.get_workspace_ids()
for wid in wids:
    tags = utils.read_file_as_list('activities.txt')
    for tag in tags:
        try:
            print TConnector.add_tag_to_workspace({'tag': {'name': tag, 'wid': wid}})
        except Exception as e:
            print e