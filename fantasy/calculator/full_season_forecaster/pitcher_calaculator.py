from scoring_settings import ScoringSettings
ssp = ScoringSettings.Pitching

def calculate_game(innings, earned_runs, total_walks, hits_allowed, \
	homeruns_allowed, strikeouts, saves, wins, losses, quality_starts):
	total = (innings * ssp.INN) + (earned_runs \
		* ssp.ER) + (total_walks * ssp.BBI) \
		+ (hits_allowed * ssp.HA) \
		+ (homeruns_allowed * ssp.HRA) \
		+ (strikeouts * ssp.K) \
		+ (saves * ssp.S) \
		+ (wins * ssp.W) \
		+ (losses * ssp.L) \
		+ (quality_starts * ssp.QS)
	return total
