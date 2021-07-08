import itertools as it
from threading import Event

from flask import Flask, make_response, redirect, request


class Chat:
    def __init__(self):
        self._msgs = []
        self._waits = [Event()]

    def send(self, message):
        self._msgs.append(message)
        self._waits[-1].set()
        self._waits.append(Event())

    def wait_for_messages(self):
        self._waits[-1].wait()
        return self._msgs


# Too lazy to make multiple chat rooms
chats = {"test": Chat()}

app = Flask(__name__)

users = iter(it.count())


@app.post("/message")
def on_message():
    try:
        fmt = f"{request.cookies['userid']}: %s"
    except KeyError:
        fmt = "%s"
    chats["test"].send(fmt % request.form["message"])
    return redirect("/message")


@app.get("/message")
def get_chatbox():
    return """
    <body>
        <form action="/message" method="post" target="_self">
            <input type="text" name="message" value="" />
            <input type="submit" value="Send" />
        </form>
    </body>
    """


@app.get("/chats")
def chatview():
    messages = chats["test"].wait_for_messages()
    response = """
    <html>
        <head>
            <meta http-equiv="refresh" content="0">
        </head>
        <body>
            <div>{}</div>
        </body>
    </html>
    """.format(
        "".join(
            # TODO: fix xss vuln
            # nvm noscript means no xss
            f"<p>{msg}</p>"
            for msg in messages[::-1]
        )
    )
    return response


# Needs initial view of chats to prevent timeout error
@app.get("/initchats")
def chatviewinit():
    messages = chats["test"]._msgs
    usernum = f"{next(users)}"
    chats["test"].send(f"New user: {usernum}")
    view = """
    <html>
        <head>
            <meta http-equiv="refresh" content="0; url=/chats">
        </head>
        <body>
            <div id="scroller">
                {}
                <div id="anchor" />
            </div>
        </body>
    </html>
    """.format(
        "".join(f"<p>{msg}</p>" for msg in messages[100::-1])
    )
    response = make_response(view)
    response.set_cookie("userid", usernum)
    return response


@app.get("/")
def index():
    return """
    <html>
        <body>
            <p>Noscript chat for devout followers of Saint Ignucius</p>
            <div style="display: flex; flex-direction: column; width: 40%; height: 100%">
                <iframe src="./initchats" height="70%"></iframe>
                <iframe
                 src="./message" height="15%"
                 sandbox="allow-top-navigation allow-scripts allow-forms allow-same-origin"
                ></iframe>
            </div>
        </body>
    </html>
    """


if __name__ == "__main__":
    app.run("0.0.0.0", 8080, threads=100)
