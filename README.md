# MyFace Verification Server

Intermediary between client app and database for image verification.
## Getting Started

This project is built to be deployed on Heroku, but can be run locally as well.
### Prerequisites

* python 3.6
* pip

### Installing

Install requirements using pip:

```
pip3 install -r requirements.txt
```

To run server:

```
python server.py
```

Use Postman or similar API-testing app for fast debug.

## Running the tests

Tests are run using the built-in unittest python module.

To run all tests, run the following:
```
python -m unittest
```

### API Tests

Server endpoints were tested for maximum code coverage.

**Test Case**|**Endpoint**|**Function**
:-----:|:-----:|:-----:
Homepage is accessible|/|testHomePage
User email confirmation successful|/new-user-confirm/|testNewUserConfirmSuccess
No uid in email confirmation request|/new-user-confirm/|testNewUserConfirmNoUid
No such user in database|/new-user-confirm/|testNewUserConfirmNoSuchUser
Kyc verification success|/api/v1/new-kyc-submit/|testNewKycSubmitSuccess
Kyc verification fail due to mismatched images|/api/v1/new-kyc-submit/|testNewKycSubmitMismatch
No uid in request|/api/v1/new-kyc-submit/|testNewKycSubmitNoUid
No such user in database|/api/v1/new-kyc-submit/|testNewKycSubmitNoSuchUser
No selfie in request|/api/v1/new-kyc-submit/|testNewKycSubmitNoSelfie
No passport in request|/api/v1/new-kyc-submit/|testNewKycSubmitNoPassport
New user registration success|/api/v1/new-user-submit/|testNewUserSubmitSuccess
No uid in user registration request|/api/v1/new-user-submit/|testNewUserSubmitNoUid
No email in user registration request|/api/v1/new-user-submit/|testNewUserSubmitNoEmail
Invalid email in user registration|/api/v1/new-user-submit/|testNewUserSubmitInvalidEmail

## Deployment

Repo can be deployed as-is to heroku.
Current demo instance running at https://myface-server.herokuapp.com/.

## Authors

* **Charles Wong** - [Profile](https://github.com/charleswongzx)

See also the list of [contributors](https://github.com/orgs/myFace-KYC/people) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* http://flask.pocoo.org/docs/0.12/testing/
* https://pypi.python.org/pypi/python-firebase/1.2
* https://azure.microsoft.com/en-us/services/cognitive-services/face/
