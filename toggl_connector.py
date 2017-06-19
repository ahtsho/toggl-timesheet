__author__ = 'ahadu_tsegaye'

import json,urllib2,urllib
import utils

class TConnector():

    @staticmethod
    def get_api():
        return json.loads(open('config/toggl.api.json', 'r').read())

    @staticmethod
    def get_header():
        authHeader = open('config/api.key', 'r').read().strip() + ":" + "api_token"
        authHeader = "Basic %s" % authHeader.encode("base64").rstrip()
        return {"Authorization": authHeader}

    @staticmethod
    def get_header_w_json_type():
        headers = TConnector.get_header();
        headers['Content-Type'] = 'application/json'
        return headers

    @staticmethod
    def do_get_request_w_id(service, obj_id):
        req = urllib2.Request(TConnector.get_api()['base_url'] + service + '/' + str(obj_id),
                          headers=TConnector.get_header())
        return json.loads(urllib2.urlopen(req).read())

    @staticmethod
    def get_workspace_name_by_id(obj_id):
        return TConnector.do_get_request_w_id(TConnector.get_api()['services']['w'], obj_id)['data']['name']

    @staticmethod
    def get_project_info_by_id(obj_id):
        name = None
        cid = None
        if obj_id:
            resp = TConnector.do_get_request_w_id(TConnector.get_api()['services']['p'], obj_id)
            data = utils.get_value_if_key_exists('data', resp)
            if data:
                name = utils.get_value_if_key_exists('name', data)
                cid = utils.get_value_if_key_exists('cid', data)
        return name, cid

    @staticmethod
    def get_client_name_by_id(obj_id):
        resp = None
        if obj_id:
            resp = TConnector.do_get_request_w_id(TConnector.get_api()['services']['c'], obj_id)['data']['name']
        return resp

    @staticmethod
    def get_time_entries_json(params):
        request = urllib2.Request(TConnector.get_api()['base_url'] +
                                  TConnector.get_api()['services']['t_e'] + '?%s' % urllib.urlencode(params),
        headers=TConnector.get_header())
        return json.loads(urllib2.urlopen(request).read())

    @staticmethod
    def get_workspace_ids():
        workspaces_url = TConnector.get_api()['base_url'] + TConnector.get_api()['services']['w']
        request = urllib2.Request(workspaces_url,headers=TConnector.get_header())
        response = urllib2.urlopen(request)
        workspaces = json.loads(response.read())
        wids = []
        for workspace in workspaces:
            wids.append(workspace['id'])
        return wids

    @staticmethod
    def add_tag_to_workspace(tag_data):
        request = urllib2.Request(TConnector.get_api()['base_url'] + TConnector.get_api()['services']['t'],
                                  json.dumps(tag_data),headers=TConnector.get_header_w_json_type())
        response = urllib2.urlopen(request)
        return response.read()