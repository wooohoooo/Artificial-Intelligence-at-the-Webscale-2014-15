
#!flask/bin/python
from flask import Flask,jsonify,abort,make_response,request
import numpy as np
import datetime
from flask import render_template,send_from_directory, send_file
#import md5
import hashlib
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
#from yourapplication import app
 
 
 
###############################################
#                                             #
# Implements a server serving Bandit Problems #
#                                             #
###############################################
 
 
 
 
#############
# Databases #
#############
 
from flask.ext.mongoalchemy import MongoAlchemy
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['MONGOALCHEMY_DATABASE'] = 'studentlib1'#change that name later
db = MongoAlchemy(app)
 
 
class Access(db.Document):
    """logs access to getcontext"""
    team_id = db.StringField()
    date = db.StringField()
    i = db.IntField()
    runid = db.IntField()
 
 
class PropPage(db.Document):
    """logs access to proposepage"""
    team_id = db.StringField()
    date = db.StringField()
 
class Cheaters(db.Document):
    """logs access to forbidden fruit"""
    team_id = db.StringField()
    date = db.StringField()
    i = db.IntField()
    runid = db.IntField()
 
def log(team,collection,num,run_id):
    """logs team id,i, runid and date in the specified collection"""
    acc = collection(team_id = team,date = str(datetime.datetime.utcnow()),
    i = num,runid=run_id)
    acc.save()
 
def log_page(team,collection):
    """logs team id and date in the proposepage collection"""
    acc = collection(team_id = team,date = str(datetime.datetime.utcnow()))
    acc.save()
 
 
############
# security #
############
 
def security(key,team_id):
    """bouncer. 
 
    takes teamid, hexdigests it and compares to given key.
	Key is super simple md5 hash"""
 
    team_id = team_id + 'howwouldYOUguessthat' #this one's been changed, of course.
    make_hash = hashlib.md5()
    tmp_key = team_id.encode('utf-8')
    make_hash.update(tmp_key)
    sec_key = make_hash.hexdigest()
    if key != sec_key:
        abort(403)
		
		
 
##############
# start page #
##############
 
@app.route('/',methods = ['GET'])
@app.route('/index',methods=['GET'])
#http://krabspin.uci.ru.nl/
#http://localhost:5000
def index():
    return render_template('index2.html')
 
 
@app.route('/downloads')
def download():
    return send_from_directory(directory='downloads',filename='Practical_Assignment.pdf',as_attachment=True)
 
 
@app.route('/description')
def description():
    return render_template('description.html')
 
 
@app.route('/about')
def about():
    return render_template('about.html')
 
@app.route('/material')
def material():
    return render_template('material.html')
 
@app.route('/intro')
def intro():
    return render_template('intro.html')
 
@app.route('/advanced')
def advanced():
    return render_template('advanced.html')
 
@app.route('/advanced/bandit')
def bandit():
    return render_template('bandit.html')
 
@app.route('/advanced/thompsonsampling')
def thompson():
    return render_template('thompsonsampling.html')
 
@app.route('/advanced/ContextBandit')
def contextbandit():
    return render_template('contextbandit.html')
 
@app.route('/intro/collfilter')
def collfilter():
    return render_template('collfilter.html')
 
@app.route('/intro/NaiveBayes')
def naivebayes():
    return render_template('Naive_Bayes.html')
 
 
 
###############
# Admin Stuff #
###############
 
###Counting
@app.route('/admin/count/access/',methods = ['GET'])
#http://krabspin.uci.ru.nl/admin/count/access/?pw=ThomasIsTheBest!
def admin_count_access():
    """accesses the database for get_context()"""
    pw = request.args.get('pw')
    teamids = Access.query.distinct(Access.team_id)
    ourkey = 'ThomasIsTheBest!'
    content = ""
    for teamid in teamids:
        accesses = Access.query.filter(Access.team_id ==teamid).count()
        content+='<p>%s: %d</p>'%(teamid,accesses)
    if pw != ourkey:
        abort(403)
    return content
 
@app.route('/admin/count/access_test/',methods = ['GET'])
#http://krabspin.uci.ru.nl/admin/count/access_test/?pw=ThomasIsTheBest!
def admin_count_access_test():
    """accesses the database for get_context()"""
    pw = request.args.get('pw')
    teamids = Access.query.distinct(Access.team_id)
    ourkey = 'ThomasIsTheBest!'
    content = ""
    for teamid in teamids:
        accesses = Access.query.filter(Access.team_id ==teamid,Access.runid>10000).count()
        content+='<p>%s: %d</p>'%(teamid,accesses)
    if pw != ourkey:
        abort(403)
    return content
 
