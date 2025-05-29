from caltopo_updater import CTUpdater
from zello_position_getter import zello_locator
# from conf import caltopo_connect_key, zello_api_key, zello_network, zello_username, zello_password
from pprint import pprint
from time import sleep
import traceback
import datetime

caltopo_connect_key = input("caltopo_connect_key: ")
zello_api_key = input("zello_api_key: ")
zello_network = input("zello_network: ")
zello_username = input("zello_username: ")
zello_password = input("zello_password: ")




try:
    z = zello_locator(zello_api_key, zello_network)
    z.get_token()
    z.login(zello_username, zello_password)
    print("Zello Login Successful")
    ct = CTUpdater(caltopo_connect_key)
    print("Caltopo Initialized")
    while(True):
        z_locs = z.location_all_active()
        print(f"Updating the following users {datetime.datetime.now()}:")
        for loc in z_locs:
            id = loc['username']
            lat = loc['latitude']
            long = loc['longitude']
            print(f"ID: {id}; LAT: {lat}; LONG: {long}")
            ct.update_position(id, lat, long)
        sleep(60)

except Exception as e:
    print(traceback.format_exc())
    print("An unexpected error occurred:", e)

finally:
    input("Press Enter to exit...")
    print(z.logout())