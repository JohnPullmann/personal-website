from flask import current_app
from flask_mail import Message
from website import mail, database
from website.models import PortfolioElement, Project, Work, Education, Certification
from sqlalchemy import desc, asc, union_all
from sqlalchemy.orm import aliased
from datetime import datetime, timedelta
from pprint import pprint

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


def build_portfolio_timeline():
    PortfolioTimeline = {}

    # Get all PortfolioElement objects ordered by date_filter
    PortfolioElements = PortfolioElement.query.order_by(asc(PortfolioElement.date_filter))

    start_date = PortfolioElements[0].date_filter
    date = start_date
    end_date = datetime.now()  # today
    while date <= end_date:
        # Add an entry to PortfolioTimeline for this month
        PortfolioTimeline[date.strftime('%Y-%m')] = {'education': {}, 'work': {}, 'events': {}}
        date += timedelta(days=30)
    
    for element in PortfolioElements:
        # Determine the type of the element
        element.type
        if element.type in ['education', 'work']:
            element_type = 'work' if element.type == 'work' else 'education'

            element_start_date = element.date_start.replace(day=1)
            element_date = element_start_date
            element_end_date = element.date_end.replace(day=1) if element.date_end else datetime.today().replace(day=1) +  timedelta(days=30)
            while element_date <= element_end_date:
                if element_date.month == element_start_date.month and element_date.year == element_start_date.year:
                    status = 's'
                elif element_date.month == element_end_date.month and element_date.year == element_end_date.year:
                    status = 'e'
                else:
                    status = 'i'
                PortfolioTimeline[element_date.strftime('%Y-%m')][element_type][f"{status}-{element.url_name}"] = element
                element_date += timedelta(days=30)
            ...
        elif element.type in ['certification']:
            element_type = 'events'
            PortfolioTimeline[element.date_filter.strftime('%Y-%m')][element_type][element.url_name] = element

        # Determine the start and end dates of the elemen

        # For each month from start_date to end_date, add the element to PortfolioTimeline
        #date = start_date
        #while date <= end_date:
        #    PortfolioTimeline[date.strftime('%Y-%m')][element_type][element.url_name] = element
        #    date += timedelta(days=30)

    #pprint(PortfolioTimeline)



    return PortfolioTimeline