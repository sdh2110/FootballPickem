from game_stats import *
import global_data
import web_browser
import opponent_strengths
from helper_functions import get_file_location
from data_files_creator import update_runconfig


def main():
    global_data.load_globals()
    opponent_strengths.clear_backups(global_data.CURRENT_YEAR)

    teams_played = {}
    for team in global_data.CURRENT_TEAMS:
        teams_played[team] = False

    schedule = web_browser.load_schedule(global_data.CURRENT_YEAR, global_data.CURRENT_WEEK)
    for game in schedule:
        game_stats = web_browser.load_game_stats(game.game_url)
        game_stats.render_game()
        teams_played[game.vis_team] = True
        teams_played[game.home_team] = True

    for team in teams_played:
        if teams_played[team] is False:
            team_ops = OpponentStrengths(get_file_location(str(global_data.CURRENT_YEAR), team))
            team_ops.phaseout_data()
            team_ops.save_to_file()

    global_data.RUNCONFIGS["week num"] += 1
    update_runconfig()


if __name__ == '__main__':
    main()