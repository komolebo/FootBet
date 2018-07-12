# NVM Handler - Non Volatile Memory Handler
# module should arrange store all info to file system
import datetime
import json
import time

did_table = {}  # table of all did are present in project


# Type definitions
class DID:  # represents data identifier to convert into JSON
    path = '../Resources/'

    def __init__(self, ID, url):
        self.ID = ID
        self.url = url
        try:
            with open(self.path + str(self.ID) + '.json') as f:
                data = json.load(f)
                self.__dict__ = json.loads(data)
                self.ID = int(self.ID)
        except EnvironmentError:
            print 'env imp error'

    def export_to_file(self):
        data = json.dumps(self.__dict__)
        if len(data):
            with open(self.path + str(self.ID) + '.json', 'w') as f:
                json.dump(data, f)

    def exists_in_nvm(self):
        try:
            with open(self.path + str(self.ID) + '.json') as f:
                self.data = json.load(f)
            return True
        except EnvironmentError:
            return False


class Match(DID):
    def __init__(self, ID, url):
        self.path = DID.path + 'Matches/'
        self.score_home = None
        self.score_away = None
        self.home_team = None
        self.away_team = None
        self.home_squad = None
        self.away_squad = None
        self.sub_home_squad = None
        self.sub_away_squad = None
        self.referee = None
        self.stadium = None
        self.date = None
        self.time = None
        self.events = None
        self.visitee = None
        DID.__init__(self, ID, url)

    def set_main_info(self, score_str, home_team_name, away_team_name):
        self.home_team = home_team_name
        self.away_team = away_team_name
        self.score_home, self.score_away = score_str.split('-')

    def set_general_info(self, referee, stadium, date, time, events, visitee):
        self.referee = referee
        self.stadium = stadium
        self.date = date
        self.time = time
        self.events = events
        self.visitee = visitee

    def set_squads(self, home_squad, away_squad, sub_home_squad, sub_away_squad):
        self.home_squad = home_squad
        self.away_squad = away_squad
        self.sub_home_squad = sub_home_squad
        self.sub_away_squad = sub_away_squad


class Player(DID):
    def __init__(self, ID, url):
        self.path = DID.path + 'Players/'
        DID.__init__(self, ID, url)


class Team(DID):
    list_clubs = {}
    list_clubs_path = DID.path + 'Clubs/__list__.json'
    last_update = None

    @staticmethod
    def load_club_list():
        try:
            with open(Team.list_clubs_path) as f:
                teams_data = json.load(f)
                if teams_data.keys():
                    Team.list_clubs = teams_data['list_clubs']
                    Team.last_update = teams_data['last_update']
                    # String -> Int dictionary keys
                    # Team.list_clubs = {int(k): v for k, v in Team.list_clubs.items()}
                    Team.list_clubs = {
                        int(t_id): {
                            'name': Team.list_clubs[t_id]['name'],
                            'comps': {
                                int(c_k): c_v for c_k, c_v in Team.list_clubs[t_id]['comps'].items()
                            }
                        }
                        for t_id in Team.list_clubs.keys()}
        except EnvironmentError:
            pass

    @staticmethod
    def export_club_list():
        with open(Team.list_clubs_path, 'w') as f:
            teams_data = {'list_clubs': Team.list_clubs, 'last_update': Team.last_update}
            json.dump(teams_data, f)

    @staticmethod
    def add_comp_for_team(team_id, team_name, comp_id):
        if team_id not in Team.list_clubs.keys():  # check if no club at all
            team_info = {'name': team_name, 'comps': {comp_id: []}}
            Team.list_clubs[team_id] = team_info
        elif comp_id not in Team.list_clubs[team_id].keys():  # check if competition is not been added before
            Team.list_clubs[team_id]['comps'][comp_id] = []
        Team.export_club_list()

    @staticmethod
    def add_match_to_list(team_id, comp_id, match_id):
        if team_id not in Team.list_clubs.keys():  # check if no club at all
            raise Exception('Teams list does not contain team info')
        elif comp_id not in Team.list_clubs[team_id]['comps'].keys():  # check if competition is not been added before
            raise Exception('Teams list does not contain competition info')
        elif match_id not in Team.list_clubs[team_id]['comps'][comp_id]:
            Team.list_clubs[team_id]['comps'][comp_id].append(match_id)
            Team.export_club_list()

    @staticmethod
    def set_last_update_teams():
        Team.last_update = time.time()
        Team.export_club_list()
        print 'Teams updated at', time.time()

    def __init__(self, ID):
        self.path = DID.path + 'Clubs/'
        self.last_update = None
        self.d_comps = {}
        DID.__init__(self, ID, None)

    def add_match(self, comp_id, match_id):
        if not (comp_id in self.d_comps.keys()):
            self.d_comps[comp_id] = [match_id]
        elif not (match_id in self.d_comps[comp_id]):
            self.d_comps[comp_id].append(match_id)
        self.export_to_file()
        Team.add_match_to_list(self.ID, comp_id, match_id)

    def set_last_update(self):
        self.last_update = time.time()
        self.export_to_file()
        print 'Setting last update:', time.time()


class Competition(DID):
    comp_dict = {}
    path = DID.path + 'competitions.json'

    @staticmethod
    def export_competitions(d_comps=comp_dict):
        with open(Competition.path, 'w') as f:
            json.dump(d_comps, f)

    @staticmethod
    def import_competitions():
        with open(Competition.path, 'r') as f:
            Competition.comp_dict = json.load(f)


class NVM:
    PATH_MATCHES = 'Matches/'
    PATH_CLUBS = 'Players/'
    PATH_PLAYERS = 'Clubs/'

    def __init__(self):
        pass

    @staticmethod
    def check_obj_in_nvm(path, ID):
        obj_path = DID.path + path + ID + '.json'
        try:
            with open(obj_path) as f:
                pass
            return True
        except EnvironmentError:
            return False
