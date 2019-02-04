import global_data
import web_browser
import comparison
from opponent_strengths import *
import opponent_strengths
from helper_functions import get_file_location
from team_profiles import TeamProfile


CMP_CHART = None
TEAM_KEYS = {}


def predict_team_ability(team_name, opponent_name):
    similar_ops = CMP_CHART[TEAM_KEYS[opponent_name]]
    similar_teams = CMP_CHART[TEAM_KEYS[team_name]]
    team_vs_sim_ops = Consensus()
    sim_teams_vs_op = Consensus()

    team_op_strs = OpponentStrengths(get_file_location(str(global_data.CURRENT_YEAR), team_name), False)
    for sim_op in team_op_strs.opponents.keys():
        team_vs_sim_ops.add_profile(team_op_strs.opponents[sim_op], similar_ops[TEAM_KEYS[sim_op]])

    for sim_team in TEAM_KEYS.keys():
        if sim_team != opponent_name:
            sim_team_op_strs = OpponentStrengths(get_file_location(str(global_data.CURRENT_YEAR), sim_team), False)
            sim_teams_vs_op.add_profile(sim_team_op_strs.opponents[opponent_name], similar_teams[TEAM_KEYS[sim_team]])

    final_consensus = Consensus()
    final_consensus.add_profile(team_vs_sim_ops.get_consensus())
    final_consensus.add_profile(sim_teams_vs_op.get_consensus())
    final_consensus.add_profile(team_op_strs.opponents[opponent_name])
    return final_consensus.get_consensus()


def predict_team_score(team_name, predicted_ability):
    if predicted_ability is None:
        print(end = "*")
        return global_data.CURRENT_TEAMS[team_name].standard_stats.points_for()
    return global_data.CURRENT_TEAMS[team_name].standard_stats.points_for() * \
           predicted_ability.stat_percents.points_for()


def main():
    global CMP_CHART
    global TEAM_KEYS

    global_data.load_globals()
    schedule = web_browser.load_schedule(global_data.CURRENT_YEAR, global_data.CURRENT_WEEK)
    CMP_CHART, TEAM_KEYS = comparison.mk_comparison_chart(comparison.compare_teams, \
                                                          global_data.CURRENT_TEAMS)

    for game in schedule:
        home_ability = predict_team_ability(game.home_team, game.vis_team)
        vis_ability = predict_team_ability(game.vis_team, game.home_team)
        home_score = int(predict_team_score(game.home_team, home_ability))
        vis_score = int(predict_team_score(game.vis_team, vis_ability))
        print(game.vis_team, vis_score, "@", game.home_team, home_score)


if __name__ == '__main__':
    main()