from app.shared.config import cfg


def test_get_results_404_sotw_not_found(client):
    # When
    response = client.get(f"{cfg.API_V1_STR}/results/3/0")
    data = response.json()

    # Then
    assert response.status_code == 404
    assert data["detail"] == "Sotw with given id 3 not found."


def test_get_results_403(client, sotw):
    # When
    response = client.get(f"{cfg.API_V1_STR}/results/1/0")

    # Then
    assert response.status_code == 403


def test_post_response_404_week_not_found(client, current_week):
    # When
    response = client.get(f"{cfg.API_V1_STR}/results/1/4")
    data = response.json()

    # Then
    assert response.status_code == 404
    assert data["detail"] == "Week 4 not found for sotw 1."


def test_get_results_success(client, current_week_new_week_new_results):
    # When
    # kick off the new week
    response = client.get(f"{cfg.API_V1_STR}/week/1/current_week")
    data = response.json()

    assert response.status_code == 200
    assert "week_num" in data.keys()
    assert data["week_num"] == 2

    # get results from previous week
    response = client.get(f"{cfg.API_V1_STR}/results/1/1")
    data = response.json()

    # Then
    assert response.status_code == 200
    assert "first_place" in data.keys()
    assert (
        data["first_place"]
        == '["Doctor Worm - They Might Be Giants", "Headlock - Snail Mail", "Lithonia - Childish Gambino"]'
    )
    assert "second_place" in data.keys()
    assert data["second_place"] == "[]"
    assert "all_songs" in data.keys()
    assert (
        data["all_songs"]
        == '{"1": {"name": "Doctor Worm - They Might Be Giants", "voters": ["test2", "test3"], "submitter": "test1", "spotify_id": "6OmApaLQPqHZL3iI78FOUR"}, "2": {"name": "Headlock - Snail Mail", "voters": ["test1", "test3"], "submitter": "test2", "spotify_id": "5mqceEgI5vhogd5pOAlwUO"}, "3": {"name": "Lithonia - Childish Gambino", "voters": ["test1", "test2"], "submitter": "test3", "spotify_id": "4JfpJrrGNXRj2yXm1fYV23"}}'
    )
    assert "guessing_data" in data.keys()
    assert "theme" in data.keys()
    assert data["theme"] == ""
    assert "theme_description" in data.keys()
    assert data["theme_description"] == ""

def test_get_results_success_themed(client, current_week_new_week_new_results_themed_survey):
    # When
    # kick off the new week
    response = client.get(f"{cfg.API_V1_STR}/week/1/current_week")
    data = response.json()

    assert response.status_code == 200
    assert "week_num" in data.keys()
    assert data["week_num"] == 3

    # get results from previous week
    response = client.get(f"{cfg.API_V1_STR}/results/1/2")
    data = response.json()

    # Then
    assert response.status_code == 200
    assert "first_place" in data.keys()
    assert (
        data["first_place"]
        == '["Doctor Worm - They Might Be Giants", "Headlock - Snail Mail", "Lithonia - Childish Gambino"]'
    )
    assert "second_place" in data.keys()
    assert data["second_place"] == "[]"
    assert "all_songs" in data.keys()
    assert (
        data["all_songs"]
        == '{"4": {"name": "Doctor Worm - They Might Be Giants", "voters": ["test2", "test3"], "submitter": "test1", "spotify_id": "6OmApaLQPqHZL3iI78FOUR"}, "5": {"name": "Headlock - Snail Mail", "voters": ["test1", "test3"], "submitter": "test2", "spotify_id": "5mqceEgI5vhogd5pOAlwUO"}, "6": {"name": "Lithonia - Childish Gambino", "voters": ["test1", "test2"], "submitter": "test3", "spotify_id": "4JfpJrrGNXRj2yXm1fYV23"}}'
    )
    assert "guessing_data" in data.keys()
    assert "theme" in data.keys()
    assert data["theme"] == "THEME"
    assert "theme_description" in data.keys()
    assert data["theme_description"] == "THEME DESCRIPTION"


def test_get_results_404_not_ready(client, current_week_new_week_new_results):
    # When
    # get results from previous week
    response = client.get(f"{cfg.API_V1_STR}/results/1/1")
    data = response.json()

    # Then
    assert response.status_code == 200
    assert "message" in data.keys()
    assert data["message"] == "Results for week 1 for test not yet available."
