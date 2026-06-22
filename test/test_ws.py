
# 测试ws路由message
def test_websocket_echo(client):
    with client.websocket_connect("/ws/message") as websocket: #这里的with 在调用websocket_connect创建websocket对象后会自动打开websocket.__enter__(self方法)
        websocket.send_text("你好")
        response = websocket.receive_text()
        assert response == "你说的是你好"