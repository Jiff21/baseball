import json
import requests
import sys
from calculator.settings.logger import log
from calculator.settings.api import UPDATED_BASE_URL, TEAM_HITTING_JSON_BLOCK

class SplitsScraper(object):

    def __init__(self):
        log.debug('Instantiate SplitsScraper')


    def get_avg(self, number, total):
        return number / total

    def get_splits_by_uri(self, uri):
        log.debug("TODO WRITE TESTS, get splits from api")
        current_url = UPDATED_BASE_URL + uri
        log.debug("get_splits_by_uri" + current_url)
        try:
            response = requests.get(current_url)
        except requests.exceptions.RequestException as e:
            print(e)
            sys.exit(1)
        log.debug('get_splits_by_uri response:\n%s\n' % response.status_code)
        assert response.status_code == requests.codes.ok, 'Get Splits by uri ' \
            'got code %s\nFrom url %s' % (
                response.status_code,
                current_url
            )
        response_text = response.text
        response_json = json.loads(response_text)
        # import pdb; pdb.set_trace()
        print('You just changed this to return response json to return directly as a guess thats where line below left off')
        # current_dict = response_json[TEAM_HITTING_JSON_BLOCK]['queryResults']['row']
        # return current_dict
        return response_json['stats']

    def get_runs(self, dic):
        return int(dic['runs'])

    def get_rbi(self, dic):
        return int(dic['rbi'])

    def get_games(self, dic):
        return int(dic['gamesPlayed'])

    def get_hits(self, dic):
        return int(dic['hits'])

    def get_home_runs(self, dic):
        return int(dic['homeRuns'])

    def get_walks(self, dic):
        print('add ints and bean balls')
        return int(dic['baseOnBalls'])

    def get_strikeouts(self, dic):
        return int(dic['strikeOuts'])

    def get_plate_appearances(self, dic):
        return int(dic['plateAppearances'])

    def get_runs_per_game(self, runs, games):
        return self.get_avg(runs, games)


    def get_relevant_splits_per_dict(self, splits_dict):
        log.debug('running get_relevant_splits_per_dict')
        r = self.get_runs(splits_dict)
        g = self.get_games(splits_dict)
        runs_per_game = self.get_runs_per_game(r, g)

        h = self.get_hits(splits_dict)
        hits_per_game = self.get_avg(h, g)

        hr = self.get_home_runs(splits_dict)
        hr_per_game = self.get_avg(hr, g)

        bb = self.get_walks(splits_dict)
        waks_per_game = self.get_avg(bb, g)

        so = self.get_strikeouts(splits_dict)
        so_per_game = self.get_avg(so, g)

        return runs_per_game, hits_per_game, hr_per_game, waks_per_game, so_per_game


    def get_pitcher_splits_per_dict(self, splits_dict):
        log.debug('running get_pitcher_splits_per_dict')
        r = self.get_runs(splits_dict)

        plate_appearances = self.get_plate_appearances(splits_dict)
        runs_per_pa = self.get_avg(r, plate_appearances)

        h = self.get_hits(splits_dict)
        hits_per_pa = self.get_avg(h, plate_appearances)

        hr = self.get_home_runs(splits_dict)
        hr_per_pa = self.get_avg(hr, plate_appearances)

        bb = self.get_walks(splits_dict)
        walks_per_pa = self.get_avg(bb, plate_appearances)

        so = self.get_strikeouts(splits_dict)
        so_per_pa = self.get_avg(so, plate_appearances)

        return runs_per_pa, hits_per_pa, hr_per_pa, walks_per_pa, so_per_pa

    def get_pitcher_rl_splits_per_dict(self, splits_dict):
        log.debug(
            'running get_pitcher_rl_splits_per_dict,\ getting rbi since no runs'
        )
        r = self.get_rbi(splits_dict)

        plate_appearances = self.get_plate_appearances(splits_dict)
        runs_per_pa = self.get_avg(r, plate_appearances)

        h = self.get_hits(splits_dict)
        hits_per_pa = self.get_avg(h, plate_appearances)

        hr = self.get_home_runs(splits_dict)
        hr_per_pa = self.get_avg(hr, plate_appearances)

        bb = self.get_walks(splits_dict)
        walks_per_pa = self.get_avg(bb, plate_appearances)

        so = self.get_strikeouts(splits_dict)
        so_per_pa = self.get_avg(so, plate_appearances)

        return runs_per_pa, hits_per_pa, hr_per_pa, walks_per_pa, so_per_pa
