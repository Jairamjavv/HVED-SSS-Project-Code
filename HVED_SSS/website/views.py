# contains all the routes from and to - user navigation

# BLueprint contains a bunch of routes inside it
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
# from .models import Note
from . import db
import json
import os
from HVED import HVED
# from ..HVED import HVED

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    # file name with extension
    for r,d,f in os.walk(os.path.join(os.getcwd(),'frames')):
        j = len(d)
        break    
    # l = len(os.listdir(os.path.join(os.getcwd(), "encrypted{}".format(j))))
    # print('====',os.path.splitext(file_name)[0])
    # if request.method == 'POST':
    #     note = request.form.get('note')
        
    #     if len(note) < 1:
    #         flash('Note is too short', category='warning')
    #     else:
    #         new_note = Note(data=note, user_id=current_user.id)
    #         db.session.add(new_note)
    #         db.session.commit()
    #         flash('Note added!', category='success')
    
    return render_template("home.html", user=current_user, totalFiles = range(int(j)))

# @views.route('/deleteNote', methods=['POST'])
# def deleteNote():
#     note = json.loads(request.data)
#     noteId = note['noteId']
#     note = Note.query.get(noteId)
#     if note:
#         if note.user_id == current_user.id:
#             db.session.delete(note)
#             db.session.commit()
    
#     return jsonify({})

@views.route('/decryptFile', methods=['GET', 'POST'])
@login_required
def decryptFile():
    # trigger decryption video
    hved = HVED()
    hved.hved_()
    flag = 1
    return render_template("display.html", user=current_user, flag=flag)