# -*- coding: utf-8 -*-

import os
# import gevent
# import gevent.monkey
# gevent.monkey.patch_all()

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell, Server

# from app import create_app, db
from app import app, db
from app.auth.models import User
from app.blog.models import Tag, Category, Article, CKPicture, BlogComment, Suggest

# app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)

# import sys
# print >> sys.stderr, app.url_map

def make_shell_context():
    return dict(
        app=app, db=db,
        User=User,Tag=Tag, Category=Category, Article=Article,
        CKPicture=CKPicture, BlogComment=BlogComment, Suggest=Suggest
    )

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
# manager.add_command( 'runserver', Server(host='localhost', port=8080, debug=True) )
manager.add_command( 'runserver', Server(host='0.0.0.0', port=5000 ) )

@manager.command
def recreate_db():
    """
    Recreates a local database. You probably should not use this on production.
    """
    db.drop_all()
    db.create_all()
    db.session.commit()

if __name__ == '__main__':
    manager.run()


