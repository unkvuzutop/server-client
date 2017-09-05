import json
import config

class BaseStorage(object):
    """
    Parent class for any storage
    """
    def __init__(self, storage_path):
        self.storage_path = storage_path

    def get_keys(self):
        """
        load keys from current storage class
        """
        pass


class JsonStorage(BaseStorage):
    def get_keys(self):
        try:
            data = json.loads(open(self.storage_path).read())
            print('STORAGE LOG: loaded data from storage - %s' % data)
            return data.get('keys')
        except Exception as e:
            raise e


class KeysPool(object):
    def __init__(self):
        self.storage = None

        if config.KEY_STORAGE_TYPE == 'json':
            self.storage = JsonStorage(config.STORAGE_LINK)

        self.keys = self.storage.get_keys()
        self._pool_keys = [i.get('key') for i in self.keys]

    def acquire(self):
        """
        Take key from Poll
        """
        key = self._pool_keys.pop()
        print('POOL log: acquired key - %s' % key)
        return key

    def release(self, key):
        """
        :return given key to Pool
        """
        self._pool_keys.append(key)
        print('POOL LOG: released key - %s' % key)
