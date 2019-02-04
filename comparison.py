from helper_functions import percent_difference
from team_profiles import TeamProfile


def compare_teams_method1(team1, team2):
    team1_stats = team1.standard_stats.as_list() + team1.extra_stats.as_list()
    team2_stats = team2.standard_stats.as_list() + team2.extra_stats.as_list()
    team1_stats = team1_stats[1:]
    team2_stats = team2_stats[1:]

    return percent_difference(team1_stats, team2_stats)


def compare_teams(team1, team2):
    return compare_teams_method1(team1, team2)


def mk_comparison_chart(cmp_function, data):
    data_keys = None
    if isinstance(data, dict):
        data_keys = {}
        indexed_data = []
        i = 0
        for key in data.keys():
            indexed_data.append(data[key])
            data_keys[key] = i
            i += 1
    else:
        indexed_data = data
    cmp_chart = []
    for entry in indexed_data:
        cmps_for_entry = []
        for cmp_entry in indexed_data:
            cmps_for_entry.append(cmp_function(entry, cmp_entry))
        cmp_chart.append(cmps_for_entry)
    if data_keys is None:
        return cmp_chart
    return cmp_chart, data_keys