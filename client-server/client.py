import config
import requests
from utils import KeysPool


class ClientManger(object):
    """
    Main client class, which give access to all available APIs 
    """
    def __init__(self):
        self.keys = KeysPool()
        self.providers = {
            'api_A': ApiA(config.HOST, config.PORTS[0], self.keys),
            'api_B': ApiB(config.HOST, config.PORTS[1], self.keys)
        }


class BaseApi(object):
    def __init__(self, host, port, keys):
        self.keys = keys
        self.host = host
        self.port = port
        self.key = self.keys.acquire()
        self.response = None

    def process(self):
        """
        API client entry point
        """
        try:
            self.response = self.send('api-call')
            self.keys.release(self.key)
            return self.process_response()
        except Exception as e:
            print e
        return False

    def send(self, path):
        """
        Make HTTP request to server
        """
        return requests.get('http://{0}:{1}/{2}?key={3}'.format(self.host, self.port, path, self.key))

    def process_response(self):
        """
        Check and log response
        """
        print ('CLIENT LOG: Request to {0} | Response : {1}'.format(self.response.request.url , self.response.content))
        if self.response.status_code == 200:
            return True
        else:
            return False


class ApiA(BaseApi):
    """
    custom class for API A can be used for customization
    """
    pass


class ApiB(BaseApi):
    """
    custom class for API B  can be used for customization
    """
    pass
