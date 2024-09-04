from main import app  # Flask instance of the API


def test_get_teams_no():
    response = app.test_client().get('/get-teams/fghrt')

    assert response.status_code == 201
    assert response.data.decode('utf-8') == '[]\n'


def test_get_teams_route():
    response = app.test_client().get(
        '/get-teams/spieltagsuebersichtSLASHnofv-oberliga-sued-deutschland'
        '-oberliga-herren-saison2324-deutschlandSLASH-SLASHstaffelSLASH'
        '02PUNGDIE800000AVS5489B4VVTKJJ35-G#!')

    assert response.status_code == 201
    assert response.data.decode('utf-8').split(',').sort() == [
        "BSG Wismut Gera", "1. FC Magdeburg II", "VfL Halle 96", "FC Grimma",
        "FC Einheit Rudolstadt", "VfB Germania Halberstadt",
        "Bischofswerdaer FV 08", "Ludwigsfelder FC", "FSV Budissa Bautzen",
        "SC Freital", "SV Blau-Weiß Zorbau", "SG Union Sandersdorf",
        "FC Einheit Wernigerode", "VfB 1921 Krieschow", "RSV Eintracht 1949",
        "VfB Auerbach"].sort()
    assert len(response.data.decode('utf-8').split(',')) == 16


def test_get_matches_no():
    response = app.test_client().get('/get-matches/hhh/hh/5')

    assert response.status_code == 202
    assert response.data.decode('utf-8') == '[]\n'


def test_get_matches_index():
    response = app.test_client().get(
        '/get-matches/VFBSPACEStuttgart/spieltagsuebersichtSLASHoberliga'
        '-baden-wuerttemberg-deutschland-frauen-oberliga-baden-wuerttemberg'
        '-frauen-saison2223-deutschlandSLASH-SLASHstaffel'
        'SLASH02ID713OQG000009VS5489B3VS27R2HJ-G/12')

    assert response.status_code == 500
    # assert response.data.decode('utf-8') == '[]\n'


def test_get_matches_route():
    import json
    response = app.test_client().get(
        '/get-matches/WerderSPACEBremen/spieltagsuebersichtSLASHa-junioren-bundesliga'
        '-nord-nordost-deutschland-a-junioren-bundesliga-a-junioren-saison2324-deutschland'
        'SLASH-SLASHstaffelSLASH02LNP13E6C00000HVS5489B4VUAB0UC4-G/3')

    assert response.status_code == 202
    data = json.loads(response.data)
    assert data[0]['match_day'] == 1
    assert data[1]['match_day'] == 2
    assert data[0]['team'] == 'Werder Bremen'
    assert data[1]['team'] == 'Werder Bremen'
    assert data[0]['team_logo_src'] == 'www.fussball.de/export.media/-/action/getLogo/' \
        'format/2/id/00ES8GN8I400001CVV0AG08LVUPGND5I/verband/0123456789ABCDEF0123456700004010'
    assert data[1]['team_logo_src'] == 'www.fussball.de/export.media/-/action/getLogo/' \
        'format/2/id/00ES8GN8I400001CVV0AG08LVUPGND5I/verband/0123456789ABCDEF0123456700004010'
    assert data[0]['opponent'] == 'Hamburger SV'
    assert data[1]['opponent'] == 'VfL Wolfsburg'
    assert data[0]['opponent_logo_src'] == 'www.fussball.de/export.media/-/action/getLogo/' \
        'format/2/id/00ES8GN8I400006JVV0AG08LVUPGND5I/verband/0123456789ABCDEF0123456700004010'
    assert data[1]['opponent_logo_src'] == 'www.fussball.de/export.media/-/action/getLogo/' \
        'format/2/id/00ES8GN77K00000JVV0AG08LVUPGND5I/verband/0123456789ABCDEF0123456700004010'
    assert data[0]['home_game'] == False
    assert data[1]['home_game'] == True
    assert data[2]['home_game'] == False
