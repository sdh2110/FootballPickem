from team_profiles import *
from game_stats import *
import urllib.request
import time


def load_all_teams(year):
    # Load in the html code from the stats web page
    stats_page = urllib.request.urlopen("https://www.pro-football-reference.com/years/" + str(year))
    html_code = stats_page.read()
    html_lines = str(html_code).split('\\n')

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

    return teams


def load_game_stats(game_url):
    # Load in the html code from the stats web page
    game_page = urllib.request.urlopen(game_url)
    html_code = game_page.read()
    html_lines = str(html_code).split('\\n')

    # Find starting line in html for team stats
    start_idx = 1080
    while html_lines[start_idx][:54] != '<tr ><th scope="row" class="right " data-stat="stat" >':
        start_idx += 1

    return GameStats(html_lines[54], html_lines[start_idx : start_idx + 9])


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