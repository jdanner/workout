from . import app

application = app


if __name__ == "__main__":
    application.run()

print('WSGI file loaded successfully')
print('Application object:', application)
