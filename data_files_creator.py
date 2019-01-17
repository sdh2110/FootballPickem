import os
from web_browser import *
from helper_functions import get_file_location
import global_data
from stats_packs import STANDARD_COUNT


def create_opponents_profile(file_location, opponents_names):
    stats_count = STANDARD_COUNT
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


def create_runconfig():
    if os.path.isfile("runconfig.txt"):
        print("runconfig.txt already exists")
    else:
        file = open("runconfig.txt", "w")
        file.write("other season=0\n")
        file.write("week num=1\n")
        file.close()


def update_runconfig():
    file = open("runconfig.txt", "w")
    for config in global_data.RUNCONFIGS:
        file.write(config + "=" + str(global_data.RUNCONFIGS[config]) + "\n")
    file.close()