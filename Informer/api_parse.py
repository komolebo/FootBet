from BeautifulSoup import BeautifulSoup

from Informer.api_data import req_url, HTML_League, HTML_Season, CommonAPI, bug_fix, HTML_Club
from Informer.nvm import Match, NVM, Team


def analyze_match_page(url):
    id = url.split('match_id=', 1)[1].split('&')[0]

    match = Match(int(id), url)
    if not NVM.check_obj_in_nvm(NVM.PATH_MATCHES, id):  # match.exists_in_nvm():
        page = req_url(url)
        match_page = BeautifulSoup(page)

        away_team, home_team, score = analyze_match_team_score(match_page)
        print "%s vs %s [%s]" % (home_team, away_team, score)

        date, referee, stadium, time, visitee = analyze_match_general_info(match_page)
        # print date, time, stadium, referee, visitee

        squad_home, squad_away, sub_squad_home, sub_squad_away = analyze_match_squads(match_page)
        # print squad_home, squad_away, sub_squad_home, sub_squad_away
        # for player1, player2 in zip(squad_home, squad_away):
        #     print "!%30s %30s!" % (player1[0], player2[0])

        events = analyze_match_events(match_page)
        # print events
        match.set_general_info(referee, stadium, date, time, events, visitee)
        match.set_main_info(score, home_team, away_team)
        match.set_squads(squad_home, squad_away, sub_squad_home, sub_squad_away)
        # match.set_data()
        match.export_to_file()
    else:
        print 'skipping %s' % url
    return match


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
        event_text = event.find('p').text
        event_additional_text_info = event.find('small').text if event.find('small') else None
        events.append((event_text, event_additional_text_info))
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


def get_seasons_for_league(league_url):
    league_page = req_url(league_url)
    parsed_league_page = BeautifulSoup(league_page)
    seasons = []
    # search all seasons for league
    seasons_url = parsed_league_page.findAll('select', {'name': 'comp_id'})
    for season in seasons_url:
        for option in season.findAll('option'):
            comp_id = option['value']
            # if not 'Select' in option.text:
            if int(comp_id) >= 0:
                seasons.append(HTML_Season(comp_id, option.text))
        # print season.findAll('option')
    return seasons
    # TODO


def get_seasons_for_leagues(api_leagues):
    for league_obj in api_leagues:
        league_obj.seasons = get_seasons_for_league(league_obj.url)


def get_matches_from_season(league_obj, season_obj):
    for offset in range(0, 1000, 10):
        try:
            url = CommonAPI.url + (
                    'competitions/LastMatches?comp_id=%s&offset=%s' % (season_obj.comp_id, str(offset)))
            # Here we should grab all matches from season
            page = req_url(url)
            parsed_page = BeautifulSoup(page)

            html_matches = parsed_page.findAll('span', {'class': 'matchVs'})
            if not len(html_matches):  # All matches are processed
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


def get_clubs_from_season_url(comp_id):
    clubs_for_league = []

    comp_url = CommonAPI.url + '/competitions/LeagueTable?comp_id=%s' % comp_id
    league_page = req_url(comp_url)
    league_page = bug_fix(league_page)
    parsed_league_page = BeautifulSoup(league_page)

    html_teams = parsed_league_page.findAll('td', {'class': 'mob tdInline'})
    for html_team in html_teams:
        # TODO add parsing for cups
        team_name = html_team.find('a').text
        club_href = html_team.find('a')['href']
        team_id = club_href.split('club_id=', 1)[1]

        clubs_for_league.append(HTML_Club(team_id, team_name))
        Team.add_comp_for_team(team_id, team_name, comp_id)

        print team_id, '::', team_name
        # if not (html_team.find('a').has_key('href')):
        #     print 'error', html_team

    return clubs_for_league


def get_matches_from_team(comp_id, team_id):
    matches = []
    for offset in range(0, 10000, 10):
        # try:
        url = CommonAPI.url + (
                'competitions/LastMatches?comp_id=%s&club_id=%s&offset=%s' % (comp_id, team_id, offset))
        # Here we should grab all matches from season
        page = req_url(url)
        parsed_page = BeautifulSoup(page)

        html_matches = parsed_page.findAll('span', {'class': 'matchVs'})
        if not len(html_matches):  # All matches are processed
            break
        for html_match in html_matches:
            match_url = html_match.find('a')['href']
            match = analyze_match_page(match_url)
            matches.append(match)
        # except Exception:
        #     print 'Pages end for club=%u comp=%u' % (team_id, comp_id)
        #     break
    return matches


def get_competitions():
    # Search all leagues
    main_page = req_url(CommonAPI.url)
    parsed_main_page = BeautifulSoup(main_page)
    api_leagues = get_leagues(parsed_main_page)
    # search all seasons in leagues
    get_seasons_for_leagues(api_leagues)
    # search all matches in league season
    competitions = [comp for league in api_leagues for comp in league.seasons]
    return competitions
