# Calculator

## install
From fantasy folder.
```
virtualenv -p python2.7 env
. env/bin/activate
```

## Single Pitcher Outing

```
python full_season_forecaster/pitcher_outing.py
```

## Inning Extrapolator

Get a projection for next season based on last seasons totals and your projection for this season.

```
python full_season_forecaster/run_pitcher_forecaster.py
```

## Streaming Pitcher Matchup Scout

Get average points against for a team. Used to determine good matchups for streaming.

```
python calculator/streaming_pitcher_matchup_scout/run.py
```


## Testing

```
pip3 install -U -r qa/requirements.txt
```

```
behave qa/features -i single_outing
```
