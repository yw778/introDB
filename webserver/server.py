#!/usr/bin/env python2.7

"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver

To run locally:

    python server.py

Go to http://localhost:8111 in your browser.

A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response, url_for

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@104.196.18.7/w4111
#
# For example, if you had username biliris and password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://biliris:foobar@104.196.18.7/w4111"
#
DATABASEURI = "postgresql://hx2224:xuhan15801342399@35.196.90.148/proj1part2"


#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)

#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
#
# engine.execute("""CREATE TABLE IF NOT EXISTS test (
#   id serial,
#   name text
# );""")
# engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")


@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print ("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """

  # DEBUG: this is debugging code to see what request looks like
  print (request.args)


  #
  # example of a database query
  #
  cursor = g.conn.execute("SELECT * FROM hero")
  names = []
  ability = []
  for result in cursor:
    names.append(result['hid'])  # can also be accessed using result[0]
    ability.append(result['hname'])
  cursor.close()

  #
  # Flask uses Jinja templates, which is an extension to HTML where you can
  # pass data to a template and dynamically generate HTML based on the data
  # (you can think of it as simple PHP)
  # documentation: https://realpython.com/blog/python/primer-on-jinja-templating/
  #
  # You can see an example template in templates/index.html
  #
  # context are the variables that are passed to the template.
  # for example, "data" key in the context variable defined below will be 
  # accessible as a variable in index.html:
  #
  #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
  #     <div>{{data}}</div>
  #     
  #     # creates a <div> tag for each element in data
  #     # will print: 
  #     #
  #     #   <div>grace hopper</div>
  #     #   <div>alan turing</div>
  #     #   <div>ada lovelace</div>
  #     #
  #     {% for n in data %}
  #     <div>{{n}}</div>
  #     {% endfor %}
  #
  context = dict(data = zip(names, ability))


  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  return render_template("index.html", **context)

#
# This is an example of a different path.  You can see it at:
# 
#     localhost:8111/another
#
# Notice that the function name is another() rather than index()
# The functions for each app.route need to have different names
#
@app.route('/another')
def another():
  return render_template("another.html")

@app.route('/hero', methods=['POST', 'GET'])
def hero():
  print (request.args)
  cursor = g.conn.execute("SELECT * FROM hero")
  names = []
  name = []
  attack = []
  roles = []
  for result in cursor:
    names.append(result['hid'])  # can also be accessed using result[0]
    name.append(result['hname'])
    attack.append(result['attack_type'])
    roles.append(result['roles'])
  cursor.close()
  context = dict(data = zip(names, name, attack, roles))
  return render_template("hero.html", **context)

@app.route('/hero/search', methods=['POST'])
def hero_search():
  hid = int(request.form['heroid'])
  print (hid)
  cursor = g.conn.execute('SELECT * FROM hero WHERE hid=cast(%s as int)', hid)
  names = []
  name = []
  attack = []
  roles = []
  for result in cursor:
    names.append(result['hid'])  # can also be accessed using result[0]
    name.append(result['hname'])
    attack.append(result['attack_type'])
    roles.append(result['roles'])
  cursor.close()
  context = dict(data = zip(names, name, attack, roles))
  return render_template("hero.html", **context)

@app.route('/item', methods=['POST', 'GET'])
def item():
  print (request.args)
  cursor = g.conn.execute("SELECT * FROM item")
  names = []
  name = []
  price = []
  for result in cursor:
    names.append(result['iid'])  # can also be accessed using result[0]
    name.append(result['iname'])
    price.append(result['price'])
  cursor.close()
  context = dict(data = zip(names, name, price))
  return render_template("item.html", **context)

@app.route('/item/search', methods=['POST'])
def item_search():
  print request.form['iid']
  iid = int(request.form['iid'])
  cursor = g.conn.execute('SELECT * FROM item WHERE iid=cast(%s as int)', iid)
  names = []
  name = []
  price = []
  for result in cursor:
    names.append(result['iid'])  # can also be accessed using result[0]
    name.append(result['iname'])
    price.append(result['price'])
  cursor.close()
  context = dict(data = zip(names, name, price))
  return render_template("item.html", **context)

@app.route('/league', methods=['POST', 'GET'])
def league():
  print (request.args)
  cursor = g.conn.execute("""SELECT M.mid, P1.ptid AS team1, P2.ptid AS team2, T1.ptname AS name1, T2.ptname AS name2
                             FROM match_host M, play_in P1, play_in P2, pro_team T1, pro_team T2
                             WHERE M.mid=P1.mid and M.mid=P2.mid and P1.ptid < P2.ptid and T1.ptid=P1.ptid and T2.ptid=P2.ptid""")
  mids = []
  team1 = []
  team2 = []
  for result in cursor:
    mids.append(result['mid'])  # can also be accessed using result[0]
    team1.append((result['team1'], result['name1']))
    team2.append((result['team2'], result['name2']))
  cursor.close()
  context = dict(data = zip(mids, team1, team2))
  return render_template("league.html", **context)

@app.route('/league/search', methods=['POST'])
def league_search():
  lid = int(request.form['lid'])
  cursor = g.conn.execute("""SELECT M.mid, P1.ptid AS team1, P2.ptid AS team2, T1.ptname AS name1, T2.ptname AS name2 
                             FROM match_host M, play_in P1, play_in P2, pro_team T1, pro_team T2 
                             WHERE M.mid=P1.mid and M.mid=P2.mid and P1.ptid<P2.ptid and T1.ptid=P1.ptid and T2.ptid=P2.ptid and M.lid=cast(%s as int)""", lid)
  mids = []
  team1 = []
  team2 = []
  for result in cursor:
    mids.append(result['mid'])  # can also be accessed using result[0]
    team1.append((result['team1'], result['name1']))
    team2.append((result['team2'], result['name2']))
  cursor.close()
  context = dict(data = zip(mids, team1, team2))
  return render_template("league.html", **context)

@app.route('/team', methods=['POST', 'GET'])
def team():
  ptid = int(request.form['ptid'])
  cursor = g.conn.execute("""SELECT C.ptid, C.pid, C.position, C.pname, P.ptname
                             FROM player_consist_of C, pro_team P
                             WHERE C.ptid=cast(%s as int) and P.ptid=C.ptid""", ptid)
  players = []
  pnames = []
  position = []
  for result in cursor:
    players.append(result['pid'])  # can also be accessed using result[0]
    position.append(result['position'])
    pnames.append(result['pname'])
    ptname = result['ptname']
  cursor.close()
  context = dict(ptids=ptid, data = zip(players, pnames, position), ptname=ptname)
  return render_template("team.html", **context)

@app.route('/player', methods=['POST', 'GET'])
def player():
  print (request.args)
  cursor = g.conn.execute("""SELECT P.pid, P.pname, P.position, P.ptid, T.ptname
                             FROM player_consist_of P, pro_team T
                             WHERE T.ptid=P.ptid""")
  player = []
  name = []
  position = []
  team = []
  tname = []
  for result in cursor:
    player.append(result['pid'])  # can also be accessed using result[0]
    name.append(result['pname'])
    position.append(result['position'])
    team.append(result['ptid'])
    tname.append(result['ptname'])
  cursor.close()
  context = dict(data = zip(player, position, team, name, tname))
  return render_template("player.html", **context)

@app.route('/player/search', methods=['POST'])
def player_search():
  pid = int(request.form['pid'])
  cursor = g.conn.execute("""SELECT P.pid, P.pname, P.position, P.ptid, T.ptname
                             FROM player_consist_of P, pro_team T
                             WHERE T.ptid=P.ptid and P.pid=cast(%s as int)""", pid)
  player = []
  name = []
  position = []
  team = []
  tname = []
  for result in cursor:
    player.append(result['pid'])  # can also be accessed using result[0]
    name.append(result['pname'])
    position.append(result['position'])
    team.append(result['ptid'])
    tname.append(result['ptname'])
  cursor.close()
  context = dict(data = zip(player, position, team, name, tname))
  return render_template("player.html", **context)


@app.route('/match', methods=['POST'])
def match():
  mid = int(request.form['mid'])
  cursor1 = g.conn.execute("""SELECT B.hid, H.hname, B.kill, B.assist, B.death, B.gpm, B.xpm, B.last_hit, B.denies
                             FROM belong_to B, hero H
                             WHERE B.hid=H.hid and B.mid=cast(%s as int) and B.radiant=True""", mid)
  cursor2 = g.conn.execute("""SELECT B.hid, H.hname, B.kill, B.assist, B.assist, B.death, B.gpm, B.xpm, B.last_hit, B.denies
                             FROM belong_to B, hero H
                             WHERE B.hid=H.hid and B.mid=cast(%s as int) and B.radiant=False""", mid)
  hero1 = []
  for result in cursor1:
    hid = result['hid']
    cursorItem = g.conn.execute("""SELECT O.iid, I.iname
                                   FROM own O, item I
                                   WHERE O.iid=I.iid and O.mid=cast(%s as int) and O.hid=cast(%s as int)""", mid, hid)
    items = []
    for item in cursorItem:
      items.append((item['iid'], item['iname']))
    hero1.append((result['hid'], result['hname'], items, result['kill'], result['assist'], result['death'], result['gpm'], result['xpm'], result['last_hit'], result['denies']))
    cursorItem.close()
  cursor1.close()
  hero2 = []
  for result in cursor2:
    hid = result['hid']
    cursorItem = g.conn.execute("""SELECT O.iid, I.iname
                                   FROM own O, item I
                                   WHERE O.iid=I.iid and O.mid=cast(%s as int) and O.hid=cast(%s as int)""", mid, hid)
    items = []
    for item in cursorItem:
      items.append((item['iid'], item['iname']))
    hero2.append((result['hid'], result['hname'], items, result['kill'], result['assist'], result['death'], result['gpm'], result['xpm'], result['last_hit'], result['denies']))
    cursorItem.close()
  cursor2.close()
  context = dict(mid=mid, team1 = hero1, team2 = hero2)
  return render_template("match.html", **context)

@app.route('/summary', methods=['POST', 'GET'])
def summary():
  print (request.args)
  hero = g.conn.execute("""SELECT DISTINCT B1.hid, Temp1.max, H.hname
                           FROM (SELECT MAX(Temp.total) as max
                                 FROM (SELECT COUNT(*) as total
                                       FROM belong_to B
                                       GROUP BY B.hid) Temp) Temp1, belong_to B1, hero H
                           WHERE B1.hid=H.hid and Temp1.max=(SELECT COUNT(*) as total
                                                          FROM belong_to B2
                                                          WHERE B2.hid=B1.hid)""")
  # item = g.conn.execute("""SELECT DISTINCT O1.iid, Temp1.max
  #                          FROM (SELECT MAX(Temp.total) as max
  #                                FROM (SELECT COUNT(*) as total
  #                                      FROM own O
  #                                      GROUP BY O.iid) Temp) Temp1, own O1
  #                          WHERE Temp1.max=(SELECT COUNT(*) as total
  #                                           FROM own O2
  #                                           WHERE O2.iid=O1.iid)""")
  summary = g.conn.execute("""SELECT MAX(B.kill) as kill, MAX(B.gpm) as gpm, MAX(B.xpm) as xpm
                              FROM belong_to B""")
  rank = g.conn.execute("""SELECT C.lid, C.ptid as cid, C.ptname as cname, R.ptid as rid, R.ptname as rname
                           FROM (SELECT P.lid, P.ptid, T.ptname
                                 FROM participate P, pro_team T
                                 WHERE P.ptid=T.ptid and P.rank=1) C,
                                (SELECT P.lid, P.ptid, T.ptname
                                 FROM participate P, pro_team T
                                 WHERE P.ptid=T.ptid and P.rank=2) R
                           WHERE C.lid = R.lid""")
  summaryhero = []
  maxhero = []
  f = []
  for result in hero:
    summaryhero.append((result['hid'], result['hname']))  # can also be accessed using result[0]
    maxhero.append(result['max'])  # can also be accessed using result[0]
  hero.close()
  for result in rank:
    f.append((result['lid'], result['cid'], result['cname'], result['rid'], result['rname']))
  # summaryitem = []
  # maxitem = []
  # for result in item:
  #   summaryitem.append(result['iid'])  # can also be accessed using result[0]
  #   maxitem.append(result['max'])  # can also be accessed using result[0]
  # item.close()
  summarys = []
  for result in summary:
    summarys.append((result['kill'], result['gpm'], result['xpm']))
  summary.close()
  # context = dict(hero = zip(summaryhero, maxhero), item = zip(summaryitem, maxitem), data = summarys)
  context = dict(hero = zip(summaryhero, maxhero), data = summarys, rank=f)
  return render_template("summary.html", **context)

@app.route('/inference', methods=['POST', 'GET'])
def inference():
  print (request.args)
  cursor = g.conn.execute("""SELECT DISTINCT B1.hid as hero1, B2.hid as hero2, Temp.max
                             FROM belong_to B1, belong_to B2, (SELECT MAX(CAST(Temp1.total as FLOAT)/CAST(Temp2.total as FLOAT)) as max
                                                               FROM (SELECT COUNT(*) as total, B3.hid as hero1, B4.hid as hero2
                                                                     FROM belong_to B3, belong_to B4, team_compose T
                                                                     WHERE B3.mid=B4.mid and B3.radiant=B4.radiant and B3.hid<B4.hid
                                                                           and B3.mid=T.mid and B3.radiant=T.radiant and T.win=true
                                                                     GROUP BY B3.hid, B4.hid
                                                                     HAVING COUNT(*)>4) Temp1,
                                                                     (SELECT COUNT(*) as total, B7.hid as hero1, B8.hid as hero2
                                                                     FROM belong_to B7, belong_to B8, team_compose T3
                                                                     WHERE B7.mid=B8.mid and B7.radiant=B8.radiant and B7.hid<B8.hid
                                                                           and B7.mid=T3.mid and B7.radiant=T3.radiant
                                                                     GROUP BY B7.hid, B8.hid
                                                                     HAVING COUNT(*)>4) Temp2
                                                               WHERE Temp1.hero1=Temp2.hero1 and Temp1.hero2=Temp2.hero2) Temp
                             WHERE B1.mid=B2.mid and B1.radiant=B2.radiant and B1.hid<B2.hid
                             and Temp.max=(SELECT MAX(CAST(Temp3.total as float)/CAST(Temp4.total as float))
                                            FROM (SELECT COUNT(*) as total
                                                  FROM belong_to B5, belong_to B6, team_compose T1
                                                  WHERE B5.mid=B6.mid and B5.radiant=B6.radiant and B5.hid=B1.hid and B6.hid=B2.hid
                                                  and B5.mid=T1.mid and B5.radiant=T1.radiant and T1.win=true
                                                  GROUP BY B5.hid, B6.hid
                                                  HAVING COUNT(*)>4) Temp3,
                                                 (SELECT COUNT(*) as total
                                                  FROM belong_to B9, belong_to B0, team_compose T2
                                                  WHERE B9.mid=B0.mid and B9.radiant=B0.radiant and B9.hid=B1.hid and B0.hid=B2.hid
                                                  and B9.mid=T2.mid and B9.radiant=T2.radiant
                                                  GROUP BY B9.hid, B0.hid
                                                  HAVING COUNT(*)>4) Temp4)""")
  inference = []
  for result in cursor:
    inference.append((result['hero1'], result['hero2'], result['max']))
  cursor.close()
  context = dict(data = inference)
  return render_template("inference.html", **context)


# Example of adding new data to the database
@app.route('/add', methods=['POST'])
def add():
  name = request.form['name']
  g.conn.execute('INSERT INTO test (name) VALUES (%s)', name)
  return redirect('/')


@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()


if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help

    """

    HOST, PORT = host, port
    print ("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()
