
import email
from enum import unique
from operator import index
from io import BytesIO
from pickle import dump
from flask import Flask, Request, render_template, request, redirect, flash, send_file
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import PrimaryKeyConstraint, Table, select, true
from flask_login import UserMixin
from flask_login import login_required, logout_user, login_user, login_manager, LoginManager, current_user
import requests
import random
import pandas as pd
import ast
from sqlalchemy import create_engine
from model import *
from difflib import get_close_matches

# my database connection
local_server = True
app = Flask(__name__)
app.secret_key = "prem"


# unique user access
#login_manager = LoginManager(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql:///username:password@localhost/databasename"
#app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@127.0.0.2:3307/newmed"

app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://cxoeaohdkmjclz:b36e9e14af552226e938d247e02eab4ff6121cb53009b0955a2d3681f76ac672@ec2-52-204-195-41.compute-1.amazonaws.com:5432/df8qaermkm5lts"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


engine = create_engine('mysql://root:@127.0.0.2:3307/newmed')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

##################################################################################################
                                #"""Data model for user accounts."""#
##################################################################################################
class Rating_user(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer)
    movie_id = db.column(db.Integer)
    rating = db.Column(db.Integer)
    mname = db.Column(db.String(100))


class History(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Integer)
    mname = db.Column(db.String(100))
    duration = db.Column(db.String(100))
    genre = db.Column(db.String(100))
    action = db.Column(db.String(100))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(25))
    umail = db.Column(db.String(25), unique=True)
    uage = db.Column(db.String(14))

    upass = db.Column(db.String(30))
    cupass = db.Column(db.String(30))

# id


class Userdata(db.Model, UserMixin):     # store favourite  movie detail 
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), primary_key=True)
    movie = db.Column(db.String(50))
    poster = db.Column(db.String(1000))
    genre = db.Column(db.String(100))
    duration = db.Column(db.String(100))


##################################################################################################
                                #"""function for fetching details of movie """
##################################################################################################


ds = pd.read_csv("dataset/processed.csv")


def all_detail(movie_id):

    lis = []
    # poster  0
    full_path = list(ds[ds['id'] == movie_id]['posters'])[0]
    lis.append(full_path)

    # adding genre 1
    st = (ds[ds['id'] == movie_id]['genres'].values)[0]
    st = ast.literal_eval(st)
    lis.append(st)

    # addding rating 2
    rating = (ds[ds['id'] == movie_id]['vote_average'].values)[0]
    # rating = data['vote_average']
    lis.append(rating)

    # runtime 3
    runtime = (ds[ds['id'] == movie_id]['runtime'].values)[0]
    # run = data['runtime']
    lis.append(runtime)

    # overview 4
    overview = (ds[ds['id'] == movie_id]['overview'].values)[0]
    # over = data['overview']
    lis.append(overview)

    # name 5
    name = (ds[ds['id'] == movie_id]['title'].values)[0]
    # name = data['original_title']
    lis.append(name)

    # rating 6
    vote = (ds[ds['id'] == movie_id]['vote_average'].values)[0]
    # vote = data['vote_average']
    lis.append(vote)

    return lis


# 
data = ds
title_list = list(data['title'])
def get_movie_id(movie):  # function for fetching movie id by movie name, in  database all titles sre in lower case so i am  fetching after lower() of title
    movie = movie.lower()

    data['title'] = data['title'].str.lower()
    first = data[["id", "title"]]
    second = first[data['title'] == movie]
    rt = list(second['id'])

    return rt[0]


def movie_detail(moviel): # this accept list of movie and return deatil of each movie in the form of 2D list

    doc = []

    for m in moviel:

        id = get_movie_id(m)
        l1 = all_detail(id)
        doc.append(l1)
    return doc


def cast_of_movie(movie): #accept moovie name and return list of 4 main cast of movie in the form of 2D list
    cast_details = []
    movie_id = get_movie_id(movie)
    cast_url = "https://api.themoviedb.org/3/movie/{}/credits?api_key=cd109cb98c90d3020a252e6f524b8d63&language=en-US".format(
        movie_id)
    cast_data = requests.get(cast_url)
    cast_data = cast_data.json()
    cast_data
    for i in range(len(cast_data['cast'])):
        single_cast = []
        single_cast.append(cast_data['cast'][i]["name"])
        single_cast.append(cast_data['cast'][i]["character"])
        single_cast.append("https://image.tmdb.org/t/p/w500" +
                           str(cast_data['cast'][i]["profile_path"]))
        cast_details.append(single_cast)

    return cast_details[:4]


