"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
import os,datetime, random, re
from app import app,db,Allowed_uploads
from flask import render_template, request, redirect, url_for, flash, session, abort, send_from_directory,make_response,jsonify
from werkzeug.utils import secure_filename
from form import NewProfileForm
from models import UserProfile

from sqlalchemy import exc

import datetime
import os

###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')
    
    
@app.route('/profile', methods=["GET", "POST"])
def profile():
    ProfileForm = NewProfileForm()
    
    if request.method == 'POST':
        if ProfileForm.validate_on_submit()==True:
            
                firstname = ProfileForm.firstname.data
                lastname = ProfileForm.lastname.data
                gender = ProfileForm.gender.data
                email = ProfileForm.email.data
                location = ProfileForm.location.data
                bio = ProfileForm.bio.data
               
                user = UserProfile(firstname=firstname, lastname=lastname, gender=gender, email=email, location=location, bio=bio)
                db.session.add(user)
                db.session.commit()
                flash('Successfullly added.', 'success')
                return redirect(url_for('profiles'))
    return render_template("create_profile.html", user=ProfileForm)
    
    
@app.route("/profiles/")
def profiles():
    ulist = UserProfile.query.all()
    users =  [{"First Name": user.first_name, "Last Name": user.last_name, "userid": user.userid} for user in ulist]
    
    if request.method == 'GET':
        if ulist is not None:
            return render_template("profiles.html", user=ulist)
        else:
            flash('No Users Found', 'danger')
            return redirect(url_for("home"))
    
    elif request.method == 'POST':
        if ulist is not None:
            response = make_response(jsonify({"users": users}))                                           
            response.headers['Content-Type'] = 'application/json'            
            return response
        else:
            flash('No Users Found', 'danger')
    return redirect(url_for("home")) 

def generateUserId(firstname, lastname):
    temp = re.sub('[.: -]', '', str(datetime.datetime.now()))
    temp = list(temp)
    temp.extend(list(map(ord,firstname)))
    temp.extend(list(map(ord,lastname)))
    random.shuffle(temp)
    temp = list(map(str,temp))
    return int("".join(temp[:7]))%10000000 

def format_date_joined(yy,mm,dd):
    return datetime.date(yy,mm,dd).strftime("%B, %d,%Y")
 
    


###
# The functions below should be applicable to all Flask apps.
###

# Flash errors from the form if validation fails
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
