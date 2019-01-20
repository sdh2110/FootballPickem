from dataclasses import dataclass
from stats_packs import *
from helper_functions import make_floats
from helper_functions import get_file_location
from helper_functions import mk_list_to_percents
from opponent_strengths import *
import global_data


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
            info0, info1 = info0.split('</td><td')
            info1 = info1.split('home_stat" >')[1][:-10]
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
        game_stats = [None, None]
        game_stats[0] = self.vis_stats.as_list()
        game_stats[1] = self.home_stats.as_list()

        for i in range(2):
            op_strs = OpponentStrengths(get_file_location(str(global_data.CURRENT_YEAR), names[i]))
            avg_stats = global_data.CURRENT_TEAMS[names[i]].standard_stats.as_list()
            percents = []

            for j in range(len(game_stats[i])):
                percents.append(game_stats[i][j] / avg_stats[j])

            op_strs.phaseout_data()
            op_strs.update_op(names[i - 1], percents)
            op_strs.opponents[names[i - 1]].decay = 1
            op_strs.save_to_file()


@dataclass
class ScheduledGame:
    __slots__ = "vis_team", "home_team", "game_url", "has_been_played"
    vis_team: str
    home_team: str
    game_url: str
    has_been_played: bool

    def __init__(self, html_code):
        self.vis_team = html_code[6].split('htm">')[1].split('<')[0]
        self.home_team = html_code[14].split('htm">')[1].split('<')[0]
        self.game_url = "https://www.pro-football-reference.com/boxscores/" + \
                        html_code[9].split("/boxscores/")[1][:16]
        self.has_been_played = html_code[0].strip() == '<div class="game_summary expanded nohover">'