genre_data = ds

# Function that return moives detail by its genre
def thriller_movies():
    thriller_genre = genre_data[genre_data['single_genre'] == 'Thriller']
    thriller_data = thriller_genre.iloc[0:24, :]
    thriller_data = thriller_data['title'].to_list()
    thriller_final = movie_detail(thriller_data)
    return thriller_final


def horror_movies():
    horror_genre = genre_data[genre_data['single_genre'] == 'Horror']
    horror_data = horror_genre.iloc[0:24, :]
    horror_data = horror_data['title'].to_list()
    horror_final = movie_detail(horror_data)
    return horror_final


def crime_movies():
    crime_genre = genre_data[genre_data['single_genre'] == 'Crime']
    crime_data = crime_genre.iloc[0:24, :]
    crime_data = crime_data['title'].to_list()
    crime_final = movie_detail(crime_data)
    return crime_final


def action_movies():
    action_genre = genre_data[genre_data['single_genre'] == 'Action']
    action_data = action_genre.iloc[0:24, :]
    action_data = action_data['title'].to_list()
    action_final = movie_detail(action_data)
    return action_final


def adventure_movies():
    adventure_genre = genre_data[genre_data['single_genre'] == 'Action']
    adventure_data = adventure_genre.iloc[0:24, :]
    adventure_data = adventure_data['title'].to_list()
    adventure_final = movie_detail(adventure_data)
    return adventure_final

#############################################################################################################################
                                #"""fetching detail from database of user rating for hybrid recommendation"""
#############################################################################################################################

query = 'select * from rating_user'
my_df = pd.read_sql_query(query, engine)
my_df = my_df[['id_user','movie_id','rating','id']]

my_df.rename(columns = {'id_user':'userId', 'movie_id':'movieId','rating':'rating', 'id':'timestamp'}, inplace = True)
my_df.to_csv('dataset/file_names3.csv',index=False)



#############################################################################################################################
                                                          #"""Routing before login """
#############################################################################################################################



@app.route("/")
def home():
    try:
        vote = pd.read_csv('dataset/data_voting.csv')  # named dataframe as vote because it is sorted by vote_average
        vote['title'] = vote['title'].str.lower()
        postsdata = []
        data_by_vote = [] 
        postsdata.append(data_by_vote) # appended  empty list for future to insert list if required

        # by popularity
        d_pop = vote.sort_values(by=['popularity'], ascending=False)
        nd_pop = d_pop.iloc[:10, :]
        nd_pop = nd_pop['title'].to_list()
        data_by_pop = movie_detail(nd_pop)
        postsdata.append(data_by_pop)

        # Most Watched / most revenued
        evergreen = []
        evergreen_data = vote.sort_values(by=['revenue'], ascending=False)
        evergreen_datan = evergreen_data.iloc[:10, :]
        evergreen_datan = evergreen_datan['title'].to_list()
        data_evergreen = movie_detail(evergreen_datan)
        evergreen.append(data_evergreen)

        # TOP Budget

        top_budget = []
        top_budget_data = vote.sort_values(by=['budget'], ascending=False)
        top_budget_datan = top_budget_data.iloc[:10, :]
        top_budget_datan = top_budget_datan['title'].to_list()
        data_top_budget = movie_detail(top_budget_datan)
        top_budget.append(data_top_budget)

        return render_template("index2.html", postsdata=postsdata, evergreen=evergreen, top=top_budget, movie=title_list)
    except:

        return render_template('not_found.html')




@app.route("/search", methods=['POST', 'GET'])
def search():
    if request.method == "POST":
        movie = request.form.get("movie")
        movie = movie.lower()
        try:

            movie_list = movie_recommender(movie)  # using normal recommender for anonymous user for movie recommendation 
            movie_list = np.insert(movie_list, 0, movie)
            postsdata = movie_detail(movie_list)
            cast = cast_of_movie(movie)
            return render_template("index.html", postsdata=postsdata, cast=cast, movie=title_list)

        except:

            try:

                m = get_close_matches(movie, title_list) #getting close matches of user input if user enter any movie which is not suggested by datalist
                m = [x.lower() for x in m]
                postsdata = movie_detail(m)
                return render_template("index_difflib.html", postsdata=postsdata, movie=title_list)

            except:

                return render_template('not_found.html')

    return redirect(url_for('home'))

