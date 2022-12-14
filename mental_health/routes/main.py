import json
from flask import Blueprint, request, render_template, jsonify
from ..database.db import db, datetime
from ..models.user import User
from ..models.entry import Entry, EntryEncoder
from ..scripts.statistics import getTargetQuery, getTotalEntries, getAvarage, getUserWeek, getMostRecentFeeling
from werkzeug import exceptions
from flask_jwt_extended import create_access_token, unset_jwt_cookies
from flask_jwt_extended import get_jwt_identity, get_jwt
from flask_jwt_extended import jwt_required

main_routes = Blueprint("main", __name__)

@main_routes.route("/new_entry", methods=["POST"])
@jwt_required()
def new_entry():

    
    try:
        user = get_jwt_identity()
        data = request.get_json()
        date = datetime.strftime(datetime.today(), "%d-%m-%Y")
        day = datetime.strftime(datetime.today(), "%A")
        week = datetime.strftime(datetime.today(), "%W")
        time = datetime.strftime(datetime.today(), "%H-%M")
        mood = data["mood"]
        energy = data["energy"]
        depression = data["depression"]
        irritability = data["irritability"]
        motivation = data["motivation"]
        stress = data["stress"]
        appetite = data["appetite"]
        concentration = data["concentration"]
        diet = data["diet"]
        enter = data["enter"]
        social = data["social"]

        new_entry = Entry(user=user, date_posted=date,
        day=day, week=week, time=time, mood=mood, energy=energy, depression=depression, irritability=irritability, motivation=motivation,
        stress=stress, appetite=appetite, concentration=concentration, diet=diet,
        enter=enter, social=social)

        db.session.add(new_entry)
        db.session.commit()

        return "Created new entry", 200
    except:
        print("error occured")


@main_routes.route("/username", methods=["GET"])
@jwt_required()
def get_user():
    try:

        user = get_jwt_identity()
        jsonified_d = f'{{"username" : {user}}}'
        return jsonified_d , 200
        
    except:
        print("Was not possible to retreive all entries")

@main_routes.route("/entries", methods=["GET"])
@jwt_required()
def get_all_entries():
    try:

        all_entries = getTotalEntries()
        jsonified_d = json.dumps(all_entries, cls=EntryEncoder, indent=4)
        return jsonified_d , 200
        
    except:
        print("Was not possible to retreive all entries")

@main_routes.route("/entry/<target>/<value>", methods=["GET"])   # for now i retrieving specific target
def get_entry(target, value):
    try:
        entries = getTargetQuery(target,value)
        jsonified_d = json.dumps(entries, cls=EntryEncoder, indent=4)
        return jsonified_d
    except:
        print("error occured when retriving specific date")

@main_routes.route("/stats/<target>/<value>", methods=["GET"])
@jwt_required()
def get_statistics(target, value):

    try:
        totalAvarage = getAvarage(target, value)
        jsonified_d = f'{{"{target}" : {value}, "total" : {totalAvarage}}}'
        return jsonified_d
    except:
        print("error getting requesting statistics")


@main_routes.route("/recent/<target>", methods=["GET"])
@jwt_required()
def get_recent_entry(target):

    try:
        recent_entry = getMostRecentFeeling(target)   
        jsonified_d = json.dumps(recent_entry, cls=EntryEncoder, indent=4)
        return jsonified_d
    except:
        print("error getting requesting statistics")



@main_routes.errorhandler(exceptions.BadRequest)
def handle_400(err):
    return {'message': f'Oops! {err}'}, 400


@main_routes.errorhandler(exceptions.Unauthorized)
def handle_401(err):
    return {'message': f'Not authorized! {err}'}, 401


@main_routes.errorhandler(exceptions.NotFound)
def handle_404(err):
    return {'message': f'Oops! {err}'}, 404


@main_routes.errorhandler(exceptions.InternalServerError)
def handle_500(err):
    return {'message': f"It's not you, it's us {err}"}, 500








      


    # day=day, week=week, time=time,
