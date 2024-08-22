def test_display_animals(web_client):
    response = web_client.get("/listings")
    assert response.status_code == 200
    # assert response.data.decode("utf-8") == ":)"