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

    def get_metering_point_details(self, mentering_point_id, attempt=1) -> str:
        access_token = read_from_config('accesstoken')

        res = post(
            url=f'{self.api_path}/meteringpoints/meteringpoint/getdetails',
            headers={
                'Authorization': f'Bearer {access_token}'
            },
            json={
                'meteringPoints': {
                    'meteringPoint': [
                        mentering_point_id
                    ]
                }
            }
        )

        if res.status_code == 401 and attempt == 1:
            print("Unauthorized. Updating access token and retrying ...")
            self.update_access_token()

            return self.get_metering_point_details(mentering_point_id, attempt=2)

        return res.json()

    def get_time_series(self, mentering_point_id: str, start_date: str, end_date: str, aggr='Actual', attempt=1) -> str:
        access_token = read_from_config('accesstoken')

        res = post(
            url=f'{self.api_path}/meterdata/gettimeseries/{start_date}/{end_date}/{aggr}',
            headers={
                'Authorization': f'Bearer {access_token}'
            },
            json={
                'meteringPoints': {
                    'meteringPoint': [
                        mentering_point_id
                    ]
                }
            }
        )

        if res.status_code == 401 and attempt == 1:
            print("Unauthorized. Updating access token and retrying ...")
            self.update_access_token()

            return self.get_metering_point_details(mentering_point_id, attempt=2)

        return res.json()


# ===== MANUAL TESTING =====

client = MyEnergyClient()

# ===== TEST: Update access token =====
# client.update_access_token()
# access_token = read_from_config('accesstoken')
# print(access_token)

# ===== TEST: Get metering point details =====
# metering_point_id = read_from_config('meteringpointid')
# metering_point_details = client.get_metering_point_details(metering_point_id)
# print(metering_point_details)

# ===== TEST: Get time series =====
metering_point_id = read_from_config('meteringpointid')
time_series = client.get_time_series(metering_point_id, '2022-04-01', '2022-04-02')
print(time_series)