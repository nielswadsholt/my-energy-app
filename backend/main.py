from my_energy_client import MyEnergyClient
from config_handler import read_from_config

if __name__ == "__main__":

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