@app.route("/signup", methods=['POST', 'GET'])
def signup():
    try : 
        if request.method == "POST":
            funame = request.form.get('username')
            fumail = request.form.get('usermail')
            fupass = request.form.get('userpass')
            fcupass = request.form.get('usercpass')
            fage = request.form.get('userage')
            user = User.query.filter_by(umail=fumail).first()

            if user:
                flash("E-mail  You have entered Already Exist", "info")
                return redirect(url_for('home'))
            new_user = db.engine.execute(
                f"INSERT INTO `user` (`id`, `uname`, `umail`, `upass`, `cupass`, `uage`)  VALUES (NULL, '{funame}','{fumail}','{fupass}','{fcupass}','{fage}');")

            flash("Registration Successful enter Credential for Account Access", "success")
            return redirect(url_for('home'))
        return redirect(url_for('home'))
    except:
        return render_template('not_found.html')


@app.route("/login", methods=['POST', 'GET'])
def login():
    try:
        if request.method == "POST":

            email = request.form.get('usermail')
            upass = request.form.get('userpass')

            user = User.query.filter_by(umail=email).first_or_404(
                description='There is no data with {}'.format(email))

            if user and user.upass == upass:
                login_user(user)
                flash("Log In Successful", "success")

                return redirect(url_for('dashboard'))

            else:
                flash("Invalide Credential", "success")
                return redirect(url_for('home'))

        return redirect(url_for('home'))
    except:
        return render_template('not_found.html')


#############################################################################################################################
                                                          #"""Routing After login """
#############################################################################################################################




@app.route("/searchdash", methods=['POST', 'GET'])
@login_required
def searchdash():
    if request.method == "POST":
        movie = request.form.get("movie")
        movie = movie.lower()

        try:

            fumail = current_user.umail     # fetching current logged in user email 

            movie_n = movie.replace("'", "''")  # replacing removing apastrophy becase mysql syntax does not support

            duration = '--'  # taking anonymous value as not much important we can fetch from moviename
            genre = '--'
            action = 'search'

            new_user = db.engine.execute(
                f"INSERT INTO `history` (`id`, `email`, `mname`, `duration`, `genre`, `action`)  VALUES (NULL, '{fumail}','{movie_n}','{duration}','{genre}','{action}');")


            #####################################    using hybrid recommender as user is logged in ################################

            movie_list = hybrid(current_user.id, movie.title())  # passing userid and movie name in title case 

            movie_list = [x.lower() for x in movie_list]

            movie_list = np.insert(movie_list, 0, movie)  # Inserting searched movie in movielist 
            recommended = movie_detail(movie_list)
            postsdata = []

            other = []

            postsdata.append(other)
            postsdata.append(recommended)
            return render_template("search_dash.html", postsdata=postsdata, movie=title_list)

        except:
            try:

                m = get_close_matches(movie, title_list)  # close matches if user input wrong moviename
                m = [x.lower() for x in m]
                postsdata = movie_detail(m)
                return render_template("difflib_dash.html", postsdata=postsdata, movie=title_list)

            except:

                return render_template('not_found.html')

        return redirect(url_for('dashboard'))


@app.route("/favourite", methods=['POST', 'GET'])
@login_required
def fovourite():
    if request.method == "POST":
        try:
            movie = request.form.get("playmovie")
            poster = request.form.get("poster")
            genre = request.form.get("genre")
            duration = request.form.get("duration")
            movie = movie.lower()
            fumail = current_user.umail

            userdata = Userdata.query.filter_by(email=fumail).all()

            cl = []

            for c in userdata:
                cl.append(c.movie)

            if cl.__contains__(movie):  #CHECKING IS USER ALREADY ADDED MOVIE IN FAVOURITE LIST OR NOT
                movie_list = movie_recommender(movie)

                movie_list = np.insert(movie_list, 0, movie)
                recommended = movie_detail(movie_list)
                postsdata = []

                other = []

                postsdata.append(other)
                postsdata.append(recommended)
                flash("Already in favourite", "info")
                return render_template("search_dash.html", postsdata=postsdata, movie=title_list)

            else:

                # adding to favourite collection of user
                new_user = db.engine.execute(
                    f"INSERT INTO `userdata` (`id`, `email`, `movie`, `poster`, `genre`, `duration`)  VALUES (NULL, '{fumail}','{movie}','{poster}','{genre}','{duration}');")

                movie_list = movie_recommender(movie)

                movie_list = np.insert(movie_list, 0, movie)
                recommended = movie_detail(movie_list)
                postsdata = []

                other = []

                postsdata.append(other)
                postsdata.append(recommended)
                flash("Added to favourite", "info")
                return render_template("search_dash.html", postsdata=postsdata, movie=title_list)
        except:

            render_template('not_found.html')

    return render_template("search_dash.html")





