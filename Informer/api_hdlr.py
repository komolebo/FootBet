import base64
import re
import urllib
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


def authentication(url):
    opener = urllib2.build_opener()
    opener.addheaders.append(('Cookie', 'footballci_session=OtrsSY75usBzHReQCFyyEkSXLDUfmwt27rmWaTniiyGhOSluFG3FM3Z4PinRm41A%2FKKDJTz%2Facbs1cGavDIa0CdUn37OsTugA2TdMd3Sr7ZYbd6ajkYxpxY2Xa07oa1TQDVsWdIKBa8ly5b0mny7dDm7H36QDIw%2FVrZbZProYe8uv2q5R3Gh5HxK8yyHL74F%2FOJ8auCZSQqtYFODBBvMjVO2kS5zHsm6f%2FZLaNQkTaKmgDiMRxqsCGu%2BPIicqbJuj1KuKVy95zjHYKYVF%2BRQYGvfR%2FxmPQG8uuSUJnrPaIMIoIA%2FcctYvSI294ORFZS7jiJI54Rr%2BIIU7fDGHIcqhZUSsqhc%2Bx8jV2B5PAv45TDHH00b1pHqkLSjHbS2zOrIDCeP%2FgtvnVCv6QtNGKXEw1D25tbwWGHHWJ1ZMK2iOGMxaO587I%2F%2Br7IG%2F1jVftItaRGa%2Bi%2Bruzov1P9nbYoIi%2BBudQT4Xhp4tfJxmCFGgc9eSdLS4e5YLJqrOqGPtxT84sYOpJweqeQ72koxVeuPVd544vztXqDExty0DrSVuT73evOIzB8BH9FzdgwXwl4qf6Vr%2BFwnw2OkVnNEGAl2DtmP3uBrka9Q4HXXV2e8dTOWbWT8XsLsAOCLhv247vNekZeHuTBpDdyX8bnEQABvFV1XHLjFUlfoMYNcCEy7irZsR6M695NJw85%2BkdisQjAxW8FSvTTmdSNOpYlYZVt98JpWP9apVumV8nLsagCOjfzZF1kNQFfvz7rL%2B2imsqUQtITy1dwHHKmCip7ozracIDWz0P5swLF7k%2BiVUgak34x%2BBwjpYqFU5uUgSjuXfM1lvLbBWcBcxf8KbjTBHsgXyTu0NZIvqyiUuoO03O5qwsg3AzHV%2Fr6plf27TQ1R8T8teQoTBAgfP2H%2FZun%2F6i3NQp8r1Zf5HBW1oZsj2SapZ5TJWezAD1OlenmX5EGPlTnEYUUW9zumKhe3x433OcCqNa2IJynh5MGqQZ6v6MDeowoa5CyxlvyV8bAkM%2BxnEIhDZkubVe8dF8ywL86zshyG8HhvN2hWB5y86JwNJvMDGL7ode2ax75gGU357OX0nADlAo2x4RZy1F877b5TTrlxwv1m%2B6THur1r0OH8txeW2XXZ8YlJnTdDOio66yEK3FVbFXmbH80HEq6xwrabyiXe7niXanp8OSXbcHaSl42Dng8%3D'))
    f = opener.open(url)
    print f

    sleep(2)

    username = "kokopyka@gmail.com"
    password = "1995522804da"
    base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')

    request = urllib2.Request(url)
    # request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36')
    # request.add_header('Content-Type', 'application/x-www-form-urlencoded')
    request.add_header('X-DevTools-Emulate-Network-Conditions-Client-Id', '5630F616A037C831B8D6F1B6182C6B32')
    #
    # request.add_header("footballci_session", "OB%2BISv7nkxx7mB873kSuthOLzT%2F0rmNwhlyX5l6YCh4jdnpFZtDilzYzZY"
    #                                          "%2BABYnSMv0MhJ5wlq3QBnM9fiTy1Tpb7%2BcpvT4Knz7%2BM%2BI54PZBiuq9N"
    #                                          "%2F2Upr4Rm3cfHi7BRrthoZrUjRIDv82vm9ftGEWpdftJPjFLcUH2VDdjEyPQbkJMHEI6"
    #                                          "%2BcPXh6A5C%2BEIQHjnpr6YzKwHqoPuZI%2Bq%2Br5PipWjwnwt%2FATg3RxQIsn2lE8kMIJIyOd5x4C4Y88F3b0Bznc1SYQFTVNoWS3%2FDJH9e00tjox9ALKjlJCqdQPK1DTden6eK2qQqQtmqA6iSP9onhNP%2BKi3pF2MGMy1am8uuSL3Wto9L3%2FYeaLpC6coHq%2BlzyvgEFCocduZmjK4e9%2B64VtXdbZGeUsbIBPbeJLVlwBSiMw7FK3A3H%2FJg5Vlb41OVtFRt%2FgXgq650I%2B%2BOVatXg1xAOYbtMYvP78xnjaYrpkYKUEoyCbTgLRCQeQspmEmdCd1WosmwyZtwxSWJbJHr%2B6D%2FXNvp0X4P%2FZYOxHKkj1UoIkkJ2hIr4S5FX25Iz6wwS%2FtU9uOqRGdUV9uOPoTAdP1Gz2bDCcRj8edbjW5aShdhTnm04i655hPwLphInU7PV1Z1A5uUNgSxCFepp0wtoDxLlaqTj0BiLjiBYBSHvr7S4%2F01pLyjrWBtcUiKvchaTIbvSqkwQdlsjlI%2FCY7jBLkooC0kij1k8HUxuK2fwoP9tmvvYASCZ0ukSLgK7j9fVDzsn7%2F0BVFVbTl2VIzHv3uYFeBSGJeH%2B3UdLhKCrkGx0epQIm2cETovHkPbJZUoGdZRidDJFaycXjiyEnsziq1hlM7aw3kbvYoTMOLyUl97pylU7uBgNJaZSSf7K%2FGrgciT3U2HE7JmuMguJDwTIMmJANzQ%2FnrtS3zNY3LAacFrSZ2ChaVJj4bFEwdtn%2BgoGlvUJYMOG7iAIKUt2oUMGr%2BzddYHSX5zlrK9N2O4KBUDOaR%2F0Nf21o1WicRvGbTthrHEPRkgDKufbu%2BxIGwPxhGX%2Bv9w9Fl87jzSjqKwzxEZo%2BFWiHHuv2Ng%2BfsRRaJQIyqZhi9g3in15k4U2wceUko1veEkKIWHp53gQIHXUNjZqBQFT7ja5TbFc%2FhS4pRuiNNBD8Hog%2Fa15l5po%2F3UHvwxfNn5Mp1X0GltgEDeKuUq40eDzsBLovTSqoc3VM%2FYPUDbJ0G%2Bo1Q39ynJuaa0Xu2H0U8Xgkj1hsYUQ%3D%3D")

    result = urllib2.urlopen(request)
    # result = urllib.urlopen(url)
    data = result.read()
    sleep(2)
    return data


def req_url(url):
    print 'requesting', url

    username = "kokopyka@gmail.com"
    password = "1995522804da"
    headers = {}

    base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')

    # headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib2.Request(url, None, headers)
    req.add_header("Authorization", "Basic %s" % base64string)
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
    print authentication('https://www.statbunker.com/competitions/LastMatches?comp_id=586&limit=10&offs=UP1')
    print authentication('https://www.statbunker.com/competitions/MatchDetails/Premier-League-17/18/Newcastle-United'
                         '-VS-Chelsea?comp_id=586&match_id=95481&date=13-May-2018')
    # deep_check()
    # for league in api_leagues:
    #     print league
