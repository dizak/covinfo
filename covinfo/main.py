#pylint: disable=bad-whitespace,too-many-arguments,import-outside-toplevel,dangerous-default-value,line-too-long

"""
Utility functions
"""


import datetime
import pandas as pd


def get_daily_data(
        request=None,
        date=None,
        country='Poland',
        url: str='https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports',
        extension: str='csv',
        country_col='Combined_Key',
        cols={
            'conf': 'Confirmed',
            'deaths': 'Deaths',
            'recov': 'Recovered',
            'active': 'Active',
        },
        recoveryrate=False,
):
    """
    Return data for a given day
    """
    if 'country' in request.args:
        country = request.args.get('country')
    if 'recoveryrate' in request.args:
        recoveryrate = True
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
    today_country_csv = today_csv[
        (today_csv[country_col] == country)
    ][list(cols.values())]
    if recoveryrate:
        return str(float(today_country_csv[cols['recov']] / today_country_csv[cols['conf']] * 100))
    return today_country_csv.to_json(orient='records')


def get_changerate(
        request=None,
        url='https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports',
        extension='csv',
):
    """
    Get change rate of new cases from last 10 days
    """
    deltas = tuple(datetime.timedelta(i) for i in range(1, 15))
    dates = tuple(datetime.datetime.today() - i for i in deltas)
    csv_urls = tuple(
        '/'.join((
            url.rstrip('/'),
            '{:02d}-{:02d}-{}.{}'.format(
                i.month,
                i.day,
                i.year,
                extension,
            ),
        ))
        for i in dates
    )
    csvs = pd.concat(tuple(pd.read_csv(i) for i in csv_urls),).reset_index(drop=True)
    return csvs[(csvs['Combined_Key'] == 'Poland')]['Active'][::-1].pct_change().to_json(orient='records')
