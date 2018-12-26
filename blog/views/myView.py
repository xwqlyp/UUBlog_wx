import requests


url='http://goeasy.io/goeasy/publish'
parms={
        'appkey':'BC-2a4759e3e1d245d99ab0fb9316090594',
        'channel':'你好',
        'content':'123',
}
requests.post(url,parms)
