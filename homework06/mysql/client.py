import sqlalchemy
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker

from mysql.models import Base


class MysqlClient:

    def __init__(self, user, password, db_name):
        self.user = user
        self.password = password
        self.db_name = db_name

        self.host = '127.0.0.1'
        self.port = 3306

        self.engine = None
        self.connection = None
        self.session = None

    def connect(self, db_created=True):
        db = self.db_name if db_created else ''

        self.engine = sqlalchemy.create_engine(
            f'mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{db}',
            encoding='utf8'
        )
        self.connection = self.engine.connect()
        self.session = sessionmaker(bind=self.connection.engine,
                                    autocommit=False,  # use autocommit on session.add
                                    expire_on_commit=False  # expire model after commit (requests data from database)
                                    )()

    def execute_query(self, query, fetch=True):
        res = self.connection.execute(query)
        if fetch:
            return res.fetchall()

    def recreate_db(self):
        self.connect(db_created=False)
        self.execute_query(f'DROP database if exists {self.db_name}', fetch=False)
        self.execute_query(f'CREATE database {self.db_name}', fetch=False)
        self.connection.close()

    def create_total_requests(self):
        if not inspect(self.engine).has_table('total_requests'):
            Base.metadata.tables['total_requests'].create(self.engine)

    def create_requests_of_type(self):
        if not inspect(self.engine).has_table('requests_of_type'):
            Base.metadata.tables['requests_of_type'].create(self.engine)

    def create_frequent_requests(self):
        if not inspect(self.engine).has_table('frequent_requests'):
            Base.metadata.tables['frequent_requests'].create(self.engine)

    def create_big_failed_requests(self):
        if not inspect(self.engine).has_table('big_failed_requests'):
            Base.metadata.tables['big_failed_requests'].create(self.engine)

    def create_threat_origins(self):
        if not inspect(self.engine).has_table('threat_origins'):
            Base.metadata.tables['threat_origins'].create(self.engine)
