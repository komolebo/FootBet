import json
import urllib
import urllib2


class Connector:
    api_url = "https://api.sportdeer.com"
    REFRESH_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9' \
                    '.eyJ1c2VySWQiOiI1YjJkOGYxNWU5MWVkNzMzMTE4NWI5MzgiLCJpYXQiOjE1Mjk3MTI0NjV9' \
                    '.N3HY80Hya0EuwQVJfPzNZ3xKVUc7SyvWhYRgz2nOEtU '

    def __init__(self):
        pass

    def request(self, url):
        link = self.api_url + url + '?access_token=' + self.get_access_token()
        return urllib.urlopen(link).read()

    def get_access_token(self):
        link = self.api_url + '/v1/accessToken?refresh_token=' + self.REFRESH_TOKEN
        response = urllib.urlopen(link)
        data = json.load(response)
        return data['new_access_token']

    def check_connection(self):
        try:
            response = urllib2.urlopen(self.api_url)
            return 1
        except urllib2.URLError, urllib2.HTTPError:
            return 0


class AbstractFootballObj:
    connector = Connector()

    def __init__(self, id, name):
        self.id = id
        self.name = name


class Fixture(AbstractFootballObj):
    def __init__(self, id, name):
        AbstractFootballObj.__init__(self, id, name)
        self.url = '/v1/fixtures/' + str(id)

        self.fixture_status = None
        self.fixture_status_short = None
        self.lineup_confirmed = None

        self.number_goal_team_home = None
        self.number_goal_team_away = None

        self.team_season_home_name = None
        self.team_season_away_name = None

        self.id_team_season_away = None
        self.id_team_season_home = None

        self.first_half_ended_at = None
        self.game_started_at = None
        self.game_ended_at = None
        self.second_half_started_at = None
        self.schedule_date = None

        self.spectators = ''
        self.stadium = ''
        self.id_referee = None
        self.referee_name = None
        self.round = None

    def set_status(self, fixture_status, fixture_status_short, lineup_confirmed):
        self.fixture_status = fixture_status
        self.fixture_status_short = fixture_status_short
        self.lineup_confirmed = lineup_confirmed

    def set_goals(self, home, away):
        self.number_goal_team_home = home
        self.number_goal_team_away = away

    def set_team_names(self, home, away):
        self.team_season_home_name = home
        self.team_season_away_name = away

    def set_team_ids(self, home, away):
        self.id_team_season_home = home
        self.id_team_season_away = away

    def set_timestamps(self, start, end, half1_end, half2_start, schedule_date):
        self.first_half_ended_at = half1_end
        self.game_started_at = start
        self.game_ended_at = end
        self.second_half_started_at = half2_start
        self.schedule_date = schedule_date

    def set_general_info(self, spectators, stadium, id_ref, ref_name, round):
        self.spectators = spectators
        self.stadium = stadium
        self.id_referee = id_ref
        self.referee_name = ref_name
        self.round = round

    def request_fixture_data(self):
        resp = json.loads(self.connector.request(self.url))['docs'][0]
        self.load_from_json(resp)

    def load_from_json(self, js):
        self.fixture_status = js['fixture_status']
        self.fixture_status_short = js['fixture_status_short']
        self.lineup_confirmed = js['number_goal_team_home']
        self.number_goal_team_home = js['number_goal_team_home']
        self.number_goal_team_away = js['number_goal_team_away']
        self.team_season_home_name = js['team_season_home_name']
        self.team_season_away_name = js['team_season_away_name']
        self.id_team_season_home = js['id_team_season_home']
        self.id_team_season_away = js['id_team_season_away']
        if 'first_half_ended_at' in js.keys():
            self.first_half_ended_at = js['first_half_ended_at']
        if 'game_started_at' in js.keys():
            self.game_started_at = js['game_started_at']
        if 'game_ended_at' in js.keys():
            self.game_ended_at = js['game_ended_at']
        if 'second_half_started_at' in js.keys():
            self.second_half_started_at = js['second_half_started_at']
        if 'schedule_date' in js.keys():
            self.schedule_date = js['schedule_date']
        if 'spectators' in js.keys():
            self.spectators = js['spectators']
        if 'stadium' in js.keys():
            self.stadium = js['stadium']
            self.stadium = self.stadium.replace('sportsdirect.com @ ', '')
        if 'id_referee' in js.keys():
            self.id_referee = js['id_referee']
        if 'referee_name' in js.keys():
            self.referee_name = js['referee_name']
        if 'round' in js.keys():
            self.round = js['round']

    def print_fixture(self):
        print "[%8d] %20s %d vs %d %20s, %35s %35s" % (self.id, self.team_season_home_name, self.number_goal_team_home,
                                                       self.number_goal_team_away, self.team_season_away_name,
                                                       self.stadium,
                                                       self.schedule_date)


