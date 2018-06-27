# NVM Handler - Non Volatile Memory Handler
# module should arrange store all info to file system
import json

# Global data
did_config_table = {
    0xF001: 'Football clubs identifiers',
    0xF002: 'Football fixtures identifiers'
}

did_table = {}  # table of all did are present in project


# Type definitions
class DID:  # represents data identifier to convert into JSON
    file_path = '../Resources/'

    def __init__(self, ID, desc):
        self.data = None
        self.desc = desc
        self.ID = ID

    def set_data(self, data):
        assert type(data) == dict
        self.data = data

    def get_data(self):
        return self.data

    def export_to_file(self):
        try:
            with open(self.file_path + str(self.ID) + '.json', 'w') as f:
                file_data = {
                    'description': self.desc,
                    'data': self.data
                }
                json.dump(file_data, f)
        except EnvironmentError:
            print 'env exp error'
            pass

    def import_from_file(self):
        try:
            with open(self.file_path + str(self.ID) + '.json') as f:
                file_data = json.load(f)
                if dict(file_data).keys():
                    assert self.desc == file_data['description']
                    self.data = file_data['data']
        except EnvironmentError:
            print 'env imp error'
            pass


# Local functions
def did_init():
    for did in did_config_table:
        desc = did_config_table[did]
        did_obj = DID(did, desc)
        did_obj.import_from_file()
        did_table[did] = did_obj
        # just create file
        did_obj.export_to_file()


if __name__ == '__main__':
    did_init()
