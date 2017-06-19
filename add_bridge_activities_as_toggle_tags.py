import urllib2, json

configs = json.loads(open('app.cfg', 'r').read())
authHeader = configs['API_KEY'] + ":" + "api_token"
authHeader = "Basic %s" % authHeader.encode("base64").rstrip()


def read_file_as_list(filename):
    with open(filename) as data_file:
        data_list = data_file.readlines()
    return [x.strip() for x in data_list]


def get_workspace_ids():
    workspaces_url = configs['time_tracker_url']+'workspaces'
    request = urllib2.Request(workspaces_url,headers={"Authorization": authHeader})
    response = urllib2.urlopen(request)
    workspaces = json.loads(response.read())
    wids = []
    for workspace in workspaces:
        wids.append(workspace['id'])
    return wids


def add_tags_to_workspace(wid, tags_file):
    tags = read_file_as_list(tags_file)

    tags_url = configs['time_tracker_url']+'tags'

    for tag in tags:
        tag_data = {'tag':{'name':tag,'wid':wid}}
        request = urllib2.Request(tags_url,json.dumps(tag_data),headers={"Authorization": authHeader,'Content-Type': 'application/json'})
        try:
            response = urllib2.urlopen(request)
            print response.read()
        except Exception as e:
           print e


wids = get_workspace_ids()
for id in wids:
    add_tags_to_workspace(id, 'test_tags.txt')
