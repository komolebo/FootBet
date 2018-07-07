from BeautifulSoup import BeautifulSoup

from Informer.api_data import req_url, CommonAPI
from Informer.api_parse import get_leagues, get_seasons_for_leagues, get_matches_from_season


# ********* algorithms to update local data ********* #
def deep_check():  # walk through main leagues found on main url
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


if __name__ == '__main__':
    # analyze_match_page(
    #     'https://www.statbunker.com/competitions/MatchDetails/Premier-League-17/18/West-Ham-United-VS-Everton?comp_id=586&match_id=95485&date=13-May-2018')
    deep_check()
    # for league in api_leagues:
    #     print league
