from game_stats import GameStats
from game_stats import ScheduledGame
from team_profiles import *
import urllib.request
import time
from progress_bars import ProgressBar
import random


def load_all_teams(year):
    pbar = ProgressBar("Loading teams", 100)
    # Load in the html code from the stats web page
    stats_page = urllib.request.urlopen("https://www.pro-football-reference.com/years/" + str(year))
    pbar.complete_task(55 + random.randint(0, 25))
    html_code = stats_page.read()
    html_lines = str(html_code).split('\\n')
    pbar.complete_task(13)

    # Find starting line in html for team stats
    start_idx = 865
    while html_lines[start_idx][:54] != '<tr ><th scope="row" class="right " data-stat="ranker"':
        start_idx += 1

    # Read in each team and add them to the dictionary of teams
    teams = {}
    idx = start_idx
    while len(html_lines[idx]) > 54 and \
            html_lines[idx][:54] == '<tr ><th scope="row" class="right " data-stat="ranker"':
        new_team = TeamProfile(html_lines[idx])
        teams[new_team.name] = new_team
        idx += 1
        pbar.complete_task()

    return teams


def load_game_stats(game_url):
    # Load in the html code from the stats web page
    game_page = urllib.request.urlopen(game_url)
    html_code = game_page.read()
    html_lines = str(html_code).split('\\n')

    # Find starting line in html for team stats
    start_idx = 700
    while len(html_lines[start_idx]) < 54 or \
            html_lines[start_idx][:54] != '<tr ><th scope="row" class="right " data-stat="stat" >':
        start_idx += 1

    return GameStats(html_lines[54], html_lines[start_idx : start_idx + 9])


def load_schedule(year, week):
    pbar = ProgressBar("Loading schedule", 100)
    schd_url = "https://www.pro-football-reference.com/years/" + str(year) + "/week_" + str(week) + ".htm"
    pbar.complete_task(40 + random.randint(0, 20))
    schd_page = urllib.request.urlopen(schd_url)
    html_code = schd_page.read()
    html_lines = str(html_code).split('\\n')

    schedule = []

    # Find section start in html for scheduled games
    search_idx = 550
    while html_lines[search_idx][:45] != '            <div class="section_heading"><h2>':
        search_idx += 1

    # Search for a game in schedule
    blank_count = 0
    while blank_count < 5:
        if len(html_lines[search_idx]) >= 30 and html_lines[search_idx][:30] == '      <div class="game_summary':
            schedule.append(ScheduledGame(html_lines[search_idx:search_idx + 21]))
            search_idx += 20
            blank_count = 0
        elif html_lines[search_idx].strip() == "":
            blank_count += 1
        else:
            blank_count = 0
        search_idx += 1
    pbar.complete_task(60)

    return schedule


def flt_to_percent(float_val):
    float_val *= 10000
    float_val = int(float_val)
    return str(float_val / 100) + "%"


def test_teams():
    teams = load_all_teams(2018)

    search = input("Enter a team's name: ")
    while search != "":
        if search in teams:
            print(teams[search])
        else:
            print("This team does not exist.")
        search = input("Enter a team's name: ")


def test_team_compare():
    teams = load_all_teams(2018)

    name1 = input("Enter the first team's name: ")
    name2 = input("Enter the second team's name: ")
    while name1 != "" and name2 != "":
        if name1 in teams and name2 in teams:
            print("These teams' profiles match", flt_to_percent(compare_teams(teams[name1], teams[name2])))
        else:
            print("This team does not exist.")
        name1 = input("Enter the first team's name: ")
        name2 = input("Enter the second team's name: ")


def test_load_game():
    url_address = input("Enter the url of the game: ").strip()
    while url_address != "":
        print(load_game_stats(url_address))
        url_address = input("Enter the url of the game: ")


def test_load_teams_speed():
    total_time = 0
    years = 0
    for year in range(2018, 1997, -1):
        print(year)
        start = time.time()
        load_all_teams(year)
        end = time.time()
        print("Read the teams in in", end - start, "seconds")
        total_time += end - start
        years += 1
    print("Read years in at", total_time / years, "seconds per year")


def test_load_schedule(year, week):
    schedule = load_schedule(year, week)
    for game in schedule:
        print(game)