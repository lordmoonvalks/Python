#running the app

from flaskblog import create_app #from init

app = create_app()


if __name__ == '__main__':
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
	app.run(debug=True)


