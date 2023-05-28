import random

from flask import Flask, Request, request, Response
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
from flask_caching import Cache

from storage import store, tag_presets

app = Flask(__name__)
# app.config['CACHE_TYPE'] = "FileSystemCache"
# app.config['CACHE_DIR'] = "cache"

CORS(app)
api = Api(app)
# cache = Cache(app)


class Media(Resource):

    def __init__(self):
        self.media = store.get_curr_media()

    # @cache.cached(timeout=3000)
    def get(self, route):
        print('route -->', route)

        match route:
            case 'all':
                return self.media.get_all_media(), 200

            case 'info':
                return {'rating_range': self.media.get_media_rating_range()}, 200

            case 'load_more':
                return self.media.load_more()

    def post(self, route):
        req = request.json
        print('route -->', route)

        match route:
            case 'settings':
                store.set_current_media(req['media_type'])
                self.media = store.get_curr_media()

                self.media.set_settings(req['settings'])
                self.media.set_filters(req['filters'])
                return 200

            case 'filters':
                self.media.set_filters(req['filters'])
                return 200

            case 'media':
                self.media.add_media(req)
                return 200

    def put(self, route):
        req = request.json
        print('route -->', route)

        match route:
            case 'media':
                self.media.update_media(req)
                return 200

            case 'check_dupe':
                return self.media.check_dupe(req)

            case 'cover':
                return self.media.get_cover(req)

    def delete(self, route):
        req = request.json
        print('route -->', route)

        match route:
            case 'media':
                self.media.del_media(req)
                return 200


class Tags(Resource):
    def __init__(self):
        self.presets = tag_presets

    def get(self):
        return self.presets.get_all_presets(), 200

    def post(self):
        req = request.json
        return self.presets.add_preset(req), 200

    def delete(self):
        req = request.json
        return self.presets.del_preset(req), 200


api.add_resource(Media, '/media/<route>')
api.add_resource(Tags, '/tags')

if __name__ == '__main__':
    app.run(debug=False)