@app.route('/admin/count/proppage/',methods = ['GET'])
#http://krabspin.uci.ru.nl/admin/count/proppage/?pw=ThomasIsTheBest!
def admin_count_proppage():
    """accesses the database for get_context()"""
    pw = request.args.get('pw')
    teamids = PropPage.query.distinct(PropPage.team_id)
    ourkey = 'ThomasIsTheBest!'
    content = ""
    for teamid in teamids:
        accesses = PropPage.query.filter(PropPage.team_id ==teamid).count()
        content+='<p>%s: %d</p>'%(teamid,accesses)
    if pw != ourkey:
        abort(403)
    return content
 
@app.route('/admin/count/cheaters/',methods = ['GET'])
#http://krabspin.uci.ru.nl/admin/count/cheaters/?pw=ThomasIsTheBest!
def admin_count_cheaters():
    """accesses the database for get_context()"""
    pw = request.args.get('pw')
    teamids = Cheaters.query.distinct(Cheaters.team_id)
    ourkey = 'ThomasIsTheBest!'
    content = ""
    for teamid in teamids:
        accesses = Cheaters.query.filter(Cheaters.team_id ==teamid).count()
        content+='<p>%s: %d</p>'%(teamid,accesses)
    if pw != ourkey:
        abort(403)
    return content
 
 
 
### not counting
@app.route('/admin/access/',methods = ['GET'])
#http://localhost:5000/admin/access/?pw=ThomasIsTheBest!
def admin_access():
    """accesses the database for get_context()"""
    pw = request.args.get('pw')
    ourkey = 'ThomasIsTheBest!'
    if pw != ourkey:
        abort(403)
    examples = Access.query.all()
    content = '<p>getcontext:</p>'
    for acc in examples:
        content +='<p>%s</p>' %acc.team_id
        content +='<p>%s</p>' %acc.date
        content +='<p>i = %s</p>' %acc.i
        content +='<p>run_id = %s</p>' %acc.runid
    return content
 
 
 
@app.route('/admin/proppage/',methods = ['GET'])
#http://localhost:5000/admin/proppage/?pw=ThomasIsTheBest!
def admin_proppage():
    """accesses database for propose_page"""
    pw = request.args.get('pw')
    ourkey = 'ThomasIsTheBest!'
    if pw != ourkey:
        abort(403)
    examples = PropPage.query.all()
    content = '<p>proppage:</p>'
    for acc in examples:
        content +='<p>%s</p>' %acc.team_id
        content +='<p>%s</p>' %acc.date
    return content
 
 
@app.route('/admin/cheaters/',methods = ['GET'])
#http://localhost:5000/admin/cheaters/?pw=ThomasIsTheBest!
def admin_cheaters():
    """ accesses database of dirty cheaters"""
    pw = request.args.get('pw')
    ourkey = 'ThomasIsTheBest!'
    if pw != ourkey:
        abort(403)
    examples = Cheaters.query.all()
    content = '<p>cheaters:</p>'
    for acc in examples:
        content +='<p>%s</p>' %acc.team_id
        content +='<p>%s</p>' %acc.date
        content +='<p>i = %s</p>' %acc.i
        content +='<p>run_id = %s</p>' %acc.runid
    return content
 
 
 
 
 
 
##########
# Models #
##########
 
def create_variables(i,m):
    """creates predetermined variables for the model
    begins with seed i+m to set user id
    then uses user id to compute age and user preference lists
    then uses user id + i to choose one from each preference list.
    """
    #set lists
    usr_agents = ['OSX','Windows','Linux']
    colors = ['black','green','red','blue']
    usr_refs = ['Google','Bing','NA']
    usr_lans = ['NL','EN','GE']
    #use runid and int as seed to draw user_id
    state = i+m
    np.random.seed(state)
    #draw user id
    user_ID = np.random.randint(1,5000)
    #use id as seed
    #create two-entry-lists (choices for each user)
    np.random.seed(user_ID)
    age = round(np.random.lognormal(3.5,.25))
    usr_ag_list = list(np.random.choice(usr_agents,1,replace=False)) + ['mobile']
    usr_lan_list = list(np.random.choice(usr_lans,2,replace=False))
    usr_ref_list = list(np.random.choice(usr_refs,2,replace=False))
    #set seed to user id + int
    #select one item from the two_lists
    np.random.seed(user_ID+i+10000)
    ag = np.random.choice(usr_ag_list,1)
    lan = np.random.choice(usr_lan_list,1)
    ref = np.random.choice(usr_ref_list,1)
    return user_ID,age,ag[0],lan[0],ref[0]
 
