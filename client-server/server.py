import config

from utils import JsonStorage
from bottle import route, run, template, request


class Server(object):
    @staticmethod
    def load_keys():
        """
        :return  all auth keys from storage
        """
        storage = None
        if config.KEY_STORAGE_TYPE == 'json':
            storage = JsonStorage(config.STORAGE_LINK)

        keys = [i.get('key') for i in storage.get_keys()]
        return keys

    @staticmethod
    def is_allowed_request(key, keys):
        """
        simple validations for given auth_key
        """
        return key in keys

    @route('/api-call', method='GET')
    def api(key=None):
        """
        API entry point
        """
        if not request.get('auth_keys'):
            request['auth_keys'] = Server.load_keys()
        auth_key = request.GET.get("key")
        if Server().is_allowed_request(auth_key, request.get('auth_keys')):
            return template('Server got valid key - {{key}}</b>!', key=auth_key)
        else:
            return template('Server got NOT VALID key - {{key}}</b>!', key=auth_key)

    @staticmethod
    def run(port):
        """
        start bottle HTTP server
        """
        run(host=config.HOST, port=port)
