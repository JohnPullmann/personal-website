from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from website import database
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from website.users.models import User, Portfolio_Comment
from sqlalchemy.ext.declarative import declared_attr
from dateutil.relativedelta import relativedelta
from dateutil.rrule import rrule, MONTHLY

class PortfolioElement(database.Model):
    __tablename__ = 'portfolio_element'
    id = database.Column(database.Integer, primary_key=True)
    url_name = database.Column(database.String(100), nullable=False)
    timeline_name = database.Column(database.String(100), nullable=False)
    name = database.Column(database.String(100), nullable=False)
    description = database.Column(database.Text, nullable=False)
    tags = database.relationship('Tag', lazy='subquery',
        backref='portfolio_element')
    images_small = database.relationship('Image', backref='portfolio_element_small', lazy=True, foreign_keys='Image.portfolio_element_small_id')
    images = database.relationship('Image', backref='portfolio_element', lazy=True, foreign_keys='Image.portfolio_element_id')
    type = database.Column(database.String(50))
    date_filer_base = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    priority = database.Column(database.Integer, nullable=False, default=0)
    comments = database.relationship('Portfolio_Comment', backref='portfolio_element', lazy=True)

    date_start = database.Column(database.DateTime, default=None)
    date_end = database.Column(database.DateTime, default=None)

    __mapper_args__ = {
        'polymorphic_identity':'portfolio_element',
        'polymorphic_on':type
    }


    #this is used to filter the portfolio elements by date if no button is selected
    @hybrid_property
    def date_filter(self):
        return self.date_filer_base

    #this is for timespan filtering from timeline
    @property
    def element_timespan(self):
        if self.date_start:
            end_backup = self.date_end if self.date_end is not None else datetime.today()
            self.date_end = self.date_end.replace(day=1) if self.date_end else datetime.today().replace(day=1)
            dates = [d for d in rrule(MONTHLY, dtstart=self.date_start, until=self.date_end)]
            if self.date_end not in dates:
                dates.append(self.date_end)
            self.date_end = end_backup
            return dates
        else:
            return [self.date_filter]

    def __repr__(self):
        return f"PortfolioElement('{self.url_name}', '{self.type}', {self.date_filter})"
        #return f"PortfolioElement('{self.name}', '{self.id}', '{self.type}', '{self.description}', '{self.tags}', '{self.images}, {self.images_small}')"

class Image(database.Model):
    __tablename__ = 'image'
    id = database.Column(database.Integer, primary_key=True)
    image_path = database.Column(database.String(120), nullable=False)
    portfolio_element_id = database.Column(database.Integer, database.ForeignKey('portfolio_element.id'), nullable=True)
    portfolio_element_small_id = database.Column(database.Integer, database.ForeignKey('portfolio_element.id'), nullable=True)

    def __repr__(self):
        return f"Image('{self.id}', '{self.portfolio_element_id}',  '{self.image_path}')"

class Tag(database.Model):
    __tablename__ = 'tag'
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(100), nullable=False)
    portfolio_element_id = database.Column(database.Integer, database.ForeignKey('portfolio_element.id'), nullable=False)

    def __repr__(self) -> str:
        return f"Tag('{self.id}', '{self.name}')"

class Project(PortfolioElement):
    __tablename__ = 'project'
    id = database.Column(database.Integer, database.ForeignKey('portfolio_element.id'), primary_key=True)
    date = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    github_link = database.Column(database.String(100), default=None)

    __mapper_args__ = {
        'polymorphic_identity':'project',
    }

    @hybrid_property
    def date_text(self):
        return self.date.strftime('Started on %d. %b %Y')
    
    @hybrid_property
    def date_filter(self):
        return self.date

    def __repr__(self):
        return f"Project('{self.url_name}', '{self.type}', {self.date_text})"
        #return f"Project('{self.name}', '{self.id}', '{self.type}', '{self.description}', '{self.tags}', '{self.date}', '{self.date_text}',  '{self.images}, {self.images_small}')"


class Work(PortfolioElement):
    __tablename__ = 'work'
    id = database.Column(database.Integer, database.ForeignKey('portfolio_element.id'), primary_key=True)
    date_text = database.Column(database.String(100), nullable=False, default=PortfolioElement.date_start + ' - ' + PortfolioElement.date_end)
    work_link = database.Column(database.String(100), default=None)

    __mapper_args__ = {
        'polymorphic_identity':'work',
    }

    @hybrid_property
    def date_text(self):
        start = self.date_start.strftime('%b %Y')
        end = self.date_end.strftime('%b %Y') if self.date_end else 'Present'
        return f'{start} - {end}'
    
    @hybrid_property
    def date_filter(self):
        return self.date_start

    def __repr__(self):
        return f"Work('{self.url_name}', '{self.type}', {self.date_text})"

class Education(PortfolioElement):
    __tablename__ = 'education'
    id = database.Column(database.Integer, database.ForeignKey('portfolio_element.id'), primary_key=True)
    date_text = database.Column(database.String(100), nullable=False, default=PortfolioElement.date_start + ' - ' + PortfolioElement.date_end)
    education_link = database.Column(database.String(100), default=None)

    __mapper_args__ = {
        'polymorphic_identity':'education',
    }

    @hybrid_property
    def date_text(self):
        start = self.date_start.strftime('%b %Y')
        end = self.date_end.strftime('%b %Y') if self.date_end is not None else 'Present'
        return f'{start} - {end}'
    
    @hybrid_property
    def date_filter(self):
        return self.date_start

    def __repr__(self):
        return f"Education('{self.url_name}', '{self.type}', {self.date_text})"


class Certification(PortfolioElement):
    __tablename__ = 'certification'
    id = database.Column(database.Integer, database.ForeignKey('portfolio_element.id'), primary_key=True)
    valid_ranges = database.Column(database.String(100), nullable=False)
    first_acquired = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    expiration_date = database.Column(database.DateTime, default=None)
    date_text = database.Column(database.String(100), nullable=False, default=valid_ranges)
    verification_link = database.Column(database.String(100), default=None)

    __mapper_args__ = {
        'polymorphic_identity':'certification',
    }

    @hybrid_property
    def date_text(self):
        return f'Valid { self.valid_ranges}'
    
    @hybrid_property
    def date_filter(self):
        return self.first_acquired

    def __repr__(self):
        return f"Certification('{self.url_name}', '{self.type}', {self.first_acquired}, {self.valid_ranges})"