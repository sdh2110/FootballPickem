import time
from helper_functions import combine_by_percent


RUNCONFIGS = {}

CURRENT_YEAR = None
CURRENT_WEEK = None
CURRENT_TEAMS = {}

EARLY_GAMES = 5
OP_STRS_SAVE_RATE = 0.7
OP_STRS_PHASEOUT_RATE = 0.9


def find_current_year():
    time_info = time.gmtime(time.time())
    if time_info.tm_mon > 6:
        return time_info.tm_year
    else:
        return time_info.tm_year - 1


def load_global_nums():
    global RUNCONFIGS
    global CURRENT_YEAR
    global CURRENT_WEEK

    for line in open("runconfig.txt"):
        line = line.strip().split("=")
        RUNCONFIGS[line[0]] = int(line[1])

    if RUNCONFIGS["other season"] == 0:
        CURRENT_YEAR = find_current_year()
    else:
        CURRENT_YEAR = RUNCONFIGS["other season"]

    CURRENT_WEEK = RUNCONFIGS["week num"]


def load_global_teams():
    import web_browser
    global CURRENT_TEAMS

    actual_current = web_browser.load_all_teams(CURRENT_YEAR)
    for team_key in actual_current:
        actual_current[team_key] = actual_current[team_key].mk_average_team()

    previous_teams = web_browser.load_all_teams(CURRENT_YEAR - 1)
    for team_key in previous_teams:
        previous_teams[team_key] = previous_teams[team_key].mk_average_team()

    for team_key in actual_current:
        if actual_current[team_key].extra_stats.games() == 0:
            CURRENT_TEAMS[team_key] = previous_teams[team_key]
        elif actual_current[team_key].extra_stats.games() >= EARLY_GAMES:
            CURRENT_TEAMS[team_key] = actual_current[team_key]
        else:
            current_prct = actual_current[team_key].extra_stats.games() / EARLY_GAMES
            c_stats = actual_current[team_key].standard_stats.as_list()
            standard_count = len(c_stats)
            c_stats += actual_current[team_key].extra_stats.as_list()
            p_stats = previous_teams[team_key].standard_stats.as_list() + \
                      previous_teams[team_key].extra_stats.as_list()
            avg_stats = []
            for i in range(len(c_stats)):
                avg_stats.append(combine_by_percent(c_stats[i], p_stats[i], current_prct))
            CURRENT_TEAMS[team_key] = web_browser.TeamProfile()
            CURRENT_TEAMS[team_key].standard_stats = web_browser.StandardPack(avg_stats[:standard_count])
            CURRENT_TEAMS[team_key].extra_stats = web_browser.ExtraOffensePack(avg_stats[standard_count:])


def load_globals():
    load_global_nums()
    load_global_teams()