from dataclasses import dataclass
from stats_packs import *
from helper_functions import make_floats
from helper_functions import get_file_location
from helper_functions import mk_list_to_percents
from opponent_strengths import OpponentStrengths
import global_data

global_data.load_globals()


@dataclass
class GameStats:
    __slots__ = "vis_team", "home_team", "vis_stats", "home_stats"
    vis_team: str
    home_team: str
    vis_stats: StandardPack
    home_stats: StandardPack

    def __init__(self, title_code, html_code):
        # Strip data from html code
        raw_data = [[], []]
        for line in html_code:
            info0 = line.split('vis_stat" >')[1]
            info0, info1 = info0.split('</td><td class="center " data-stat="home_stat" >')
            info1 = info1[:-10]
            raw_data[0].append(info0)
            raw_data[1].append(info1)

        # Organize the data to properly create a stats pack
        organized_data = [[], []]
        for i in range(2):
            organized_data[i].append(int(raw_data[i][7])) # turnovers
            organized_data[i].append(int(raw_data[i][6].split("-")[1])) # fumbles lost
            organized_data[i] += (make_floats(raw_data[i][2].split("-"))) # cmp, att, yds, tds, ints
            sack_data = make_floats(raw_data[i][3].split("-"))
            pass_NYA = (organized_data[i][4] - sack_data[1]) / (organized_data[i][3] + sack_data[0])
            organized_data[i].append(pass_NYA) # Net Yards gained per pass Attempt
            organized_data[i] += (make_floats(raw_data[i][1].split("-"))) # rushs, yds, tds
            organized_data[i].append(organized_data[i][9] / organized_data[i][8]) # rushing yards per attempt
            organized_data[i] += (make_floats(raw_data[i][8].split("-"))) # penalties, penalty yards

        # Get names and scores from title_code
        title_code = title_code[38:]
        title_info = title_code.split(" at ")
        title_info[1] = title_info[1].split(" on")[0]

        for i in range(2):
            score = title_info[i].split()[-1]
            title_info[i] = title_info[i][:-(len(score) + 1)]
            organized_data[i].append(int(score))

        self.vis_team = title_info[0]
        self.home_team = title_info[1]

        self.vis_stats = StandardPack(organized_data[0])
        self.home_stats = StandardPack(organized_data[1])


    def render_game(self):
        names = [self.vis_team, self.home_team]
        op_strs = [None, None]
        op_strs[0] = OpponentStrengths(get_file_location(str(global_data.CURRENT_YEAR), self.vis_team))
        op_strs[1] = OpponentStrengths(get_file_location(str(global_data.CURRENT_YEAR), self.home_team))

        avg_stats = [None, None]
        avg_stats[0] = global_data.CURRENT_TEAMS[self.vis_team].standard_stats.as_list()
        avg_stats[1] = global_data.CURRENT_TEAMS[self.home_team].standard_stats.as_list()

        game_stats = [None, None]
        game_stats[0] = self.vis_stats.as_list()
        game_stats[1] = self.home_stats.as_list()

        percents = [[], []]

        for i in range(2):
            for j in range(len(game_stats[i])):
                percents[i].append(game_stats[i][j] / avg_stats[i][j])