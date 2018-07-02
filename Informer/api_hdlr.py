import re
import urllib2
from time import sleep

from nvm import Match, Club, Player, NVM
from BeautifulSoup import BeautifulSoup


# .....
class CommonAPI:
    url = 'https://www.statbunker.com/'
    ip = '84.47.179.79'

    def __init__(self):
        pass


class PlayerAPI(Player, CommonAPI):
    def __init__(self, ID):
        Player.__init__(self, ID)


class MatchAPI(Match, CommonAPI):
    # def __init__(self, ID, name, league_name, comp_id, date):
    def __init__(self, ID, match_url):
        Match.__init__(self, ID)
        self.match_url = match_url
        # self.league_name = league_name
        # self.comp_id = comp_id
        # self.date = date
        # self.name = name

    # def get_url(self):
    #     return self.url + ("competitions/MatchDetails/%s" % self.league_name)


class ClubAPI(Club, CommonAPI):
    def __init__(self, ID):
        Club.__init__(self, ID)


class HTML_Season:
    def __init__(self, comp_id, name):
        self.name = name
        self.comp_id = comp_id


class HTML_League:
    def __init__(self, url, name):
        self.url = url
        self.name = name
        self.seasons = []


api_leagues = []


def req_url(url):
    print 'requesting', url
    headers = {}
    # headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib2.Request(url, None, headers)
    resp = urllib2.urlopen(req)
    sleep(2)
    return resp.read()


def analyze_match_page(url):
    print 'analyzing %s' % url

    page = req_url(url)
    parsed_page = BeautifulSoup(page)

    # score
    score_tag = parsed_page.findAll('div', {'class': 'matchReportTitle'})
    # for i in score_tag:
    #     print i #score_tag
    print score_tag
    home_team = None
    away_team = None
    score = None


# ********* algorithms to update local data ********* #
def deep_check():  # walk through main leagues found on main url
    # Search all leagues
    page = req_url(CommonAPI.url)
    parsed_page = BeautifulSoup(page)

    html_leagues = parsed_page.findAll('div', {'class': 'intRight'})
    for div in html_leagues:
        tags = div.findAll('a')
        for tag in tags:
            league_href = tag['href']
            league_name = tag.find('span').text
            api_leagues.append(HTML_League(league_href, league_name))

    # search all seasons in leagues
    for league_obj in api_leagues:
        page = req_url(league_obj.url)
        parsed_page = BeautifulSoup(page)
        # print league_obj.name

        # search all seasons for league
        seasons_url = parsed_page.findAll('select', {'name': 'comp_id'})
        for season in seasons_url:
            for option in season.findAll('option'):
                comp_id = option['value']
                # if not 'Select' in option.text:
                if int(comp_id) >= 0:
                    league_obj.seasons.append(HTML_Season(comp_id, option.text))
            # print season.findAll('option')
        # TODO
        break

    # search all matches in league season
    tmp = 0
    for league_obj in api_leagues:
        for season_obj in league_obj.seasons:
            if not tmp:
                tmp = 1
                continue
            # TODO
            url = CommonAPI.url + ('competitions/LastMatches?comp_id=%s&limit=10' % season_obj.comp_id)

            # Here we should grab all matches from season
            page = req_url(url)
            parsed_page = BeautifulSoup(page)

            html_matches = parsed_page.findAll('span', {'class': 'matchVs'})
            for html_match in html_matches:
                match_url = html_match.find('a')['href']
                analyze_match_page(match_url)

            # for season in league_obj.seasons:
            # matches_url = parsed_page.findAll('a', {'title': season + ' Latest results'})
            # print matches_url, season

            break
        # print matches_url


if __name__ == '__main__':
    deep_check()
    # for league in api_leagues:
    #     print league
