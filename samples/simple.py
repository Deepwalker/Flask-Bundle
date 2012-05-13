from flask import Flask

from flask.ext.bundle import expose
from flask.ext.bundle import api


app = Flask(__name__)
app.debug = True


class Room(api.APIBundle):
    @expose('/<int:id>')
    def get(self, id):
        "Return room info"
        return {'id': id}

    @expose('/<int:id>/message', methods=['POST'])
    def post_message(self, id):
        "Post new message"
        # create new message in given room
        return 'Done, my master.'

Room('room', '/room').push_bundle(app)

apis = list(api.dump_api(app))
api_generated = api.generate_api(apis, '127.0.0.1:5000')
for m in apis:
    print m

print api_generated.room.get.__dict__
#print 'API call result:', api_generated.room.get(id=1)
