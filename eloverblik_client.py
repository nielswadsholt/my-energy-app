from mimetypes import init
from requests import get, post
from config_handler import read_from_config, write_to_config

class MyEnergyClient:

    def __init__(self) -> None:
        self.api_path = 'https://api.eloverblik.dk/customerapi/api'

    def get_new_access_token(self) -> str:
        refresh_token = read_from_config('refreshtoken')

        res = get(
            url=f'{self.api_path}/token',
            headers={
                'Authorization': f'Bearer {refresh_token}'
            }
        )

        return res.json()['result']

    def update_access_token(self) -> None:
        new_access_token = self.get_new_access_token()
        write_to_config('accesstoken', new_access_token)

    def get_metering_point_details(self, mentering_point_id) -> str:
        access_token = read_from_config('accesstoken')

        res = post(
            url=f'{self.api_path}/meteringpoints/meteringpoint/getdetails',
            headers={
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            },
            json={
                'meteringPoints': {
                    'meteringPoint': [
                        mentering_point_id
                    ]
                }
            }
        )

        return res.json()

client = MyEnergyClient()

# ===== TEST: Update access token =====
client.update_access_token()
access_token = read_from_config('accesstoken')
print(access_token)

# ===== TEST: Get metering point details =====
metering_point_id = read_from_config('meteringpointid')
metering_point_details = client.get_metering_point_details(metering_point_id)
print(metering_point_details)