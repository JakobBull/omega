import os

print('skipping')

'''
_debug = bool(os.environ.get("EAGLE_DEBUG", False))


class FlaskSettings:
    flask_secret = os.environ["EAGLE_FLASK_SECRET_KEY"]
    jwt_secret = os.environ["EAGLE_JWT_SECRET_KEY"]
    url_serializer_secret = os.environ["EAGLE_URL_SERIALIZER_SECRET_KEY"]
    debug = _debug
    url_root = (
        os.environ.get("EAGLE_ROOT_URL", "localhost")
        if _debug
        else os.environ["EAGLE_ROOT_URL"]
    )


class MongoDBSettings:
    url = (
        os.environ.get("MONGODB_CONN_STRING", "localhost:27017")
        if _debug
        else os.environ["MONGODB_CONN_STRING"]
    )


class MailSettings:
    server = "smtp.gmail.com"
    port = 587
    use_tls = True
    use_ssl = False
    username = os.environ.get("EAGLE_SUPPORT_EMAIL", "aios.email.validation@gmail.com")
    password = os.environ["EAGLE_VALIDATION_EMAIL_PASSWORD"]
'''