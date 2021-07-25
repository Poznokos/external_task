import requests


class HBD:

    body_url = "https://p9fwi1d77e.execute-api.eu-west-1.amazonaws.com/Prod/next-birthday?"

    @staticmethod
    def get_info(**param):
        response = requests.get(HBD.body_url, params=param, verify=False)

        return response


