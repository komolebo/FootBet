from BeautifulSoup import BeautifulSoup

from Informer.api_data import req_url, HTML_League, HTML_Season, CommonAPI


def analyze_match_page(url):
    print 'analyzing %s' % url

    page = req_url(url)
    match_page = BeautifulSoup(page)

    away_team, home_team, score = analyze_match_team_score(match_page)
    print "%s vs %s [%s]" % (home_team, away_team, score)

    date, referee, stadium, time, visitee = analyze_match_general_info(match_page)
    print date, time, stadium, referee, visitee

    team_home, team_away, sub_home, sub_away = analyze_match_squads(match_page)
    # print team_home, team_away, sub_home, sub_away
    for player1, player2 in zip(team_home, team_away):
        print "!%30s %30s!" % (player1[0], player2[0])

    events = analyze_match_events(match_page)
    print events


def analyze_match_general_info(match_page):
    general_tags = match_page.findAll('div', {'class': 'matchStatsInt'})
    date = general_tags[0].text
    time = general_tags[1].text
    stadium = general_tags[2].text
    referee = general_tags[3].text
    visitee = general_tags[4].text
    return date, referee, stadium, time, visitee


def analyze_match_team_score(match_page):
    # score
    score_tags = match_page.findAll('div', {'class': 'matchReportTitle'})
    # for i in score_tag:
    #     print i #score_tag
    score_tag = score_tags[0]
    score_tags = score_tag.findAll('h2')
    home_team = score_tags[0].text
    away_team = score_tags[2].text
    score = score_tags[1].text
    return [away_team, home_team, score]


def analyze_match_events(match_page):
    events = []
    event_tags = match_page.findAll('div', {'class': 'matchReportSubInt'})
    for event in event_tags:
        events.append((event.find('p').text, event.find('small').text))
    return events


def analyze_tag_player(player_tag):
    sub_ref = player_tag.find('a')['href']
    id = sub_ref.split('player_id=', 1)[1]
    player_data = player_tag.find('div', {'class': 'playerName'}).text
    name, position = player_data.split(',')
    return name, position, id


def analyze_squad(squad):
    squad_players = []
    for player_tag in squad:
        player = analyze_tag_player(player_tag)
        squad_players.append(player)
    return squad_players


def analyze_match_squads(match_page):
    match_squads_tags = match_page.findAll('ul', {'class': 'matchSquads'})
    # 0 home, 1 away, 2 home sub, 3 away sub
    home_squad = analyze_squad(match_squads_tags[0].findAll('li'))
    away_squad = analyze_squad(match_squads_tags[1].findAll('li'))
    sub_home_squad = analyze_squad(match_squads_tags[2].findAll('li'))
    sub_away_squad = analyze_squad(match_squads_tags[3].findAll('li'))
    return home_squad, away_squad, sub_home_squad, sub_away_squad


def get_leagues(parsed_page):
    html_leagues = parsed_page.findAll('div', {'class': 'intRight'})
    leagues = []
    for div in html_leagues:
        tags = div.findAll('a')
        for tag in tags:
            league_href = tag['href']
            league_name = tag.find('span').text
            leagues.append(HTML_League(league_href, league_name))
    return leagues


def get_seasons_for_league(league_obj, parsed_league_page):
    # search all seasons for league
    seasons_url = parsed_league_page.findAll('select', {'name': 'comp_id'})
    for season in seasons_url:
        for option in season.findAll('option'):
            comp_id = option['value']
            # if not 'Select' in option.text:
            if int(comp_id) >= 0:
                league_obj.seasons.append(HTML_Season(comp_id, option.text))
        # print season.findAll('option')
    # TODO


def get_seasons_for_leagues(api_leagues):
    for league_obj in api_leagues:
        league_page = req_url(league_obj.url)
        parsed_league_page = BeautifulSoup(league_page)
        get_seasons_for_league(league_obj, parsed_league_page)


def get_matches_from_season(league_obj, season_obj):
    for offset in range(0, 1000, 10):
        try:
            url = CommonAPI.url + (
                    'competitions/LastMatches?comp_id=%s&offset=%s' % (season_obj.comp_id, str(offset)))
            # Here we should grab all matches from season
            page = req_url(url)
            parsed_page = BeautifulSoup(page)

            html_matches = parsed_page.findAll('span', {'class': 'matchVs'})
            if not len(html_matches):
                break
            for html_match in html_matches:
                match_url = html_match.find('a')['href']
                analyze_match_page(match_url)
        except Exception:
            print 'Pages end for league=%u season=%u' % (league_obj.name, season_obj.name)
            break

        # for season in league_obj.seasons:
        # matches_url = parsed_page.findAll('a', {'title': season + ' Latest results'})
        # print matches_url, season