from caltopo_updater import CTUpdater
from zello_position_getter import zello_locator
from conf import caltopo_connect_key, zello_api_key, zello_network, zello_username, zello_password
from pprint import pprint


try:
    z = zello_locator(zello_api_key,zello_network)
    ct = CTUpdater(caltopo_connect_key)
    print(z.get_token())
    print(z.login(zello_username, zello_password))
    z_locs = z.location_all_active()
    for loc in z_locs:
        pprint(loc)
        id = loc['username']
        lat = loc['latitude']
        long = loc['longitude']
        print(f"ID: {id}; LAT: {lat}; LONG: {long}")
        ct.update_position(id, lat, long)
except:
    print(z.logout())
    raise