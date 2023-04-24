"""Define class that creates database objects and all methods used to use database.

Use includes adding history to questions, players and matches.

Classes:
------
DBTools - Creating a database object.
"""

import random
from typing import List

import bcrypt
import pandas as pd
import pymongo
from bson.objectid import ObjectId

import settings


class DBTools:
    """Create a database object.

    Methods are used for all database operations.

    Parameters:
    ------
    None

    Public Methods:
    ------
    add_match -
    add_player -
    add_question -
    update - Updating player and question metrics after a match.
    get_user - Returning a player from the database by name.
    get_closest_question - Returning closest question to some score.
    clear_matches - Deleting all matches from the database.

    """

    def __init__(self, client=None):
        if client is None:
            self.client = pymongo.MongoClient(settings.MongoDBSettings.url)
        else:
            self.client = client
        self.db = self.client["omega"]
        self.users = self.db["users"]

    def check_collection(self, collection_name):
        return collection_name in self.db.list_collection_names()


    '''def add_users(
        self,
        username: str,
        password: str,
        account_id: str,
    ):
        """Add a player with a new random unique ID.

        Parameters:
        str pref_name: Player's preferred name
        str email: Player's email (should be unique identifier)
        str password: Player's password
        int score: Player's score
        int dev: Player score deviation
        float vol: Volatility for the player's score
        [ObjectID] match_ids: List of matches that the user has been in
        ------

        Returns:
        Player ObjectID.
        """
        if self.players.find_one({"username": username}):
            raise ValueError("There already exists a user with this username!")

        user = {
            "username": username,
            "password": self.hash_password(password),
            "account_id": account_id,
        }
        return self.users.insert_one(user).inserted_id

    def hash_password(self, password):
        return bcrypt.hashpw(bytes(password, "utf-8"), bcrypt.gensalt())

    def check_password(self, email, password):
        player = self.players.find_one({"email": email}, projection={"password": True})
        if player is None:
            return False
        return bcrypt.checkpw(bytes(password, "utf-8"), player["password"])

    def add_question(
        self, mode, question, solution, score=1500, dev=350, vol=0.06, match_ids=None
    ):
        """Add a question with a new random unique ID.

        Parameters:
        question: Question content.
        solution: Question solution.
        ------

        Returns:
        Question ObjectID.
        """
        if match_ids is None:
            match_ids = []
        question = {
            "question": question,
            "solution": solution,
            "flag": mode,
            "score": score,
            "dev": dev,
            "vol": vol,
            "match_ids": match_ids,
        }
        z = self.questions.insert_one(question)
        return z.inserted_id

    def update(
        self,
        mode: str,
        p_id: ObjectId,
        p_glicko_score: GlickoScore,
        p_update: float,
        q_id: ObjectId,
        q_glicko_score: GlickoScore,
        q_update: float,
        win: bool,
        time: str,
        date: str,
    ):
        """Update rating information in the database.

        Add match with new unique random ID to the matches collection
        and update ratings of questions and players.
        """
        if not isinstance(p_id, ObjectId):
            p_id = ObjectId(p_id)
        if not isinstance(q_id, ObjectId):
            q_id = ObjectId(q_id)

        match_id = self.add_match(
            mode,
            p_id,
            p_glicko_score,
            p_update,
            q_id,
            q_glicko_score,
            q_update,
            win,
            time,
            date,
        )
        player_matches = self.players.find({"_id": p_id})[0].get("match_ids")
        if player_matches is None:
            player_matches = []
        player_matches.append([match_id, time, date])
        self.players.update_one(
            {"_id": p_id},
            {
                "$set": {
                    "match_ids": player_matches,
                    f"scores.{mode}": p_glicko_score.as_dict(),
                }
            },
        )
        question_matches = self.questions.find({"_id": q_id})[0].get("match_ids")
        if question_matches is None:
            question_matches = []
        question_matches.append([match_id, time, date])
        self.questions.update_one(
            {"_id": q_id},
            {
                "$set": {
                    "match_ids": question_matches,
                    "score": q_glicko_score.score,
                    "dev": q_glicko_score.deviation,
                    "vol": q_glicko_score.volatility,
                }
            },
        )

    def get_user(self, email):
        """Return single user by email.

        Assumes that emails are unique, will later be changed to ID.

        Parameters:
        email: Player email.
        ------

        Returns:
        user: Single user object.
        """
        potential_users = list(self.players.find({"email": email}))
        if len(potential_users) == 1:
            user = potential_users[0]
        elif len(potential_users) < 1:
            user = None
        elif len(potential_users) > 1:
            raise ValueError("Too many users with email address")
        return user

    def get_user_history(self, email, limit=1000):
        """Return all matches of user by id."""
        user_id = self.get_user(email).get("_id")
        potential_games = (
            self.matches.find(
                {"p_id": user_id},
                {
                    "p_glicko_score": 1,
                    "p_update": 1,
                    "win": 1,
                    "solvetime": 1,
                    "date": 1,
                },
            )
            .sort([("date", -1)])
            .limit(limit)
            .sort([("date", 1)])
        )
        potential_games_list = list(potential_games)
        potential_games_df = pd.DataFrame(potential_games_list)
        return potential_games_df

    def get_all_matches(self, mode):
        potential_questions = (
            self.questions.distinct(
                "_id",
                {"flag": mode}
            )
        )

        games = (
            self.matches.find(
                {"q_id": {"$in": potential_questions}},
                {
                    "p_id": 1,
                    "q_id": 1,
                    "win": 1,
                    "_id": 0,
                },

            )
        )
        return pd.DataFrame(list(games))

    def get_closest_question(self, mode, p_score):
        """Return question closest to target score.

        Query database for question closest to some input score. Creates ordered list in descending closeness, so can return multiple.

        Parameters:
        p_score: Target score we are sampling near.
        ------

        Returns:
        question: Single closest question to target score.
        """
        query_list = [
            {"$addFields": {"diff": {"$abs": {"$subtract": [p_score, "$score"]}}}},
            {"$sort": {"diff": 1}},
            {"$limit": 1},
        ]
        questions = self.questions.aggregate([{"$match": {"flag": mode}}, *query_list])
        return list(questions)[0]

    def get_random_question(self, mode, p_score, num_closest):
        """
        Return a random question from the `num_closest` questions with closest scores
        to `p_score`.

        Parameters:
        p_score: Target score we are sampling near.
        num_closest: Number of questions to sample around the p_score
        ------

        Returns:
        question: Single closest question to target score.
        """
        query_list = [
            {"$addFields": {"diff": {"$abs": {"$subtract": [p_score, "$score"]}}}},
            {"$sort": {"diff": 1}},
            {"$limit": num_closest},
        ]
        questions = self.questions.aggregate([{"$match": {"flag": mode}}, *query_list])
        return random.choice(list(questions))

    def pick_random_mode(self):
        return random.choice(["sub", "add", "mul", "div"])

    def clear_matches(self):
        """Delete all matches from database."""
        self.matches.delete_many({})
        self.players.update_one({}, {"$set": {"match_ids": []}})
        self.questions.update_one({}, {"$set": {"match_ids": []}})

    def clear_questions(self):
        self.questions.delete_many({})

    def clear_players(self):
        self.players.delete_many({})

    def get_question_with_id(self, question_id):
        if not isinstance(question_id, ObjectId):
            question_id = ObjectId(question_id)
        question_match = self.questions.find_one({"_id": question_id})
        return question_match
'''