def personal_price_response(cluster,price,product):
    """computes personal response to pricing
    needs change. Bwahaha."""
    optimal_price =((product + cluster*2)/1.5)**2**1/2# cluster+ product #dummy price response..
    #could depend on age, os, product, cluster, ...
    return -(optimal_price *.003* price -1)
 
def personal_header_response(ag,head):
    """computes personal response to header"""
    if ag != 'mobile':
        return 0
    if head <15:
        return 1
    factor = np.random.choice([-1,0])#on mobile too long is sometimes bad
    return factor * head
 
def personal_color_response(color):
    """computes personal response to color"""
    colors = np.array(['black','green','red','blue'])
    color_vec = np.zeros(len(colors))
    color_vec[colors == color] = 1
    if color == 'black': #black text on black screen isn't readablw, thus always negative
        return -10
    col_resp = np.dot(color_vec,np.random.normal(0,1,4)) 
    return col_resp
 
def personal_adtype_response(ag,ad,cluster):
    """computes personal response to adtype"""
    if ag == 'mobile'and ad == 'banner': #noone likes banners on mobile
        return -10
    ad_list = np.array(['banner','skyscraper','square'])    
    ad_vec = np.zeros(len(ad_list))
    ad_vec[ad_list==ad]=1
    ad_resp = np.dot(ad_vec,np.random.normal(0,1,len(ad_list))) +cluster/5
    return ad_resp
     
def personal_ref_response(ref):
    ref_list = ['Google','Bing','NA']
    ref_vec = np.zeros(len(ref_list))
    ref_vec[ref_list==ref] = 1
    ref_resp = np.dot(ref_vec,np.random.normal(0,1,len(ref_list)))
    return ref_resp
 
     
     
 
def compute_response(i,runid,head,ad,color,product,price):
    """computes overall response.
    returns sum of all personal responses"""
    #make variables, depending on runid
	
    np.random.seed(runid)
    num_clusters = np.random.randint(5,10)
    eff_cluster = np.random.normal(0,5,num_clusters)
    num_products = 25#?
    user_ID,age,ag,lan,ref = create_variables(i,runid)
    cluster = np.random.randint(1,5)
    
	#draw cluster_effect, set seed User_ID
    np.random.seed(user_ID)
    user_cluster = np.random.randint(1,num_clusters)
    user_cluster_effect = eff_cluster[user_cluster]
    
	#draw personal product need, seed user_ID+lang+ag
    personal_product_need = np.random.normal(0,1,num_products)
    prod_vec = np.zeros(num_products)
    prod_vec[product] = 1
     
    #variable influence
    personal_product = np.dot(prod_vec,personal_product_need)
    personal_price = personal_price_response(user_cluster_effect ,price,product)
    personal_head = personal_header_response(ag,head)
    personal_color = personal_color_response(color)
    personal_adtype = personal_adtype_response(ag,ad,user_cluster_effect)
    personal_ref = personal_ref_response(ref)
    #make some price effect depending on the cluster.
     
     
    return np.sum([personal_price,
        personal_head,
        personal_color,
        personal_product,
        personal_adtype,
        personal_ref])
 
     
def sigmoid(X):
    """computes inverse logit"""
    return 1./(1.+np.exp(-X))
 

 
##############
# getContext #  
##############
 
