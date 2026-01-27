class Session:
    user = None
    role = None  # "admin" ou "user"

    @classmethod
    def login(cls, username, role):
        cls.user = username
        cls.role = role

    @classmethod
    def logout(cls):
        cls.user = None
        cls.role = None
