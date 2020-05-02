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
        days_back=23,
        country='Poland',
        url='https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports',
        extension='csv',
):
    """
    Get change rate of new cases from last 10 days
    """
    js_template = """
    <html>
      <head>
        <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
        <script type="text/javascript">
          google.charts.load('current', {{'packages':['corechart']}});
          google.charts.setOnLoadCallback(drawChart);

          function drawChart() {{
            var data = google.visualization.arrayToDataTable({});

            var options = {{
              title: 'Number of Sick Daily Relative Change Rate in Poland',
              curveType: 'function',
              legend: {{ position: 'bottom' }}
            }};

            var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));

            chart.draw(data, options);
          }}
        </script>
      </head>
      <body>
        <div id="curve_chart" style="width: 900px; height: 500px"></div>
      </body>
    </html>
    """
    if 'days' in request.args:
        days_back = int(request.args.get('days'))
    if 'country' in request.args:
        country = request.args.get('country').title()
    deltas = tuple(datetime.timedelta(i) for i in range(2, days_back))
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
    csvs['Last_Update'] = pd.to_datetime(csvs['Last_Update'])
    csvs_country_inverted = csvs[(csvs['Combined_Key'] == country)][['Last_Update', 'Active']][::-1]
    csvs_selected = pd.concat(
        [
            csvs_country_inverted['Last_Update'],
            csvs_country_inverted['Active'].pct_change(),
        ],
        axis=1,
    )
    csvs_selected.dropna(inplace=True)
    csvs_selected['Last_Update'] = csvs_selected['Last_Update'].astype(str)
    csvs_list = csvs_selected.values.tolist()
    csvs_list.insert(0, list(csvs_selected.columns))
    return js_template.format(csvs_list, country)
