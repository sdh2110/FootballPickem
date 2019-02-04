from helper_functions import percent_diff
from team_profiles import TeamProfile


def compare_teams_method1(team1, team2):
    team1_stats = team1.standard_stats.as_list() + team1.extra_stats.as_list()
    team2_stats = team2.standard_stats.as_list() + team2.extra_stats.as_list()
    team1_stats = team1_stats[1:]
    team2_stats = team2_stats[1:]

    return percent_diff(team1_stats, team2_stats)


def compare_teams(team1, team2):
    return compare_teams_method1(team1.mk_average_team(), team2.mk_average_team())


def mk_comparison_chart(cmp_function, data):
    cmp_chart = []
    for entry in data:
        cmps_for_entry = []
        for cmp_entry in data:
            cmps_for_entry.append(int(cmp_function(entry, cmp_entry) * 100))
        cmp_chart.append(cmps_for_entry)
    if isinstance(data[0], TeamProfile):
        data_keys = {}
        for i in range(len(data)):
            data_keys[data[i].name] = i
            return cmp_chart, data_keys
    return cmp_chart