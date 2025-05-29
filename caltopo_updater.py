import requests
from random import randrange
from time import sleep

class CTUpdater():
    def __init__(self, caltopo_connect_key):
        if not caltopo_connect_key:
            print("NO KEY, BAD")
        self.key = caltopo_connect_key

    def update_position(self,id, lat, long):
        resp = requests.get(
            f"https://caltopo.com/api/v1/position/report/{self.key}?id={id}&lat={lat}&lng={long}")
        resp.raise_for_status()


def simple_test():
    from conf import caltopo_connect_key
    caltopo = CTUpdater(caltopo_connect_key)

    while(True):
        ids = ["MYDEVICE90sdf980sdf890sdf0zz", "MYDEVICE"]
        for id in ids:
            lat = "45.92" + str(randrange(1000))
            long = "-66.64" + str(randrange(1000))
            caltopo.update_position(id, lat, long)

        sleep(15)

if __name__ == '__main__':
    simple_test()


