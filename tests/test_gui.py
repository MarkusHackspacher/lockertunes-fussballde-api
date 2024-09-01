from main import app  # Flask instance of the API


def test_index_route():
    response = app.test_client().get('/')

    assert response.status_code == 200
    assert response.data.decode('utf-8')[:15] == '<!DOCTYPE html>'


def test_second_route():
    response = app.test_client().get('/second_gui')

    assert response.status_code == 500
    assert response.data.decode('utf-8')[:15] == '<!doctype html>'


def test_third_route():
    response = app.test_client().get('/third_gui')

    assert response.status_code == 200
    assert response.data.decode('utf-8') == 'Keine Daten ausgewählt.'
