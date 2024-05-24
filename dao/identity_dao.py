import os
from datetime import datetime
from sqlalchemy import or_
from entity import Contact
from model import IdentityRequestModel
from api import db


def identity_dao(identity_request: IdentityRequestModel):
    if identity_request.email and identity_request.phoneNumber:
        email_contacts = Contact.query.filter(Contact.email == identity_request.email).all()
        phoneNumber_contacts = Contact.query.filter(Contact.phoneNumber == identity_request.phoneNumber).all()

        # Case 1: Check if contact exist for incoming request
        if not email_contacts or not phoneNumber_contacts:
            if not email_contacts and not phoneNumber_contacts:
                add_as_primary(identity_request)
            else:
                add_as_secondary(identity_request)

        # Case 2: Check if primary can turn secondary
        """
            Step 1- Find min id object for both email and phoneNumber
            Step 2- Check if id is same. No action if same id
            Step 3- If id is different, 
                    change the larger id's linkPrecedence to secondary
                    add smaller id in its linkedId
        """
        min_email_contact = Contact.query.filter(Contact.email == identity_request.email).order_by(Contact.id).first()
        min_phone_contact = Contact.query.filter(Contact.phoneNumber == identity_request.phoneNumber).order_by(Contact.id).first()

        if min_phone_contact.id != min_email_contact.id:
            min_email_contact_id = min_email_contact.id
            min_phone_contact_id = min_phone_contact.id
            if min_email_contact_id < min_phone_contact_id:
                smaller_id = min_email_contact_id
                larger_contact = min_phone_contact
            else:
                smaller_id = min_phone_contact_id
                larger_contact = min_email_contact

            # change the larger ID's linkPrecedence to secondary
            larger_contact.linkPrecedence = os.getenv('SECONDARY')
            # add smaller ID in its linkedId
            larger_contact.linkedId = smaller_id
            db.session.commit()

    # Query the Contact entity for objects with the same email or phoneNumber
    contacts = Contact.query.filter(or_(Contact.email == identity_request.email,
                                        Contact.phoneNumber == identity_request.phoneNumber)).all()

    return contacts


def add_as_primary(identity_request: IdentityRequestModel):
    insert_contact(identity_request.phoneNumber, identity_request.email)


def add_as_secondary(identity_request: IdentityRequestModel):
    primary_contact = Contact.query.filter(or_(Contact.email == identity_request.email,
                                               Contact.phoneNumber == identity_request.phoneNumber)).order_by(Contact.id).first()
    insert_contact(identity_request.phoneNumber, identity_request.email, primary_contact.id, os.getenv('SECONDARY'))


def insert_contact(phoneNumber, email, linkedId=None, linkPrecedence=os.getenv('PRIMARY')):
    # Create a new Contact instance
    new_contact = Contact(
        phoneNumber=phoneNumber,
        email=email,
        linkedId=linkedId,
        linkPrecedence=linkPrecedence,
        createdAt=datetime.now(),
        updatedAt=datetime.now()
    )

    # Add the new contact to the session
    db.session.add(new_contact)

    # Commit the session to save the new contact to the database
    db.session.commit()
