from proxypool.api import app
from proxypool.schedule import Schedule


def run():
    s = Schedule()
    s.run()
    app.run()


if __name__ == '__main__':
    run()
