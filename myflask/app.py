from flask import Flask, redirect, url_for, request, render_template, g
from flask_bootstrap import Bootstrap
from flask_script import Manager
import csv
import sqlite3
import json

app = Flask(__name__)
manager =Manager(app)
bootstrap = Bootstrap(app)

@app.before_first_request
def create_db_user():
	db = sqlite3.connect('user.db', isolation_level=None)
	c = db.cursor()
	c.execute('''DROP TABLE IF EXISTS user''')
	c.execute('''CREATE TABLE user (email text,password text,groups text);''')
	users = [('admin1@admin1','admin1','admin')
				,('admin2@admin2','admin2','admin')
				,('admin3@admin3','admin3','admin')
				,('guest1@guest1','guest1','guest')
				,('guest2@guest2','guest2','guest')
				,('guest3@guest3','guest3','guest')]
	c.executemany('insert into user (email,password,groups) values (?,?,?)',users)
	db.commit()
	db.close()

@app.before_first_request
def create_db_product_cpu():
	db = sqlite3.connect('product.db', isolation_level=None)
	c = db.cursor()
	c.execute('''DROP TABLE IF EXISTS product_cpu''')
	c.execute('''CREATE TABLE product_cpu (groups text, image_path text, product_name text, price text, content text, footer text);''')
	product_cpu_list = [('CPU','static/img/i9-10920x.jpg','i9-10920X','$5999','clockrate: 3.5/4.6GHzMHz,Socket:LGA 2066,Cache:19.25MB','The best CPU for now'),
						('CPU','static/img/i9-9900k.jpg','i9-9900K','$3999','clockrate: 3600-5000MHz,Socket: LGA1151,Cache:16 MB SmartCache','Best for gaming'),
						('CPU','static/img/i7-9700k.jpg','i7-9700K','$3200','Clockrate :3600 MHz Max Turbo 4900MHz,Socket:LGA 1151,Cache:12 MB','&#9733; &#9733; &#9733; &#9733; &#9734;'),
						('CPU','static/img/3900x.jpg','3900X','$4599','clockrate:3.30 GHz/4.10 GHzMHz,Socket:AM4,Cache:L3 64MB','&#9733; &#9733; &#9733; &#9733; &#9733;'),
						('CPU','static/img/3700x.jpg','3700X','$2599','clockrate:3.6GHz/4.4GHzMHz,Socket:AM4,Cache:L3 32MB','&#9733; &#9733; &#9733; &#9733; &#9734;'),
						('CPU','static/img/3600.jpg','3600','$1599','clockrate:3.6GHz/4.2GHzMHz,Socket:AM4,Cache:L3 32MB','&#9733; &#9733; &#9734; &#9734; &#9734;')]
	c.executemany('insert into product_cpu (groups, image_path, product_name, price, content, footer) values (?,?,?,?,?,?)',product_cpu_list)
	c.execute('''DROP TABLE IF EXISTS product_d_card''')
	c.execute('''CREATE TABLE product_d_card (groups text, image_path text, product_name text, price text, content text, footer text);''')
	product_d_card_list = [('d_card','static/img/2080ti.jpg','NVIDIA GeForce RTX2080 Ti','$12,550','The best. Nothing to say','Buy it is the only right choice'),
							('d_card','static/img/2060.jpg','MSI GeForce RTX2060 VENTUS 6G OC','$2750','RAM:6GB GDDR6,Input/Output:DisplayPort x 3 (v1.4) / HDMI 2.0b x 1,Clockrate (RAM/GPU):Boost Clock / Memory Speed 1710 MHz / 14 Gbps.','Best for gaming'),
							('d_card','sstatic/img/1660s.jpg','GIGABYTE GeForce GTX1660 SUPER GAMING OC 6G','$2100','RAM:6GB GDDR6,Input/Output:DisplayPort 1.4 *3, HDMI 2.0b *1,Clockrate (RAM/GPU):1860 MHz (Reference Card: 1785 MHz)','Best for gaming'),
							('d_card','static/img/3900x.jpg','Zotac Gaming GeForce RTX 2070 SUPER AMP','$4599','RAM 8GB GDDR6','Best for gaming'),
							('d_card','static/img/3700x.jpg','SAPPhiRE Radeon RX5700 XT 8G GDDR6','$3390','RAM:8GB GDDR6,Clockrate (RAM/GPU):GPU: Boost Clock: Up to 1905 MHz','Best for gaming'),
							('d_card','static/img/3600.jpg','GIGABYTE GeForce GTX 1650 SUPER OC 4G','$1380','RAM:4GB DDR6,Input/Output:DisplayPort 1.4 *1, HDMI 2.0b *1,DVI-D *1,Clockrate (RAM/GPU):1740 MHz (Reference Card: 1725 MHz)','Best for gaming')]
	c.executemany('insert into product_d_card (groups, image_path, product_name, price, content, footer) values (?,?,?,?,?,?)',product_d_card_list)
	c.execute('''DROP TABLE IF EXISTS product_game''')
	c.execute('''CREATE TABLE product_game (groups text, image_path text, product_name text, price text, content text, footer text);''')
	product_game_list = [('game','static/img/lol.jpg','League of Legends','Free','Oldest and the best','find someone with you'),
						('game','static/img/r6.jpg','Tom Clancy’s Rainbow Six Siege','$89','First-Person-Shooter! Tactics!','Try it and you will love it'),
						('game','static/img/cod.jpg','Call of Duty：Modern Warfare','$320','First-Person-Shooter! Tactics!','Try it and you will love it'),
						('game','static/img/angry.jpg','Coming Soon','$0','Coming Soon','Coming Soon'),
						('game','static/img/angry.jpg','Coming Soon','$0','Coming Soon','Coming Soon'),
						('game','static/img/angry.jpg','Coming Soon','$0','Coming Soon','Coming Soon')]
	c.executemany('insert into product_game (groups, image_path, product_name, price, content, footer) values (?,?,?,?,?,?)',product_game_list)
	db.commit()
	db.close()

