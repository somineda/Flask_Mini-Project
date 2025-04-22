#사용자 모델을 정의
class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password