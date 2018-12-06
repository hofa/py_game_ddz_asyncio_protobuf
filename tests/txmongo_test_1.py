from txmongo.connection import ConnectionPool
from twisted.internet import defer, reactor

@defer.inlineCallbacks
def example():
    # tls_ctx = ServerTLSContext(privateKeyFileName='./mongodb.key', certificateFileName='./mongodb.crt')
    mongodb_uri = "mongodb://192.168.10.57:27017"

    # mongo = yield ConnectionPool(mongodb_uri, ssl_context_factory=tls_ctx)
    mongo = yield ConnectionPool(mongodb_uri)
    foo = mongo.foo  # `foo` database
    test = foo.test  # `test` collection

    # fetch some documents
    # yield test.insert({"title": "sb", "content": "sb"})
    docs = yield test.find(limit=10)
    for doc in docs:
        print(doc)

if __name__ == '__main__':
    example().addCallback(lambda ign: reactor.stop())
    reactor.run()