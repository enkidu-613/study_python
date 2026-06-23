def test_websocket_echo(client):
    with client.websocket_connect("/ws/message") as websocket:
        websocket.send_text("你好")
        response = websocket.receive_text()
        assert response == "你说的是你好"
