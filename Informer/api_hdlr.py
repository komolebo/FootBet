from BeautifulSoup import BeautifulSoup

from Informer.api_data import req_url, CommonAPI
from Informer.api_parse import get_leagues, get_seasons_for_leagues, get_matches_from_season, get_clubs_from_league, \
    get_matches_from_club
# ********* algorithms to update local data ********* #
from Informer.nvm import Club



class Informer:
    @staticmethod
    def init():
        Club.load_club_list()

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
    get_matches_from_club(586, 5)