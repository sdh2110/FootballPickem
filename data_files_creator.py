import os
from web_browser import *
from helper_functions import get_file_location


def create_opponents_profile(file_location, opponents_names):
    stats_count = len(StandardPack.__slots__)
    blank_stats = "|0|0" + " 0" * (stats_count - 1)
    if os.path.isfile(file_location):
        print("A profile already exists at", file_location)
    else:
        file = open(file_location, "w")
        for op_name in opponents_names:
            file.write(op_name + blank_stats + "\n")
        file.close()


def create_all_profiles(year):
    teams = list(load_all_teams(year).keys())
    folder_name = str(year)

    if not os.path.exists(folder_name):
        os.mkdir(folder_name)

    for i in range(len(teams)):
        opponents = teams[:]
        del opponents[i]
        create_opponents_profile(get_file_location(folder_name, teams[i]), opponents)