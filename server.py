from flask import Flask, request, render_template, redirect
from plexapi.server import PlexServer
from plexapi.media import Media
from plexapi.library import Library

app = Flask(__name__)

SERVER_IP = 'SERVER_IP_ADDR'
PORT = 'SERVER_PORT'
TOKEN = 'PLEX_X-TOKEN'

def dump(obj):
  for attr in dir(obj):
    print("obj.%s = %r" % (attr, getattr(obj, attr)))

@app.route("/")
def hello():
	baseurl = 'http://' + SERVER_IP + ':' + PORT
	plex = PlexServer(baseurl, TOKEN)
	account = plex.myPlexAccount()
	
	art = None
	showTitle = None
	title = None
	username = None
	sessions = []
	
	for i in plex.sessions():
		art = i.artUrl
		if i.type == 'episode':
			showTitle = i.grandparentTitle
		else:
			showTitle = ''
		title = i.title
		username = i.usernames[0]
		
		session = {'art': art, 'showTitle': showTitle, 'title': title, 'username': username}
		sessions.append(session)
		
	return render_template('index.html', sessions=sessions)

@app.route("/watch", methods=["GET"])
def loadMain():	
	return redirect("/", code=302)
	
@app.route("/watch", methods=["POST"])
def data():
	baseurl = 'http://' + SERVER_IP + ':' + PORT
	plex = PlexServer(baseurl, TOKEN)
	account = plex.myPlexAccount()
	
	player = request.form.get('player')
	
	for client in plex.clients():
		if (player == client.name):
			media = plex.search(request.form.get('title'))
			player.playMedia(media)
			return render_template('success.html', art=request.form.get('art'), player=player, title=request.form.get('title'))
			
	return render_template('notfound.html', art=request.form.get('art'))
if __name__ == '__main__':
    app.run(debug=True)