@app.route('/')
def index():
	return render_template('index.html',logout = 1)

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/login', methods=['GET','POST'])
def login():
	db = sqlite3.connect('user.db', isolation_level=None)
	c = db.cursor()
	if request.method == 'GET':
		return render_template('login_page.html',logout = 1)
	if request.method == 'POST':
		email_li = request.values['email_li']
		password_li = request.values['password_li']
		try:
			c.execute('SELECT email FROM user WHERE email = ?',(email_li,))
			if not c.fetchone():
				return render_template('fail_login.html')
		except TypeError:
				return render_template('fail_login.html')
		else:
			groups = c.execute('SELECT groups FROM user WHERE email = ?',(email_li,))
			groups = c.fetchall()[0][0]
			return render_template('finish_login.html', email_li=email_li, password_li=password_li, groups=groups)

@app.route('/sign_up', methods=['GET','POST'])
def sign_up():
	db = sqlite3.connect('user.db', isolation_level=None)
	c = db.cursor()
	if request.method == 'GET':
		return render_template('sign_page.html')
	if request.method == 'POST':
		email_su = request.values['email_su']
		password_su = request.values['password_su']
		username_su = request.values['username_su']
		guest = 'guest'
		c.execute('INSERT INTO user (email,password,groups) VALUES (?,?,?)',(email_su,password_su,guest))
		db.commit()
		db.close()
		return render_template('finish_sign_in.html', email_su=email_su, password_su=password_su, username_su=username_su)

@app.route('/product')
def product():
	db = sqlite3.connect('product.db', isolation_level=None)
	c = db.cursor()
	product_cpu = c.execute('SELECT * FROM product_cpu').fetchall()
	output_product_cpu = []
	for row in product_cpu:
		output_product_cpu.append({
			'groups': row[0],
			'image_path': row[1],
			'product_name':row[2],
			'price':row[3],
			'content':row[4],
			'footer':row[5]
			})
	product_d_card = c.execute('SELECT * FROM product_d_card').fetchall()
	output_product_d_card = []
	for row in product_d_card:
		output_product_d_card.append({
			'groups': row[0],
			'image_path': row[1],
			'product_name':row[2],
			'price':row[3],
			'content':row[4],
			'footer':row[5]
			})
	product_game = c.execute('SELECT * FROM product_game').fetchall()
	output_product_game = []
	for row in product_game:
		output_product_game.append({
			'groups': row[0],
			'image_path': row[1],
			'product_name':row[2],
			'price':row[3],
			'content':row[4],
			'footer':row[5]
			})
	return render_template('product.html', output_product_cpu= output_product_cpu, output_product_d_card= output_product_d_card, output_product_game= output_product_game)

@app.route('/add_product', methods=['GET','POST'])
def add_data():
	if request.method =='GET':
		return render_template('/add_product.html')
	if request.method == 'POST':
		product_groups = request.values['groups']
		product_img_path = 'static/img/happy.jpg'
		product_name = request.values['name']
		product_price = request.values['price']
		product_content = request.values['content']
		product_comment = request.values['comment']
		product_input = [(product_groups),
						(product_img_path),
						(product_name),
						(product_price),
						(product_content),
						(product_comment)]	
		db = sqlite3.connect('product.db', isolation_level=None)
		c = db.cursor()
		if product_groups == 'cpu':
			c.execute('INSERT INTO product_cpu (groups,image_path,product_name,price,content,footer) VALUES (?,?,?,?,?,?)',
				(product_groups,product_img_path,product_name,product_price,product_content,product_comment,))
		elif product_groups == 'd_card':
			c.execute('INSERT INTO product_d_card (groups,image_path,product_name,price,content,footer) VALUES (?,?,?,?,?,?)',
				(product_groups,product_img_path,product_name,product_price,product_content,product_comment,))
		elif product_groups == 'game':
			c.execute('INSERT INTO product_game (groups,image_path,product_name,price,content,footer) VALUES (?,?,?,?,?,?)',
				(product_groups,product_img_path,product_name,product_price,product_content,product_comment,))
		db.commit()
		db.close()
	
		return render_template('success.html', 
			product_groups =product_groups,
			product_img_path = product_img_path,
			product_name= product_name,
			product_price = product_price,
			product_content = product_content,
			product_comment =product_comment
			)


if __name__ == '__main__':
	app.debug = True
	app.run(host="0.0.0.0", port=5000)