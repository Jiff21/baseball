# Calculator


## Dependencies

Last tested at Python Version 3.10.4.

## Install

```bash
python -m venv env
source env/bin/activate
pip install -r calculator/requirements.txt
```

## Run

```bash
python main.py
```

TODO: Need to store data after getting it


## Update team data
NOT WORKING SEE https://stackoverflow.com/questions/14132789/relative-imports-for-the-billionth-time, runs on main
```bash
python calculator/mlbdotcom_teamscraper.py
```
TODO: Need to store data after getting it


## Single Pitcher Outing
NOT WORKING SEE https://stackoverflow.com/questions/14132789/relative-imports-for-the-billionth-time, runs on main
```bash
python full_season_forecaster/pitcher_outing.py
```

## Inning Extrapolator
NOT WORKING SEE https://stackoverflow.com/questions/14132789/relative-imports-for-the-billionth-time, runs on main
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
