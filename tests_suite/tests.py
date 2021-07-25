import pytest
from .helpers import get_standard_result_message
from http import HTTPStatus
from src.API.hbd_api import HBD
from datetime import datetime, timezone, timedelta

time_zone = +2.0
date_timezone = timezone(timedelta(hours=time_zone))

class TestSuite:
    CASE_TIMEOUT = 1 * 60  # one minute in seconds
    current_date = datetime.now(date_timezone).strftime('%Y-%m-%d')

    @pytest.mark.parametrize('date_of_birth', [current_date, '1999-08-01', '2001-07-27', '1991-04-13'])
    def test_positive_hour_unit(self, date_of_birth, unit='hour'):
        baseTestResult = HBD.get_info(dateofbirth=date_of_birth, unit=unit)
        res = baseTestResult.json().get('message')
        assert res == get_standard_result_message(date_of_birth, unit), f'Wrong result:{res}'

    @pytest.mark.parametrize('date_of_birth', [current_date, '1999-08-01', '2001-07-25', '1991-04-13'])
    def test_positive_day_unit(self, date_of_birth, unit='day'):
        baseTestResult = HBD.get_info(dateofbirth=date_of_birth, unit=unit)
        res = baseTestResult.json().get('message')
        assert res == get_standard_result_message(date_of_birth, unit), f'Wrong result:{res}'

    @pytest.mark.parametrize('date_of_birth', [current_date, '1999-08-01', '1999-08-02', '1991-04-24'])
    def test_positive_week_unit(self, date_of_birth, unit='week'):
        baseTestResult = HBD.get_info(dateofbirth=date_of_birth, unit=unit)
        res = baseTestResult.json().get('message')
        assert res == get_standard_result_message(date_of_birth, unit), f'Wrong result:{res}'

    @pytest.mark.parametrize('date_of_birth', [current_date, '1999-08-01', '1999-08-25', '1991-10-13'])
    def test_positive_month_unit(self, date_of_birth, unit='month'):
        baseTestResult = HBD.get_info(dateofbirth=date_of_birth, unit=unit)
        res = baseTestResult.json().get('message')
        assert res == get_standard_result_message(date_of_birth, unit), f'Wrong result:{res}'


#NEGATIVE TESTS
#There are no requirements for response statuses and messages so if scenarios are invalid we don't expect status 200 OK

    @pytest.mark.parametrize('unit', ['year', 'smth', 'Month'])
    def test_wrong_unit(self, unit, date_of_birth='1991-04-13'):
        baseTestResult = HBD.get_info(dateofbirth=date_of_birth, unit=unit)
        res = baseTestResult.status_code
        assert res != HTTPStatus.OK, f'Status is OK though unit param is invalid'

    @pytest.mark.parametrize('date_of_birth', ['1999-08-01 23:45:04', '2001-07-07 23-45', '2001-25-07', '04-13',
                                               '1999-08', '01-08-1999', '2001:07:07', '2003-5-4'])
    def test_wrong_date_format(self, date_of_birth, unit='day'):
        baseTestResult = HBD.get_info(dateofbirth=date_of_birth, unit=unit)
        msg = baseTestResult.json().get('message')
        res = baseTestResult.status_code
        assert res != HTTPStatus.OK, f'Status is OK though dateofbirth param is invalid. {msg}'

    @pytest.mark.parametrize('date_of_birth', ['2025-12-12', '10000-12-12'])
    def test_wrong_date_from_future(self, date_of_birth, unit='month'):
        baseTestResult = HBD.get_info(dateofbirth=date_of_birth, unit=unit)
        res = baseTestResult.status_code
        assert res != HTTPStatus.OK, f'Status is OK though dateofbirth is greater then current date'

    @pytest.mark.parametrize('date_of_birth', ['1987-02-30', '1996-12-32'])
    def test_wrong_impossible_date(self, date_of_birth, unit='month'):
        baseTestResult = HBD.get_info(dateofbirth=date_of_birth, unit=unit)
        res = baseTestResult.status_code
        assert res != HTTPStatus.OK, f'Status is OK though dateofbirth is non exist'

    @pytest.mark.parametrize('date_of_birth, unit', [('1999-08-01', ''), ('', 'month'), ('', '')])
    def test_empty_parameters(self, date_of_birth, unit):
        baseTestResult = HBD.get_info(dateofbirth=date_of_birth, unit=unit)
        res = baseTestResult.status_code
        assert res != HTTPStatus.OK, f'Status is OK though params are invalid.'


#STRESS TEST

    def test_big_request(self):
        baseTestResult = HBD.get_info(dateofbirth='1991-04-13', unit='a'*1000000)
        res = baseTestResult.status_code
        assert res == HTTPStatus.REQUEST_URI_TOO_LONG, f'Status is OK though REQUEST URI TOO LONG'
        baseTestResult = HBD.get_info(dateofbirth='1991-04-13', unit='month')
        res = baseTestResult.json().get('message')
        assert res == get_standard_result_message('1991-04-13', 'month'), f'Wrong result:{res}'

#PERFOMANCE TESTS

    def test_perf_check(self, date_of_birth='2001-07-07', unit='week'):
        i = 0
        while i < 100:
            baseTestResult = HBD.get_info(dateofbirth=date_of_birth, unit=unit)
            res = baseTestResult.json().get('message')
            assert res == get_standard_result_message(date_of_birth, unit), f'Wrong result:{res}'
            i = i + 1


#SECURITY TESTS

    def test_sec_test(self, unit='week', date_of_birth='<script>alert("Pwned")</script>'):
        baseTestResult = HBD.get_info(dateofbirth=date_of_birth, unit=unit)
        res = baseTestResult.status_code
        msg = baseTestResult.json().get('message')
        assert res != HTTPStatus.OK, f'Status is OK though params are invalid. {msg}'
