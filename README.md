# Covinfo

Playground for ```gcloud``` functions. The data are fetched from
```CSSEGISandData/COVID-19``` repository and filtered for given date, country,
output columns. If no arguments are given, the data are filtered for a previous
day, Poland, and following output columns:

    - 'Confirmed'
    - 'Deaths'
    - 'Recovered'
    - 'Active'

The function responds to a simple HTTP request. The arguments are ```country``` and ```recoveryrate```.

Examples:

    - default values, data for Poland:

	```console
	curl "https://europe-west3-decisive-mapper-272319.cloudfunctions.net/covinfo"

	curl "https://europe-west3-decisive-mapper-272319.cloudfunctions.net/changerate"
	```
    - recovery rate, data for france:

	```console
	curl "https://europe-west3-decisive-mapper-272319.cloudfunctions.net/covinfo?recoveryrate=&country=france"
	```
