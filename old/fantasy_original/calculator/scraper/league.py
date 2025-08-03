from calculator.settings.team_object import Team

def get_all_team_names(d):
    mlb = {}
    for t in d:
        team = Team()
        team.abbr = t
        team.id = d[t]
        mlb[team.abbr] = team
    return mlb
