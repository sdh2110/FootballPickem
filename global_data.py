from web_browser import *
import time


CURRENT_YEAR = None
CURRENT_TEAMS = None
EARLY_GAMES = 5


def find_current_year():
    time_info = time.gmtime(time.time())
    if time_info.tm_mon > 6:
        return time_info.tm_year
    else:
        return time_info.tm_year - 1


def load_globals(year = None):
    global CURRENT_YEAR
    global CURRENT_TEAMS

    if year is None:
        CURRENT_YEAR = find_current_year()
    else:
        CURRENT_YEAR = year

    actual_current = load_all_teams(CURRENT_YEAR)
    for team_key in actual_current:
        actual_current[team_key] = actual_current[team_key].mk_average_team()

    previous_teams = load_all_teams(CURRENT_YEAR - 1)
    for team_key in previous_teams:
        previous_teams[team_key] = previous_teams[team_key].mk_average_team()

    for team_key in actual_current:
        if actual_current[team_key].extra_stats.games == 0:
            CURRENT_TEAMS[team_key] = previous_teams[team_key]
        elif actual_current[team_key].extra_stats.games >= EARLY_GAMES:
            CURRENT_TEAMS[team_key] = actual_current[team_key]
        else:
            current_prct = actual_current[team_key].extra_stats.games / EARLY_GAMES
            c_stats = actual_current[team_key].standard_stats.as_list()
            standard_count = len(c_stats)
            c_stats += actual_current[team_key].extra_stats.as_list()
            p_stats = previous_teams[team_key].standard_stats.as_list() + \
                      previous_teams[team_key].extra_stats.as_list()
            avg_stats = []
            for i in range(len(c_stats)):
                avg_stats.append((c_stats[i] * current_prct) + (p_stats[i] * (1 - current_prct)))
            CURRENT_TEAMS[team_key] = TeamProfile()
            CURRENT_TEAMS[team_key].standard_stats = StandardPack(avg_stats[:standard_count])
            CURRENT_TEAMS[team_key].extra_stats = BonusPack(avg_stats[standard_count:])