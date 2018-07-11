from BeautifulSoup import BeautifulSoup

from Informer.api_data import req_url, CommonAPI
from Informer.api_parse import get_leagues, get_seasons_for_leagues, get_matches_from_season, \
    get_competitions, get_clubs_from_season_url
# ********* algorithms to update local data ********* #
from Informer.nvm import Team, Competition


class Informer:
    @staticmethod
    def init():
        Team.load_club_list()
        Competition.import_competitions()

    @staticmethod
    def update_competitions():  # rare < 10 min
        competitions = get_competitions()
        d_comps = dict((comp.comp_id, comp.name) for comp in competitions)
        Competition.export_competitions(d_comps=d_comps)

    @staticmethod
    def update_teams():  # rare < 20 min
        # Search all leagues
        main_page = req_url(CommonAPI.url)
        parsed_main_page = BeautifulSoup(main_page)

        if Competition.comp_dict.keys():
            print 'Competitions are loaded before'
            competitions_list = Competition.comp_dict.keys()
        else:
            api_leagues = get_leagues(parsed_main_page)
            print 'leagues list downloaded'

            get_seasons_for_leagues(api_leagues)
            print 'seasons are got'

            competitions_list = [season.comp_id for league_obj in api_leagues for season in league_obj.seasons]

        # search all teams in leagues
        teams = []

        for competition in competitions_list:
            clubs_for_season = get_clubs_from_season_url(competition)
            teams.extend(clubs_for_season)

        Team.set_last_update()

        return teams

    @staticmethod
    def update_matches_for_team(team_id, comp_id):
        pass

    class Rare:
        @staticmethod
        def get_matches_by_leagues():  # walk through main leagues found on main url
            # Search all leagues
            main_page = req_url(CommonAPI.url)
            parsed_main_page = BeautifulSoup(main_page)

            api_leagues = get_leagues(parsed_main_page)

            # search all seasons in leagues
            get_seasons_for_leagues(api_leagues)

            # search all matches in league season
            for league_obj in api_leagues:
                for season_obj in league_obj.seasons:
                    get_matches_from_season(league_obj, season_obj)
                # print matches_url

        @staticmethod
        def get_clubs():
            # Search all leagues
            main_page = req_url(CommonAPI.url)
            parsed_main_page = BeautifulSoup(main_page)

            api_leagues = get_leagues(parsed_main_page)

            # search all clubs in leagues
            clubs = []

            for league_obj in api_leagues:
                clubs_for_league = get_clubs_from_league(league_obj)
                clubs.extend(clubs_for_league)

            return clubs

    class Frequent:
        pass


if __name__ == '__main__':
    Informer.init()
    # analyze_match_page(
    #     'https://www.statbunker.com/competitions/MatchDetails/Premier-League-17/18/West-Ham-United-VS-Everton?comp_id=586&match_id=95485&date=13-May-2018')
    # deep_check()
    # all_clubs = get_all_clubs()
    # get_matches_from_club(586, 5)

    # Informer.update_competitions()
    Informer.update_teams()
