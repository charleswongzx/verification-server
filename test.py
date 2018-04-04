import os
import server
import unittest
import tempfile


class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, server.app.config['DATABASE'] = tempfile.mkstemp()
        server.app.testing = True
        self.app = server.app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(server.app.config['DATABASE'])

    # HOMEPAGE TESTS
    def testHomePage(self):
        rv = self.app.get('/')
        assert b'Welcome to the MyFace Verification Server!' in rv.data

    # NEW USER CONFIRM TESTS
    def testNewUserConfirmSuccess(self):
        data = dict(
            uid='NEWUSER123'
        )
        rv = self.app.get('/new-user-confirm/', query_string=data)
        assert b'Email confirmation successful! Redirecting to MyFace to login...' in rv.data

    def testNewUserConfirmNoUid(self):
        data = dict()
        rv = self.app.get('/new-user-confirm/', query_string=data)
        assert b'No uid in args!' in rv.data

    def testNewUserConfirmNoSuchUser(self):
        data = dict(
            uid='NONEXISTENT'
        )
        rv = self.app.get('/new-user-confirm/', query_string=data)
        assert b'No such user exists!' in rv.data

    # NEW KYC SUBMIT TESTS
    def testNewKycSubmitSuccess(self):
        data = dict(
            uid='NEWUSER123',
            selfie_url='https://firebasestorage.googleapis.com/v0/b/kyc-app-db.appspot.com/o/selfie%20with%20driving%20license?alt=media&token=74e7a621-7642-4c5b-9b5d-31dfb6f7775f',
            passport_url='https://firebasestorage.googleapis.com/v0/b/kyc-app-db.appspot.com/o/0321%200900%20Charles%20Wong.jpg?alt=media&token=24dea5e5-2dc2-4d60-81f2-616b19d0da6e'
        )
        rv = self.app.put('/api/v1/new-kyc-submit/', data=data)
        assert b"KYC APPROVED" in rv.data

    def testNewKycSubmitMismatch(self):
        data = dict(
            uid='NEWUSER123',
            selfie_url='https://firebasestorage.googleapis.com/v0/b/kyc-app-db.appspot.com/o/selfie%20with%20driving%20license?alt=media&token=74e7a621-7642-4c5b-9b5d-31dfb6f7775f',
            passport_url='https://firebasestorage.googleapis.com/v0/b/kyc-app-db.appspot.com/o/4CC09F46-DD71-477B-A1C9-197455BE2106%20-%20Joel%20Tan.jpeg?alt=media&token=127b241d-72e3-41cb-8ba5-3bd2e97a20ba'
        )
        rv = self.app.put('/api/v1/new-kyc-submit/', data=data)
        assert b"KYC REJECTED" in rv.data

    def testNewKycSubmitNoUid(self):
        data = dict(
            selfie_url='https://firebasestorage.googleapis.com/v0/b/kyc-app-db.appspot.com/o/selfie%20with%20driving%20license?alt=media&token=74e7a621-7642-4c5b-9b5d-31dfb6f7775f',
            passport_url='https://firebasestorage.googleapis.com/v0/b/kyc-app-db.appspot.com/o/4CC09F46-DD71-477B-A1C9-197455BE2106%20-%20Joel%20Tan.jpeg?alt=media&token=127b241d-72e3-41cb-8ba5-3bd2e97a20ba'
        )
        rv = self.app.put('/api/v1/new-kyc-submit/', data=data)
        assert b'No uid in args!' in rv.data

    def testNewKycSubmitNoSuchUser(self):
        data = dict(
            uid='NONEXISTENT',
            selfie_url='https://firebasestorage.googleapis.com/v0/b/kyc-app-db.appspot.com/o/selfie%20with%20driving%20license?alt=media&token=74e7a621-7642-4c5b-9b5d-31dfb6f7775f',
            passport_url='https://firebasestorage.googleapis.com/v0/b/kyc-app-db.appspot.com/o/4CC09F46-DD71-477B-A1C9-197455BE2106%20-%20Joel%20Tan.jpeg?alt=media&token=127b241d-72e3-41cb-8ba5-3bd2e97a20ba'
        )
        rv = self.app.put('/api/v1/new-kyc-submit/', data=data)
        assert b'No such user!' in rv.data

    def testNewKycSubmitNoSelfie(self):
        data = dict(
            uid='NEWUSER123',
            passport_url='https://firebasestorage.googleapis.com/v0/b/kyc-app-db.appspot.com/o/4CC09F46-DD71-477B-A1C9-197455BE2106%20-%20Joel%20Tan.jpeg?alt=media&token=127b241d-72e3-41cb-8ba5-3bd2e97a20ba'
        )
        rv = self.app.put('/api/v1/new-kyc-submit/', data=data)
        assert b'No selfie_url in args!' in rv.data

    def testNewKycSubmitNoPassport(self):
        data = dict(
            uid='NEWUSER123',
            selfie_url='https://firebasestorage.googleapis.com/v0/b/kyc-app-db.appspot.com/o/selfie%20with%20driving%20license?alt=media&token=74e7a621-7642-4c5b-9b5d-31dfb6f7775f',
        )
        rv = self.app.put('/api/v1/new-kyc-submit/', data=data)
        assert b'No passport_url in args!' in rv.data

    # NEW USER SUBMIT TESTS
    def testNewUserSubmitSuccess(self):
        data = dict(
            uid='NEWUSER123',
            email='charlescrinkle@gmail.com'
        )
        rv = self.app.put('/api/v1/new-user-submit/', data=data)
        assert b'Email success' in rv.data

    def testNewUserSubmitNoUid(self):
        data = dict(
            email='charlescrinkle@gmail.com'
        )
        rv = self.app.put('/api/v1/new-user-submit/', data=data)
        assert b'No uid in args!' in rv.data

    def testNewUserSubmitNoEmail(self):
        data = dict(
            uid='NEWUSER123'
        )
        rv = self.app.put('/api/v1/new-user-submit/', data=data)
        assert b'No email in args!' in rv.data

    def testNewUserSubmitInvalidEmail(self):
        data = dict(
            uid='NEWUSER123',
            email='WRONG EMAIL@yah0.wrong'
        )
        rv = self.app.put('/api/v1/new-user-submit/', data=data)
        assert b'Email failed' in rv.data


if __name__ == '__main__':
    unittest.main()