class Stage(AbstractFootballObj):
    def __init__(self, id, name):
        AbstractFootballObj.__init__(self, id, name)
        self.fixture_list = None
        self.url = '/v1/stages/' + str(id)

    def request_fixtures(self):
        fixtures = json.loads(self.connector.request(self.url + '/fixtures'))['docs']
        self.fixture_list = []
        for fixture in fixtures:
            id = fixture['_id']
            fixture_obj = Fixture(id, None)
            self.fixture_list.append(fixture_obj)

    def get_fixtures(self):
        return self.fixture_list


class Season(AbstractFootballObj):
    def __init__(self, id, name):
        AbstractFootballObj.__init__(self, id, name)
        self.url = '/v1/seasons/' + str(id)
        self.stages_list = None

    def request_stages(self):
        stages = json.loads(self.connector.request(self.url + '/stages'))['docs']
        # print stages
        self.stages_list = []
        for stage in stages:
            id = stage['_id']
            self.stages_list.append(Stage(id, stage['name']))

    def get_stages(self):
        return self.stages_list


class League(AbstractFootballObj):
    def __init__(self, id, name):
        AbstractFootballObj.__init__(self, id, name)
        self.url = '/v1/leagues/' + str(id)
        self.season_list = None

    def request_seasons(self):
        seasons = json.loads(self.connector.request(self.url + '/seasons'))['docs']
        self.season_list = []
        for season in seasons:
            id = season['_id']
            self.season_list.append(Season(id, season['name']))

    def get_seasons(self):
        return self.season_list


class Country(AbstractFootballObj):
    def __init__(self, name, id):
        AbstractFootballObj.__init__(self, id, name)
        self.url = '/v1/countries/' + str(id)
        self.league_list = None

    def request_leagues(self):
        leagues = json.loads(self.connector.request(self.url + '/leagues'))['docs']
        self.league_list = []
        for league in leagues:
            id = league['_id']
            self.league_list.append(League(id, league['name']))

    def get_leagues(self):
        return self.league_list


def search_player_by_name():
    pass


def get_players_list():
    pass


connector = Connector()

# if not connector.check_connection():
#     print 'No connection'
#     exit(0)

print connector.get_access_token()

# 1. Getting country list
countries = json.loads(connector.request('/v1/countries'))
country_list = []
for country in countries['docs']:
    id = country['_id']
    country_list.append(Country(country['name'], id))
    break

# print 'Country list'
# for country in country_list:
#     print country.name

# 2. Getting all leagues for each country
print 'Leagues list for country: '

league_list = []
for country in country_list:
    country.request_leagues()
    # print country.name + ':'
    for league in country.get_leagues():
        # print league.name
        league_list.append(league)

# 3. Getting all seasons for each league
print 'Seasons list for league'
season_list = []
for league in league_list:
    league.request_seasons()
    for season in league.season_list:
        season_list.append(season)

# 4. Getting all stages for each league
print 'Stages list for league'
stage_list = []
for season in season_list:
    season.request_stages()
    for stage in season.get_stages():
        stage_list.append(stage)

# 5. Getting all fixtures for each stage
print 'Fixture list for league'
fixture_list = []
for stage in stage_list:
    stage.request_fixtures()
    print stage.name + ' ' + str(len(stage.get_fixtures()))
    for fixture in stage.get_fixtures():
        fixture.request_fixture_data()
        fixture.print_fixture()
        fixture_list.append(fixture)

# req_url = '/v1/seasons/46'
# req = '/v1/seasons/'
# req2 = '/v1/players/'