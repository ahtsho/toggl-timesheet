import urllib,urllib2, json

configs  = json.loads(open('app.cfg', 'r').read())

authHeader = configs['API_KEY'] + ":" + "api_token"
authHeader = "Basic %s"%authHeader.encode("base64").rstrip()

params={}
if(configs['from']):
	params['start_date']=configs['from']
else:
	params['start_date'] = '2017-06-01T07:00:00+00:00'
if(configs['to']):
	params['end_date']=configs['to']
else:
	params['end_date']='2017-06-01T20:00:00+00:00'

request = urllib2.Request(configs['time_traker_url']+configs['time_entries_service']+'?%s'%urllib.urlencode(params), headers={"Authorization" : authHeader})

print urllib2.urlopen(request).read()
