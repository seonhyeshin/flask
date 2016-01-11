from flask import Flask,render_template, request, jsonify, session,flash, g, redirect, url_for

import urllib
from datetime import datetime
from bs4 import BeautifulSoup
from sqlite3 import dbapi2 as sqlite3
import os

app = Flask(__name__)

DATABASE = os.path.join(app.root_path, 'cd.db')

def init_db():
	with app.open_resource('schema.sql') as f:
		db.cursor().executescript(f.read())
	db.commit()

def get_db():
	if not hasattr(g, 'sqlite_db'):
		g.sqlite_db = sqlite3.connect(DATABASE)
	return g.sqlite_db

@app.teardown_request
def close_db(error):
	if hasattr(g,'sqlite_db'):
		g.sqlite_db.close()

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/search')
def search():
	k = request.args.get('k', "", type=str)
	try:
		html = urllib.urlopen("https://www.google.com/finance?q="+k+"&ei="+k)
        	soup = BeautifulSoup(html, "html.parser")
        	price = soup.find('meta', attrs={'itemprop':'price'})
        	change = soup.find('meta', attrs={'itemprop':'priceChange'})
        	symbol = soup.find('meta', attrs={'itemprop':'tickerSymbol'})
        	exchange = soup.find('meta', attrs={'itemprop':'exchange'})
        	code = (exchange['content'])+":"+(symbol['content'])
        	time = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		db=get_db()
		db.execute('insert into searchlist (code, time, price, change) values (?, ?, ?, ?)', (code, time, price['content'], change['content']))
		db.commit()
	
		return jsonify(result="Price : "+ price['content'] +", Price Change : "+ change['content'])

	except:
		return jsonify(result="code is not exist")

@app.route('/search_list')
def list():
	db = get_db()
	cur = db.execute('select * from searchlist')
	searchlist = cur.fetchall()
	return render_template('list.html', searchlist=searchlist)

if __name__ == '__main__':
	app.run()
