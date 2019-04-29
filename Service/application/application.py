from flask import Flask
from flask_restful import Api
from application.resource import studio
from application.resource import movie
from application.resource import person
from application.resource import credit


def index():
    return "Welcome to Box Office Mentat!"


def create_app():
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(studio.Studio, '/studios/<id>')
    api.add_resource(studio.Studios, '/studios')

    api.add_resource(movie.Movie, '/movie/<id>')
    api.add_resource(movie.Movies, '/movies')

    api.add_resource(movie.Genres, '/genres')
    api.add_resource(movie.MpaaRatings, '/ratings')

    api.add_resource(person.Person, '/person/<id>')
    api.add_resource(person.SearchPeople, '/people')

    api.add_resource(credit.Credits, '/credits/<movie_id>')

    app.add_url_rule('/', 'index', index)

    return app


application = create_app()


@application.after_request
def add_cors_header(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


if __name__ == '__main__':
    application.run()

