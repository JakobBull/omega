import datetime
import json
import os
from datetime import timedelta

from flask import Flask
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import send_from_directory
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import unset_jwt_cookies
from flask_mail import Mail
from flask_mail import Message
from itsdangerous import BadSignature
from itsdangerous import SignatureExpired
from itsdangerous.url_safe import URLSafeTimedSerializer

#from backend.question import AlgebraQuestion
#from backend.update_score import glickoupdate_score
#from backend.user import User
#from database import DBTools
#from settings import FlaskSettings
#from omega.settings import MailSettings


def create_app(mongo_client=None):
    app = Flask(__name__)

    app.config["SECRET_KEY"] = 'jakob' #FlaskSettings.flask_secret
    app.config["JWT_SECRET_KEY"] = 'jakob' #FlaskSettings.jwt_secret
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=2)
    app.config["JWT_CSRF_IN_COOKIES"] = True
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]

    '''# Mail config
    app.config["MAIL_SERVER"] = MailSettings.server
    app.config["MAIL_PORT"] = MailSettings.port
    app.config["MAIL_USE_SSL"] = MailSettings.use_ssl
    app.config["MAIL_USE_TLS"] = MailSettings.use_tls
    app.config["MAIL_USERNAME"] = MailSettings.username
    app.config["MAIL_PASSWORD"] = MailSettings.password

    mail = Mail(app)'''

    #score_updater = glickoupdate_score
    #database = DBTools(mongo_client)

    '''reset_password_serializer = URLSafeTimedSerializer(
        FlaskSettings.url_serializer_secret
    )
    url_root = FlaskSettings.url_root'''

    jwt = JWTManager(app)  # pylint: disable = unused-variable

    @jwt.unauthorized_loader
    def redirect_unauthorized(expired_token):
        # pylint: disable = unused-argument
        return redirect("/")

    '''@jwt.expired_token_loader
    def redirect_expired(jwt_header, jwt_payload):
        # pylint: disable = unused-argument
        return redirect("/")'''

    # Path for our main Svelte page
    @app.route("/app")
    @jwt_required()
    def base():
        return render_template('index.html')

    @app.route("/api/login", methods=["POST"])
    def login():
        given_data = json.loads(request.data)
        if given_data:
            pass
        login_success = database.check_password(
            given_data["email"], given_data["password"]
        )
        if not login_success:
            print(f'Failed sign in attempt for user {given_data["email"]}')
            return jsonify({"msg": "bad email or password"}), 401
        user = User(database, given_data["email"])
        # TODO(ti250): this identity shouldn't be tied to email but rather to ID or something
        # more fundamental.. baby steps
        access_token = create_access_token(identity=user.email_address)
        response = redirect("/app")
        set_access_cookies(response, access_token)
        return response




    @app.route("/api/forgotPasswordRequest", methods=["POST"])
    def reset_password_request():
        given_data = json.loads(request.data)

        user = database.get_user(given_data["email"])
        if user is None:
            # We return this on purpose so that a bad actor wouldn't be able to
            # check whether a user has an account on the service
            return jsonify({"msg": "Reset password request successful"})

        timestamp = str(datetime.datetime.now())
        user["resetPasswordRequestedDate"] = timestamp
        database.players.update_one(
            {"_id": user["_id"]}, {"$set": {"resetPasswordRequestedDate": timestamp}}
        )

        email = user["email"]
        dumped_string = reset_password_serializer.dumps([email, timestamp])
        link = f"{url_root}/resetPassword?user_token={dumped_string}&user_email={email}#/resetPassword"

        # TODO(ti250): Let's configure these outside of code at some point...
        message = Message(
            "Reset your aios password", sender=MailSettings.username, recipients=[email]
        )
        message.body = f"Here({link}) is your password reset link."
        message.html = f"""<a href="{link}">Here</a> is your password reset link."""
        mail.send(message)

        return jsonify({"msg": "Reset password request successful"})

    @app.route("/api/resetPassword", methods=["POST"])
    def reset_password():
        given_data = json.loads(request.data)
        user_token = given_data["user_token"]

        try:
            user = validate_and_retrieve_user_for_reset(user_token)
        except (ValueError, KeyError):
            return jsonify({"msg": "reset password failed"}), 403

        database.players.update_one(
            {"_id": user["_id"]},
            {
                "$set": {
                    "password": database.hash_password(given_data["password"]),
                    "resetPasswordRequestedDate": "invalidDate",
                }
            },
        )

        return jsonify({"msg": "reset password succeeded"}), 200

    @app.route("/api/logout", methods=["POST"])
    def logout():
        response = redirect("/")
        unset_jwt_cookies(response)
        return response

    @app.route("/api/updatePassword", methods=["POST"])
    @jwt_required()
    def update_password():
        given_data = json.loads(request.data)
        email = get_jwt_identity()

        user = database.get_user(email)
        if user is None:
            print(
                f"Failed password update for {email} due to bad email. This should not be happening"
            )
            return jsonify({"msg": "bad user or password"}), 401

        current_password = given_data["current_password"]

        current_password_correct = database.check_password(email, current_password)
        if not current_password_correct:
            print(f"Failed password update for {email} due to bad password")
            return jsonify({"msg": "bad user or password"}), 401

        new_password = given_data["new_password"]

        database.players.update_one(
            {"_id": user["_id"]},
            {
                "$set": {
                    "password": database.hash_password(new_password),
                    "resetPasswordRequestedDate": "invalidDate",
                }
            },
        )

        return jsonify({"msg": "Update password succeeded"}), 200

    @app.route("/api/setSettings", methods=["POST"])
    @jwt_required()
    def set_settings():
        # Settings such as reduce motion/dark mode go here
        given_data = json.loads(request.data)
        email = get_jwt_identity()

        updated_settings_query = {}

        for setting_key, setting_value in given_data["updated_settings"].items():
            updated_settings_query[f"settings.{setting_key}"] = setting_value

        user = database.get_user(email)

        database.players.update_one(
            {"_id": user["_id"]},
            {"$set": updated_settings_query},
        )

        return jsonify({"msg": "Update settings succeeded"}), 200

    @app.route("/api/getQuestion")
    @jwt_required()
    def get_question():
        user_name = get_jwt_identity()
        mode = request.args.get("mode")

        user = User(database, user_name)
        if mode is not None:
            if mode == "all":
                mode = database.pick_random_mode()
            question_data = database.get_random_question(
                mode, user.float_score_for_mode(mode), 10
            )
        else:
            raise ValueError("Mode should not be None!")

        question_id = question_data["_id"]
        # It would in principle be nice to remove this but we can't get the string_repr
        # without the AlgebraQuestion object...
        question = AlgebraQuestion(
            question_data["flag"],
            question_data["score"],
            question_data["dev"],
            question_data["vol"],
            question_data["solution"],
            *question_data["question"],
        )

        return {
            "question": {
                "score": question.score,
                "string": question.string_repr,
                "questionId": str(question_id),
                "mode": question.mode,
            }
        }

    @app.route("/api/user")
    @jwt_required()
    def get_username():
        email = get_jwt_identity()

        if email is None:
            raise ValueError("No username input!")

        user = User(database, email)

        return {
            "userPreferredName": str(user.preferred_name),
            "email": str(user.email_address),
        }

    @app.route("/api/userScoresForMode")
    @jwt_required()
    def get_user_scores():
        email = get_jwt_identity()
        given_mode = request.args.get("mode", type=str)
        modes = [given_mode] if given_mode != "all" else ["add", "sub", "mul", "div"]

        if email is None:
            raise ValueError("No username input!")
        elif modes is None:
            raise ValueError("Mode should not be None!")

        user = User(database, email)
        scores = {mode: str(int(user.float_score_for_mode(mode))) for mode in modes}

        return {
            "scores": scores,
            "userPreferredName": str(user.preferred_name),
            "email": str(user.email_address),
        }

    @app.route("/api/settings", methods=["GET"])
    @jwt_required()
    def get_settings():
        email = get_jwt_identity()

        user = User(database, email)

        return user.settings

    @app.route("/api/userSolution", methods=["POST"])
    @jwt_required()
    def update_score():
        email_address = get_jwt_identity()
        given_data = json.loads(request.data)
        question_id = given_data["question_id"]
        # Time taken in milliseconds
        time_taken = int(given_data["time_taken"])

        if email_address is None:
            raise ValueError("No user name input!")

        user = User(database, email_address)

        question_data = database.get_question_with_id(question_id)

        question = AlgebraQuestion(
            question_data["flag"],
            question_data["score"],
            question_data["dev"],
            question_data["vol"],
            question_data["solution"],
            *question_data["question"],
        )

        response_dict = {}
        user_input = given_data["answer"]

        was_correct = question.is_correct(user_input)

        response_dict["wasCorrect"] = was_correct

        given_mode = given_data["mode"]
        score_updater(
            database,
            user.id,
            question_id,
            user,
            question,
            was_correct,
            time_taken,
        )

        modes = [given_mode] if given_mode != "all" else ["add", "sub", "mul", "div"]
        scores = {mode: str(int(user.float_score_for_mode(mode))) for mode in modes}
        response_dict["scores"] = scores

        return response_dict

    @app.route("/api/signup", methods=["POST"])
    def signup():
        user_data = json.loads(request.data)
        try:
            database.add_player(
                user_data["pref_name"],
                user_data["email"],
                user_data["password"],
            )
        except ValueError:
            return jsonify({"msg": "signup failed"}), 409
        access_token = create_access_token(identity=user_data["email"])
        response = redirect("/app")
        set_access_cookies(response, access_token)
        return response

    def is_valid_password_reset_token(user_token, max_age=3600):
        try:
            email, date = reset_password_serializer.loads(user_token, max_age=max_age)
        except (BadSignature, SignatureExpired):
            return False
        user_dict = database.get_user(email)
        if user_dict is None or user_dict["resetPasswordRequestedDate"] != date:
            return False
        return True

    def validate_and_retrieve_user_for_reset(user_token, max_age=3600):
        if not is_valid_password_reset_token(user_token, max_age=max_age):
            raise ValueError("Invalid password reset token")

        email, _ = reset_password_serializer.loads(user_token, max_age=max_age)
        user = database.get_user(email)
        if user is None:
            return KeyError("User does not exist")

        return user

    return app


if __name__ == "__main__":
    app_instance = create_app()
    app_instance.run(debug=bool(os.environ.get("EAGLE_DEBUG", False)), port=80, host="0.0.0.0")
    #app_instance.run(debug=FlaskSettings.debug, port=80, host="0.0.0.0")

