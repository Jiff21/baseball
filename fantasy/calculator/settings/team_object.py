class Team(object):
    def __init__(self):
        """Return a team and there win loss splits."""
        self.standings = None

        def set_wins(wins):
            self.wins = wins

        def set_losses(losses):
            self.losses = losses

        def set_games(games_played):
            self.games_played = games_played

        def set_win_avg(win_avg):
            self.win_avg = get_avg(self.wins, self.losses)

        def set_loss_avg(loss_avg):
            self.loss_avg = loss_avg

        def get_avg(avg_to_get, other_half):
            avg = avg_to_get / avg_to_get + other_half
            return get_avg
