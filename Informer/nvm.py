# NVM Handler - Non Volatile Memory Handler
# module should arrange store all info to file system
import json

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
        except EnvironmentError:
            print 'env imp error'

    def export_to_file(self):
        data = json.dumps(self.__dict__)
        if len(data):
            with open(self.path + str(self.ID) + '.json', 'w') as f:
                json.dump(data, f)

    # def import_from_file(self):
    #     try:
    #         with open(self.path + str(self.ID) + '.json') as f:
    #             self.data = json.load(f)
    #     except EnvironmentError:
    #         print 'env imp error'
    #         self.data = {}
    #         pass

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
        DID.__init__(self, ID, url)
        self.path = DID.path + 'Players/'


class Club(DID):
    def __init__(self, ID, url):
        DID.__init__(self, ID, url)
        self.path = DID.path + 'Clubs/'


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

# Local functions
# def did_init():
#     for did in did_config_table:
#         desc = did_config_table[did]
#         did_obj = DID(did)
#         did_obj.import_from_file()
#         did_table[did] = did_obj
#         # just create file
#         did_obj.export_to_file()


# if __name__ == '__main__':
#     did_init()
