from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TotalRequests(Base):
    __tablename__ = 'total_requests'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<Total requests(" \
               f"id='{self.id}'," \
               f"requests_count='{self.requests_count}', " \
               f"filename='{self.filename}'" \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    requests_count = Column(Integer, nullable=False)
    filename = Column(String(100), nullable=True)


class RequestOfType(Base):
    __tablename__ = 'requests_of_type'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<Requests of type(" \
               f"id='{self.id}'," \
               f"requests_type='{self.requests_type}', " \
               f"requests_count='{self.requests_count}', " \
               f"filename='{self.filename}'" \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    requests_type = Column(String(300), nullable=False)
    requests_count = Column(Integer, nullable=False)
    filename = Column(String(100), nullable=True)


class FrequentRequest(Base):
    __tablename__ = 'frequent_requests'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<Frequent request(" \
               f"id='{self.id}'," \
               f"url='{self.url}', " \
               f"requests_count='{self.requests_count}', " \
               f"filename='{self.filename}'" \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(1000), nullable=False)
    requests_count = Column(Integer, nullable=False)
    filename = Column(String(100), nullable=True)


class BigFailedRequest(Base):
    __tablename__ = 'big_failed_requests'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<Big failed request(" \
               f"id='{self.id}'," \
               f"url='{self.url}', " \
               f"error_code='{self.error_code}', " \
               f"size='{self.size}', " \
               f"origin_ip='{self.origin_ip}', " \
               f"filename='{self.filename}'" \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(1000), nullable=False)
    error_code = Column(Integer, nullable=False)
    size = Column(Integer, nullable=False)
    origin_ip = Column(String(40), nullable=False)
    filename = Column(String(100), nullable=True)


class ThreatOrigin(Base):
    __tablename__ = 'threat_origins'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<Threat origin(" \
               f"id='{self.id}'," \
               f"origin_ip='{self.origin_ip}', " \
               f"requests_count='{self.requests_count}', " \
               f"filename='{self.filename}'" \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    origin_ip = Column(String(40), nullable=False)
    requests_count = Column(Integer, nullable=False)
    filename = Column(String(100), nullable=True)