@app.route('/dashboard')
@login_required
def dashboard():
    try:
        email = current_user.umail
        deta = Userdata().query.filter_by(email=email).all()
        ##############################################################################################################
                                           # CHECKING USER BEHAVIOUR / user favourite movie collection 
        #########################################################################################################

        if deta:                          
            userId = current_user.id
            postsdata = []
            nl = []
            postsdata.append(nl)
            movie = deta[-1].movie                  ##################### currently i am taking last favourite movie of user we can take any number of movie and can recommend movie/ also we can use user search history data 
            movie_list = hybrid(userId, movie.title())  # hybrid model recommendation 
            movie_list = [x.lower() for x in movie_list]
            recommended = movie_detail(movie_list)
            postsdata.append(recommended)

            movie_list2 = movie_recommender(movie)    # also using normal recommendation to  recommend movie based on user behaviour 
            
            recommended_favourite = movie_detail(movie_list2)
            postsdata.append(recommended_favourite)

            # top
            vote = pd.read_csv('dataset/data_voting.csv')
            vote['title'] = vote['title'].str.lower()
            top_budget = []
            top_budget_data = vote.sort_values(by=['budget'], ascending=False)
            top_budget_datan = top_budget_data.iloc[:10, :]
            top_budget_datan = top_budget_datan['title'].to_list()
            data_top_budget = movie_detail(top_budget_datan)
            top_budget.append(data_top_budget)

            return render_template("dashboard.html", postsdata=postsdata, top=top_budget, movie=title_list)

        else:

            vote = pd.read_csv('dataset/data_voting.csv')
            vote['title'] = vote['title'].str.lower()

            postsdata = []

            data_by_vote = []
            postsdata.append(data_by_vote)

            # by popularity
            d_pop = vote.sort_values(by=['popularity'], ascending=False)
            nd_pop = d_pop.iloc[:6, :]
            nd_pop = nd_pop['title'].to_list()
            data_by_pop = movie_detail(nd_pop)

            postsdata.append(data_by_pop)
            # flash("Login Successful", "success")

            # top
            top_budget = []
            top_budget_data = vote.sort_values(by=['budget'], ascending=False)
            top_budget_datan = top_budget_data.iloc[:10, :]
            top_budget_datan = top_budget_datan['title'].to_list()
            data_top_budget = movie_detail(top_budget_datan)
            top_budget.append(data_top_budget)

            return render_template("dashboard.html", postsdata=postsdata, top=top_budget, movie=title_list)
    except:
        return render_template('not_found.html')


@app.route("/profile")
@login_required
def profile():
    try:
        return render_template("profile.html", movie=title_list)
    except:

        return render_template('not_found.html')


@app.route('/watchlist')
@login_required
def watchlist():

    try:

        umail = current_user.umail
        postsdata = History.query.filter_by(email=umail).all()
        m_l = []
        for row in postsdata:
            if row.action == 'played':
                if row.mname.lower() in title_list or row.mname.title() in title_list:
                    m_l.append(row.mname)

        m_l.reverse()  # to display lates movie first
        m_l = list(set(m_l))
      
        l = movie_detail(m_l)
        

        return render_template("watchlist.html", postsdata=l, movie=title_list)
    except:

        return render_template('not_found.html')

    # return render_template("watchlist.html")


@app.route('/favcol')
@login_required
def favcol():
    try:

        fumail = current_user.umail

        userdata = Userdata.query.filter_by(email=fumail).all()

        if userdata:

            return render_template("favcol.html", postsdata=userdata, movie=title_list)

        else:

            return render_template("favcol.html", movie=title_list)
    except:

        return render_template('not_found.html')

# ############################################################## genre based movie #######################################
@app.route('/genre')
@login_required
def genre():
    try:
        return render_template("genre.html", movie=title_list)
    except:

        return render_template('not_found.html')


