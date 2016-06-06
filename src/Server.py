from klein import Klein
from twisted.internet import task, reactor
from twisted.web.resource import Resource

import Sequential

app = Klein()

def delayedCall(n):
    return 'Delayed for %d seconds' % n

@app.route('/delay/<int:t>')
def delay(requests, t):
    """
    Delay the response by t seconds
    """
    if t > 0:
        d = task.deferLater(reactor, t, delayedCall, t)
        return d
    else:
        return delayedCall(0)

@app.route('/upload', branch=True)
def sequential(request):
    return Sequential.app.resource()


app.run('localhost', 8000)
