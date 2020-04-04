#pylint: disable=bad-whitespace,too-many-arguments,import-outside-toplevel,dangerous-default-value

"""
Utility functions
"""


import datetime
import pandas as pd


def get_daily_data(
        request=None,
        date=None,
        country='Poland',
        url: str='https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports',#pylint: disable=line-too-long
        extension: str='csv',
        country_col='Combined_Key',
        out_cols=[
            'Confirmed',
            'Deaths',
            'Recovered',
            'Active',
        ],
):
    """
    Return data for a given day
    """
    if request is None:
        pass
    one_day = datetime.timedelta(1)
    if date is None:
        date = datetime.datetime.today() - one_day
    country = country.title()
    today_csv_url = '/'.join((
        url.rstrip('/'),
        '{:02d}-{:02d}-{}.{}'.format(
            date.month,
            date.day,
            date.year,
            extension,
        ),
    ))
    today_csv = pd.read_csv(today_csv_url)
    return today_csv[
        (today_csv[country_col] == country)
    ][out_cols].to_json(orient='records')