@app.route('/thriller')
@login_required
def thriller():
    try:
        thriller = thriller_movies()
        return render_template("genre_specific.html", genre=thriller, name='Thriller', movie=title_list)
    except:

        return render_template('not_found.html')


@app.route('/horror')
@login_required
def horror():

    try:
        horror = horror_movies()
        return render_template("genre_specific.html", genre=horror, name='Horror', movie=title_list)
    except:

        return render_template('not_found.html')


@app.route('/crime')
@login_required
def crime():
    try:
        crime = crime_movies()
        return render_template("genre_specific.html", genre=crime, name='Crime', movie=title_list)
    except:

        return render_template('not_found.html')


@app.route('/action')
@login_required
def action():
    try:
        action = action_movies()
        return render_template("genre_specific.html", genre=action, name='Action', movie=title_list)
    except:

        return render_template('not_found.html')


@app.route('/adventure')
@login_required
def adventure():
    try:
        adventure = adventure_movies()
        return render_template("genre_specific.html", genre=adventure, name='Adventure', movie=title_list)
    except:

        return render_template('not_found.html')


@app.route('/playmovie', methods=['POST', 'GET'])
@login_required
def playmovie():
    try:
        if request.method == "POST":
            movie = request.form.get("playmovie")
            movie = movie.lower()

            duration = request.form.get("duration")
            genre = request.form.get("genre")
            action = 'played'
            fumail = current_user.umail

            new_user = db.engine.execute(
                f"INSERT INTO `history` (`id`, `email`, `mname`, `duration`, `genre`, `action`)  VALUES (NULL, '{fumail}','{movie}','{duration}','{genre}','{action}');")

            movie_list = []
            movie_list.append(movie)

            postsdata = movie_detail(movie_list)

            cast = cast_of_movie(movie)

            email = current_user.umail
            movie_id = get_movie_id(movie)

            rating_data = Rating_user.query.filter_by(
                id_user=current_user.id).all()
            if rating_data: # checking movie is already rated or not 

                rated_list = []
                for k in rating_data:
                    if k.mname == movie:
                        rated_list.append(k.rating)

                if len(rated_list) > 0:
                    return render_template("playmovie.html", postsdata=postsdata, cast=cast, rated_list=rated_list) #If rated then show user rating 
                else:
                    return render_template("playmovie.html", postsdata=postsdata, cast=cast)

            return render_template("playmovie.html", postsdata=postsdata, cast=cast, movie=title_list)

        return redirect(url_for('dashboard'))
    except:

        return render_template('not_found.html')


@app.route('/submitrating', methods=['POST', 'GET'])
@login_required
def submitrating():
    try:
        if request.method == "POST":
            u_id = current_user.id
            email = current_user.umail
            rating = request.form.get("rating")
            rating = float(rating)*2
            movie = request.form.get("movie").lower()
            movie_id = get_movie_id(movie)
            new_user = db.engine.execute(
                f"INSERT INTO `rating_user` (`id`,`id_user`, `movie_id`, `rating`,`mname`)  VALUES (NULL,'{u_id}', '{movie_id}','{rating}','{movie}');") # addes user rating in databse for future movie recommendation

            movie_list = []
            movie_list.append(movie)
            postsdata = movie_detail(movie_list)

            cast = cast_of_movie(movie)
            rated_list = []
            rated_list.append((rating))

            flash("Thanks for your rating ")
            return render_template("playmovie.html", postsdata=postsdata, cast=cast, rated_list=rated_list, movie=title_list)

        return redirect(url_for('dashboard'))
    except:

        return render_template('not_found.html')


@app.route('/history')
@login_required
def history():
    try:
        umail = current_user.umail
        postsdata = History.query.filter_by(email=umail).all()
        # # return "history"
        l = []
        for row in postsdata:
            if row.mname.lower() in title_list or row.mname.title() in title_list:
                temp_list = []
                temp_list.append((row.mname))
                temp_list.append((row.genre))
                temp_list.append((row.duration))
                temp_list.append((row.action))
                l.append(temp_list)

        if len(l)>30:
            l = l[-30:]  # show only latest 30 activity 

        return render_template("history.html", postsdata=l, movie=title_list)
    except:

        return render_template('not_found.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout Successful", "success")
    return redirect(url_for('home'))


app.run(debug=False)


#############################################################################################################################
                                                          #""" END  """
#############################################################################################################################