@app.route('/getcontext.json/',methods = ['GET'])
#http://localhost:5000/getcontext.json/?i=3&runid=10&teamid=Thomas&teampw=fda52cd2fc221324a3a3b05599df5d3c
#http://krabspin.uci.ru.nl/getcontext.json/?i=3&runid=10&teamid=Thomas&teampw=fda52cd2fc221324a3a3b05599df5d3c
#http://krabspin.uci.ru.nl/getcontext.json/?i=3&runid=10&teamid=Maurits&teampw=6231e6ba646281fedd139f4c9b317371
def get_context():
    """generates context for i and m
    asks for right Teamid and teampw
    returns json object"""
    #get variables:
    team_id = request.args.get('teamid')
    team_pw = request.args.get('teampw')
    runid = int(request.args.get('runid'))
    i = int(request.args.get('i'))
    #call security
    security(team_pw,team_id)
    if i > 100000 or i < 0:
        abort(404)
 
    if runid >10100 or runid < 0:
        abort(404) 
 
    #if runid > 10000 and teamid=='Thomas':
    #   #log(team_id,Cheaters,i,runid)
    #   return jsonify({'note':'Authorities have been notified. Resistance is futile.'})
    #   abort(403)
    #if i > 10000 and teamid=='Thomas':
    #   #log(team_id,Cheaters,i,runid)
    #   return jsonify({'note':'Authorities have been notified. Resistance is futile.'})
    #   abort(403)
    #todo: logg legitimate acess to different mongodb.
    #if runid > 10000 and datetime.date.today() < datetime.date(2015,6,24):
    #   log(team_id,Cheaters,i,runid)
    #   return jsonify({'note':'Authorities have been notified. Resistance is futile.'})
    #   abort(403)
    #if runid > 10100:
    #   return jsonify({'note':'RunID is too high.'})
    #   abort(403)
 
 
 
 
         
        #abort(403)#why does this work. Without it, the normal database loggs cheaters 
    #make variables
    # log
    #log(team_id,Access,i,runid)
    user_ID,age,ag,lan,ref = create_variables(i,runid)
    context = [
{
    'ID' : user_ID,
    'Age':age,
    'Language': lan,
    'Agent' : ag,
    'Referer' : ref,
},
]
 
    if context==True:
        abort(404)
    return jsonify({'context':context[0]})
 
 
 
 
###############
# proposepage #
###############
 
@app.route('/proposePage.json/',methods = ['GET'])
#http://localhost:5000/proposePage.json/?i=3&runid=10&teamid=Thomas&header=5&adtype=banner&color=black&productid=10&price=10&teampw=fda52cd2fc221324a3a3b05599df5d3c
#http://krabspin.uci.ru.nl/proposePage.json/?i=3&runid=10&teamid=Thomas&header=5&adtype=banner&color=black&productid=10&price=10&teampw=fda52cd2fc221324a3a3b05599df5d3c
def propose_page():
    """calculates buy or leave response depending on input variables
    checks matching teamid and pw."""
    #old vars
    team_id = request.args.get('teamid')
    team_pw = request.args.get('teampw')
    runid = int(request.args.get('runid'))
    i = int(request.args.get('i'))
 
    #new vars
    head = int(request.args.get('header'))
    ad = request.args.get('adtype')
    color = request.args.get('color')
    product_id = int(request.args.get('productid'))
        product_id -= 1
    price = float(request.args.get('price'))
    if price <0 or price >50:
        return jsonify({'note':'The price is too high!'})
        abort(403)
    if product_id >24 or product_id < 9: # mind the -1
        return jsonify({'note':'Invalid_Id'})
        abort(403)
         
    #call security
    security(team_pw,team_id)
    #log
    #log_page(team_id,PropPage)
 
    if i > 100000 or i < 0:
        abort(404)
 
    if runid >10100 or runid <0:
        abort(404) 

		
    #if runid > 10100:
    #   return jsonify({'note':'RunID is too high.'})
    #   abort(403)
    #if runid > 10000 and datetime.date.today() < datetime.date(2015,6,24):
    #   log(team_id,Cheaters,i,runid)
    #   return jsonify({'note':'Authorities have been notified. Resistance is futile.'})
    #   abort(403)
    #if runid > 10000 and teamid=='Thomas':
    #   #log(team_id,Cheaters,i,runid)
    #   return jsonify({'note':'Authorities have been notified. Resistance is futile.'})
    #   abort(403)
    #if runid > 10000 and teamid=='Thomas':
    #   #log(team_id,Cheaters,i,runid)
    #   return jsonify({'note':'Authorities have been notified. Resistance is futile.'})
    #   abort(403)
 
 
 
    #THEMODEL
    response = compute_response(i,runid,head,ad,color,product_id,price)
    #maps to probability
    response = sigmoid(response)
    response = np.random.binomial(1,response)
#   if response == 0:
#       response = 'leave'
#   if response == 1:
#       response = 'buy'
    effect = [
{
    'Success':response,
    'Error' : None
},
]
    if effect ==True:
        abort(404)
    return jsonify({'effect':effect[0]})
 
 
 
 
 
 
###################
# errors and Main #
###################
 
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error':'Not found'}),404)
 
@app.errorhandler(403)
def forbidden_data(error):
    return make_response(jsonify({'error':'Forbidden.'}),403)
 
if __name__ == '__main__':
 
 http_server = HTTPServer(WSGIContainer(app))
 http_server.listen(80, address='0.0.0.0')
 IOLoop.instance().start()
 #app.run(host='0.0.0.0',port=80)
 
 
    