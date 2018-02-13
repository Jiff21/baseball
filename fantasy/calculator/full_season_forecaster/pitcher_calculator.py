from calculator.settings.scoring_settings import ScoringSettings
ssp = ScoringSettings.Pitching

def calculate_game(innings, earned_runs, total_walks, hits_allowed, \
	homeruns_allowed, strikeouts, saves, wins, losses, quality_starts):
	total = (float(innings) * ssp.INN) \
		+ (float(earned_runs) * ssp.ER) \
	 	+ (float(total_walks) * ssp.BBI) \
		+ (float(hits_allowed) * ssp.HA) \
		+ (float(homeruns_allowed) * ssp.HRA) \
		+ (float(strikeouts) * ssp.K) \
		+ (float(saves) * ssp.S) \
		+ (float(wins) * ssp.W) \
		+ (float(losses) * ssp.L) \
		+ (float(quality_starts) * ssp.QS)
	return round(float(total),1)
