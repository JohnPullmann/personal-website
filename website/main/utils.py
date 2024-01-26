from flask import current_app
from flask_mail import Message
from website import mail, database
from website.models import PortfolioElement, Project, Work, Education, Certification
from sqlalchemy import desc, asc, union_all
from sqlalchemy.orm import aliased

def filter_portfolio_elements(button, search=None, sort=None):
    switch = {
        'Projects': Project,
        'Work': Work,
        'Education': Education,
        'Certifications': Certification
    }

    # Get elements from database based on button parameter
    Model = switch.get(button, PortfolioElement)

    # Apply search filter if search parameter is present
    if search:
        PortfolioElements = Model.query.filter(Model.name.contains(search))
    else:
        PortfolioElements = Model.query

    # Apply sorting if sort parameter is present
    if sort == 'newest':
        PortfolioElements = PortfolioElements.order_by(desc(Model.date_filter))
    elif sort == 'oldest':
        PortfolioElements = PortfolioElements.order_by(asc(Model.date_filter))
    elif sort == 'alphabetically':
        PortfolioElements = PortfolioElements.order_by(asc(Model.name))
    else:
        PortfolioElements = PortfolioElements.order_by(desc(Model.priority))


    return PortfolioElements