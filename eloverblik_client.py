from requests import get, post
from config_handler import read_from_config, write_to_config

class MyEnergyClient:

    def __init__(self) -> None:
        self.__api_path = 'https://api.eloverblik.dk/customerapi/api'

    def __get_new_access_token(self) -> str:
        refresh_token = read_from_config('refreshtoken')

        res = get(
            url=f'{self.__api_path}/token',
            headers={
                'Authorization': f'Bearer {refresh_token}'
            }
        )

        return res.json()['result']
    
    def __execute_post_query(self, endpoint_path: str, data=None):
        succes = False
        failed_attempts = 0
        res = None
        
        while succes == False and failed_attempts < 2:
            access_token = read_from_config('accesstoken')
            res = post(
                url=f'{self.__api_path}/{endpoint_path}',
                headers={
                    'Authorization': f'Bearer {access_token}'
                },
                json=data
            )

            if res.status_code == 401:
                print("Unauthorized. Updating access token and retrying ...")
                self.update_access_token()
                failed_attempts += 1
            else:
                succes = True

        return res.json()

    def update_access_token(self) -> None:
        new_access_token = self.__get_new_access_token()
        write_to_config('accesstoken', new_access_token)

    def get_metering_point_details(self, mentering_point_id: str) -> str:
        
        return self.__execute_post_query(
            endpoint_path='meteringpoints/meteringpoint/getdetails',
            data={
                'meteringPoints': {
                    'meteringPoint': [
                        mentering_point_id
                    ]
                }
            }
        )

    def get_time_series(self, mentering_point_id: str, start_date: str, end_date: str, aggr='Actual') -> str:
        
        return self.__execute_post_query(
            endpoint_path=f'meterdata/gettimeseries/{start_date}/{end_date}/{aggr}',
            data={
                'meteringPoints': {
                    'meteringPoint': [
                        mentering_point_id
                    ]
                }
            }
        )

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