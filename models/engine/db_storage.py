#!/usr/bin/python3



class DBStorage:
    """ """

    __engine = None
    __session = None

    __init__(self):
    """ """
    sel.__engine = create_engine('mysql+mysqldb://{}:{}@localhost/{}'.format(
        HBNB_MYSQL_USER, HBNB_MYSQL_PWD, HBNB_MYSQL_DB), pool_pre_ping=True)


    all(self, cls=None):
    """ """

    new(self, obj):
    """ """

    save(self):
    """ """

    delete(self, obj=None):
    """ """

    reload(self):
    """ """

def close(self):
        """ calls remove()
        """
        self.__session.close()    
