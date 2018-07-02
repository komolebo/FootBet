# NVM Handler - Non Volatile Memory Handler
# module should arrange store all info to file system
import json

did_table = {}  # table of all did are present in project


# Type definitions
class DID:  # represents data identifier to convert into JSON
    path = '../Resources/'

    def __init__(self, ID):
        self.data = {}
        self.ID = ID

    def set_data(self, data):
        assert type(data) == dict
        self.data = data

    def get_data(self):
        return self.data

    def export_to_file(self):
        if len(self.data):
            try:
                with open(self.path + str(self.ID) + '.json', 'w') as f:
                    json.dump(self.data, f)
            except EnvironmentError:
                print 'env exp error'
                pass

    def import_from_file(self):
        try:
            with open(self.path + str(self.ID) + '.json') as f:
                self.data = json.load(f)
        except EnvironmentError:
            print 'env imp error'
            self.data = {}
            pass


class Match(DID):
    def __init__(self, ID):
        DID.__init__(self, ID)
        self.path = DID.path + 'Matches/'


class Player(DID):
    def __init__(self, ID):
        DID.__init__(self, ID)
        self.path = DID.path + 'Players/'


class Club(DID):
    def __init__(self, ID):
        DID.__init__(self, ID)
        self.path = DID.path + 'Clubs/'


class NVM:
    PATH_MATCHES = 'Matches/'
    PATH_CLUBS = 'Players/'
    PATH_PLAYERS = 'Clubs/'

    def __init__(self):
        pass

    def check_obj_in_nvm(self, path, ID):
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
