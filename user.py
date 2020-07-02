from werkzeug.security import check_password_hash


class User:

    def __init__(self, username, mobile,email,password):
        print('init method #',username)
        self.username = username
        self.mobile = mobile
        self.email = email
        self.password = password

    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def is_anonymous():
        return False
    '''
    def get_id(self):
        return self.username
    '''

    def get_id(self):
        return self.email

    def check_password(self, password_input):
        return check_password_hash(self.password, password_input)