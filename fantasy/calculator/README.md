# Calculator

## install
From fantasy folder.

```bash
virtualenv -p python3.6 env
. env/bin/activate
```

## Update team data

```bash
python calculator/mlbdotcom_teamscraper.py
```

TODO: Need to store data after getting it


## Single Pitcher Outing

```bash
python full_season_forecaster/pitcher_outing.py
```

## Inning Extrapolator

Get a projection for next season based on last seasons totals and your projection for this season.

```bash
python full_season_forecaster/run_pitcher_forecaster.py
```

## Streaming Pitcher Matchup Scout

Get average points against for a team. Used to determine good matchups for streaming.

```bash
python calculator/streaming_pitcher_matchup_scout/run.py
```


## Testing

```bash
pip3 install -U -r qa/requirements.txt
```

```bash
python calculator/tests/StandingsData_test.py
```

```bash
behave qa/features -i single_outing
```
