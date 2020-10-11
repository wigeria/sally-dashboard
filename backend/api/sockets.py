""" Contains handlers for socket connections via SocketIO """


from flask import request
from flask_socketio import Namespace, emit, send, ConnectionRefusedError
from backend import settings
from backend.api import socketio
from backend.database.models import User


class JobsNamespace(Namespace):
    def on_connect(self):
        if request.args.get("secret", None):
            if request.args["secret"] == settings.WS_SECRET:
                send("Hello!")
                return
        else:
            try:
                user = User.validate_jwt(request.args["token"])
                if user is not None:
                    send("Hello")
                    return
            except:
                raise ConnectionRefusedError("Unauthorized")
        raise ConnectionRefusedError("Unauthorized")

    def on_disconnect(self):
        send("Goodbye!")

    def on_job_update(self, data):
        """ This is emitted by the task-worker client for each new log entry
            and once again on finish
        """
        socketio.emit('job_update_notification', data, broadcast=True)

socketio.on_namespace(JobsNamespace('/'))
