from flask import Flask

import bundle


app = Flask(__name__)
app.debug = True


class Room(bundle.APIBundle):
    @bundle.expose('/<int:id>')
    def get(self, id):
        "Return room info"
        return {}

    @bundle.expose('/<int:id>/message', methods=['POST'])
    def post_message(self, id):
        "Post new message"
        # create new message in given room
        return 'Done, my master.'

Room('room', '/room').push_bundle(app)

apis = list(bundle.dump_api(app))
api = bundle.generate_api(apis, '127.0.0.1:5000')
for m in apis:
    print m

print api.room.get.__dict__
#print 'API call result', api.room.get(id=1)
