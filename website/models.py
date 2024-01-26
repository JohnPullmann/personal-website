from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from website import database
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

class PortfolioElement(database.Model):
    __tablename__ = 'portfolio_element'
    id = database.Column(database.Integer, primary_key=True)
    url_name = database.Column(database.String(100), nullable=False)
    name = database.Column(database.String(100), nullable=False)
    description = database.Column(database.Text, nullable=False)
    tags = database.Column(database.String(100), nullable=False)
    images = database.relationship('Image', backref='portfolio_element', lazy=True)
    type = database.Column(database.String(50))

    __mapper_args__ = {
        'polymorphic_identity':'portfolio_element',
        'polymorphic_on':type
    }

    def __repr__(self):
        return f"PortfolioElement('{self.name}', '{self.id}', '{self.type}', '{self.description}', '{self.tags}', '{self.images}')"

class Image(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    image_path = database.Column(database.String(120), nullable=False)
    portfolio_element_id = database.Column(database.Integer, database.ForeignKey('portfolio_element.id'), nullable=False)

    def __repr__(self):
        return f"Image('{self.id}', '{self.portfolio_element_id}',  '{self.image_path}')"

class Project(PortfolioElement):
    __tablename__ = 'project'
    id = database.Column(database.Integer, database.ForeignKey('portfolio_element.id'), primary_key=True)
    date = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)

    __mapper_args__ = {
        'polymorphic_identity':'project',
    }

    @hybrid_property
    def date_text(self):
        return self.date.strftime('Started on %d. %b %Y')

    def __repr__(self):
        return f"Project('{self.name}', '{self.id}', '{self.type}', '{self.description}', '{self.tags}', '{self.date}', '{self.date_text}',  '{self.images}')"


class Work(PortfolioElement):
    __tablename__ = 'work'
    id = database.Column(database.Integer, database.ForeignKey('portfolio_element.id'), primary_key=True)
    date_start = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    date_end = database.Column(database.DateTime, default=None)
    date_text = database.Column(database.String(100), nullable=False, default=date_start + ' - ' + date_end)

    __mapper_args__ = {
        'polymorphic_identity':'work',
    }

    @hybrid_property
    def date_text(self):
        start = self.date_start.strftime('%b %Y')
        end = self.date_end.strftime('%b %Y') if self.date_end else 'Present'
        return f'{start} - {end}'

    def __repr__(self):
        return f"Work('{self.name}', '{self.id}', '{self.type}', '{self.description}', '{self.tags}', '{self.date_start}', '{self.date_end}', '{self.date_text}', '{self.images}')"


class Education(PortfolioElement):
    __tablename__ = 'education'
    id = database.Column(database.Integer, database.ForeignKey('portfolio_element.id'), primary_key=True)
    date_start = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    date_end = database.Column(database.DateTime, default=None)
    date_text = database.Column(database.String(100), nullable=False, default=date_start + ' - ' + date_end)

    __mapper_args__ = {
        'polymorphic_identity':'education',
    }

    @hybrid_property
    def date_text(self):
        start = self.date_start.strftime('%b %Y')
        end = self.date_end.strftime('%b %Y') if self.date_end else 'Present'
        return f'{start} - {end}'

    def __repr__(self):
        return f"Education('{self.name}', '{self.id}', '{self.type}', '{self.description}', '{self.tags}', '{self.date_start}', '{self.date_end}', '{self.date_text}', '{self.images}')"


class Certification(PortfolioElement):
    __tablename__ = 'certification'
    id = database.Column(database.Integer, database.ForeignKey('portfolio_element.id'), primary_key=True)
    valid_ranges = database.Column(database.String(100), nullable=False)
    expiration_date = database.Column(database.DateTime, default=None)
    date_text = database.Column(database.String(100), nullable=False, default=valid_ranges)

    __mapper_args__ = {
        'polymorphic_identity':'certification',
    }

    @hybrid_property
    def date_text(self):
        return f'Valid { self.valid_ranges}'

    def __repr__(self):
        return f"Certification('{self.name}', '{self.id}', '{self.type}', '{self.description}', '{self.tags}', '{self.valid_ranges}', '{self.date_text}', '{self.images}')"