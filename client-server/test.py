import multiprocessing as mp
from time import sleep


import config
from server import Server
from client import ClientManger


def test():
    api = ClientManger()

    api.providers['api_A'].process()
    api.providers['api_B'].process()


if __name__ == '__main__':
    """
    1. start webserver process for each given port 
    2. start test process and wait while it is alive
    3. stop all process
    """
    processes = [mp.Process(target=Server.run, args=([x])) for x in config.PORTS]
    
    test_process = mp.Process(target=test, args=())
    processes.append(test_process)
    
    for p in processes:
        p.start()

    while test_process.is_alive():
        print 'TEST LOG: test still alive' 
        sleep(1)

    for p in processes:
        p.terminate()
