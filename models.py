from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
import pandas as pd

Base = declarative_base()

class Paper(Base):
    __tablename__ = 'papers'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    abstract = Column(String)
    published_year = Column(String, nullable=True)

    def __repr__(self):
        return f'<Paper {self.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'abstract': self.abstract,
            'published_year': self.published_year,
        }

class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return f'<Author {self.name}>'
    
class AuthorPaper(Base):
    __tablename__ = 'authors_papers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    author_id = Column(Integer, ForeignKey('authors.id'))
    paper_id = Column(Integer, ForeignKey('papers.id'))
    author = relationship('Author', backref='author_papers')
    paper = relationship('Paper', backref='author_papers')
    
class AuthorCitePaper(Base):
    __tablename__ = 'authors_cite_papers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    author_id = Column(Integer, ForeignKey('authors.id'))
    paper_id = Column(Integer, ForeignKey('papers.id'))
    citation_year = Column(String)
    author = relationship('Author', backref='author_cite_papers')
    paper = relationship('Paper', backref='author_cite_papers')
    
## Load data
"""
def load_paper_csv(file_path, session):
    df = pd.read_csv(file_path)
    for index,row in df.iterrows():
        row_dict = row.to_dict()
        new_paper = Paper(id=row_dict['paper_id'], title=row_dict['title'], abstract=row_dict['abstract'], published_year=row_dict['published_year'])
        session.add(new_paper)
    session.flush()
    session.commit()    

def load_author_csv(file_path, session):
    df = pd.read_csv(file_path)
    for index,row in df.iterrows():
        row_dict = row.to_dict()
        new_author = Author(id=row_dict['author_id'], name=row_dict['author_name'])
        session.add(new_author)
    session.flush()
    session.commit()    

def load_author_paper_csv(file_path, session):
    df = pd.read_csv(file_path)
    for index,row in df.iterrows():
        row_dict = row.to_dict()
        new_author_paper = AuthorPaper(author_id=row_dict['author_id'], paper_id=row_dict['paper_id'])
        session.add(new_author_paper)
    session.flush()
    session.commit()    

def load_author_cite_paper_csv(file_path, session):
    df = pd.read_csv(file_path)
    for index,row in df.iterrows():
        row_dict = row.to_dict()
        new_author_paper = AuthorCitePaper(author_id=row_dict['author_id'], paper_id=row_dict['paper_id'], citation_year=row_dict['year_citation'])
        session.add(new_author_paper)
    session.flush()
    session.commit()    
"""