import urllib2
from time import sleep

from nvm import Match, Club, Player

# id_session = 'qvR8qvPZO%2BnYV8wHS0%2Bi9QY2hcFa4YJsLSKsr4JcVTGHwdCoCGBHHQkTgX%2FFBAc57qNKjVgCA2NKo8JGMocQ%2FB0PVc9KTu9uhsLGMf61UO1V6wLdApgtiGIKT3M2nCr7WjsgRt0jLgKmjODEsl6DLcm6zzOVz7%2Ba6Z%2BQdlso8vysuyLNuSpFED7RzpyUHZjGAX7KlYIPGKt1hNR3MnZbcnRzVNgZuAkoLXZKXOLXYLX26bFYlorKOWBS87uCPdP6mU2Yol1JtrsN%2Bbcc1QP0Yjzb1nmfHxib57aCMPEOy7OYeD5Q0DM1jBvrLlCVnJf13Foql7rxcOHhRsJrWp1S6p9i3%2Biq%2FnNPpxFn%2BnCRI4D4xB02cEg7U2ntt4uWbOtTNmyBWgcHS5EDxndlpRjAQa%2F0MrUnGB72yps1Tbp348QQ%2FwtlfvISFz8nGpjuJMYjPXFsMUn8O3e7ltp4BDIpGSpZ24RVpeh8O0memBf09xe9IRtF6AfNKf1pFRwoifcNd08NYaiag248V5I3km4NktNQgBpejFoWFiuJEcYTWjQdbq32E%2FbJFFNIAzj5a%2BY%2BNgeT3jm0BgodP0yIvIzYIBL1DZt4Ods06lIC04GFvR4UFjlDYEzSKlFzknXjZMsX4bTJ6y9v0VGd%2F85q51xJmX3Egrz0R%2B0vUa%2BzKjlpxgbJbmSaErHDX4XdHzhj0Zumxz%2FHtYBICBHddxjvPXW3bsT8CFjYrjfGaDAG9xqigXt81w9rQ4FuE4bMtl7KOzIj5DxY4Suandn34hp9YAMwvDD0g6L2sDNqGKdOitKD8LGEbgphYl6XI1SqKxLbUpnD2f7oUqD5rqmUCTH70FKJhmTPiB%2BUqRvNYnin7JJ5loPPnsx1OlAfNYN4n%2FbTva3297rKFWb%2BHToiesYPUY4NU9bwI5wQL6VYvD5g8cnJwmrt3Wu%2FgzdL1OB3FObTuZvFU2Hi2wbug3%2FLmWrXYty6Tp5Qsp4ZZeC%2BAol3uKiiKqm2yYCFor5f37WdspgPRQ36mj%2FJMVQjo0D0ZMRZmSJJOoKkkuCeX5%2BYgwW7QvhNaz%2BcZ49z%2F16hmkS1ZLS8OBpVdMHF2D7wRgEZAn1bYoRIMRW41fuH7S9MF%2Fzo91wNpyqSo9aHiREwWmi5uZ7ISAx1gUDqAUKN25cY1pkJLIAGW8Edi29sSHoOY536IJjjNN2TbFn3q%2BhtoUoH2fcRdjx6N%2BDWraBG3X97DJGFlGRmLs8MbY%2BiuLEkYlNE4oYAag6WToJ3LP1aA%2FwMdXkWjoi2'
id_session = 'juozHsae1QgDtPqOKsWM8S5fUt%2BqOBYLtm6Wfll036ELR3fQQ7pa9I3x9r7O3WLVv%2B5Y%2BQKULyIhxZZGmL3GF64CPQWgyi%2B4yzbR05fE3lIT7MJxaO%2FTNVjdWl6YNi2ot0fWsbpuhlm%2BjislaU%2FU5ZBuJh2htcgyxmXakLTc9tiUmrDoaGU12WX48HuaWwShd6oXcUJYLetMA5MuJsyNmXzXpD4fPvF1Ow0BJj2ThkttmTZjECiAmDqGuA6IDFsI%2Fk2JG7eKTkE%2FxU7QgXV45XbXAtfW%2FvZZy7zjwgRwRXP8E1kT7OWiDjVTSbJf56bGt8qWxEgpS0VBD096Vx%2FYH%2BHvq0zVQ%2BxomZFd3UPb5QKOLTKW3huaN0Fziri8KGKuuXL6uFcn5UCt%2FFRWNnrDeKmCHP1auMle04pbznYgp2z1CgtsfM6HQd3yh9Gjpf87QKx%2FJsWtWvVsdYAiFDmStViFMZaI4V0XSUCyyfha8PU73Vm5xBfZ0ObMK%2F1Fjq6r8CTTHZoZmfATfTeWpL3ZOs%2BrcEHbZFvswiWRRmo24IED2jyVTJxcICSXQuS5GKhZZGw%2FmLk1X5kgfM0lHsckFNYTHkybLmq6DKrOrIfAdG%2FDnblpqVSUp3XrwwW7KnDiIZFNO4UXzRok9C4CR6zQbjdEKrQoYRUrfBBrdLWpT9Ydkjq%2FO3NaDDz%2Fj7BAJ861orJRBpaA7STQoj%2BLLPBerl9WiYfvyTYDxwBVBAycl46HFX3aUEFAH72brdlIZIRIJMh8ReIyXBgBH0%2FT2UDnmLZxx9q5%2BrPmJv8EoqUW4M0cR%2FRI2pRndHDBAjE8r8FkVB51PgIh5bJ6zrAAvfAa5HMwa9qq3Rcnt5doMvrW62e8GNpgQ3KhqUK8XAEhqxMxButzFShhjCTAtfv5HGrQs7Q3JKlr%2F19RYbmIJ4cYdsQJDE1UCbZgQWkylU8DEwvqhzP9gLRnUG6BoXkgOfIl0KmVGKMO95ZsoNVtS9CwuxRx3VnCcAvzLkaAILUs7Q3ejWjCBOc%2F%2Fq0NmR69GKXeRvbyIFpt12ERotVTlxf5jKFiqIbuuAnBjULKeoZkgy5Ozg7IHu4F01TwkYFWzvF%2BgdyuAp3lIgMojOM33QP%2FcAXmLfnocCoTuo1neGwEb9Hgml4PhZfqybrXDkW94WW6c22JEJ6Qlh4qfqpIRcr%2Fg1COWIcBulDLoQFbA3MFwMWTsN3SZnr7tvMyAB13VwCMf%2FcrWpFeZdXvoH2f41osiMmkaSoDRNC0cR7e8IXoGxLs'


class CommonAPI:
    url = 'https://www.statbunker.com/'

    def __init__(self):
        pass


class PlayerAPI(Player, CommonAPI):
    def __init__(self, ID):
        Player.__init__(self, ID)


class MatchAPI(Match, CommonAPI):
    def __init__(self, ID, match_url):
        Match.__init__(self, ID)
        self.match_url = match_url
        # self.league_name = league_name
        # self.comp_id = comp_id
        # self.date = date
        # self.name = name


class HTML_Club():
    def __init__(self, ID, name):
        self.club_id = ID
        self.name = name


class HTML_Season:
    def __init__(self, comp_id, name):
        self.name = name
        self.comp_id = comp_id


class HTML_League:
    def __init__(self, url, name):
        self.url = url
        self.name = name
        self.seasons = []


def req_url(url):
    print 'requesting', url

    opener = urllib2.build_opener()
    opener.addheaders.append(('Cookie', 'footballci_session=' + id_session))
    resp = opener.open(url)
    sleep(1)
    return resp.read()


def bug_fix(page):
    # API Bug fix #1: Borussia M' causes html parsing error
    if 'Borussia M' in page:
        page = page.replace("Borussia M\'", "Borussia M\"")

    return page