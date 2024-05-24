import os
from datetime import datetime
from sqlalchemy import or_
from entity import Contact
from model import IdentityRequestModel
from api import db
from collections import deque


def identity_dao(identity_request: IdentityRequestModel):
    """
        Data Access Layer of /identity API

        :param identity_request: IdentityRequestModel
        :return: contacts: Contact[]
    """
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
        primary_to_secondary(identity_request)

    # Query the Contact entity for objects
    contacts = bfs_contact_search(identity_request)
    if not contacts:
        add_as_primary(identity_request)
        contacts = bfs_contact_search(identity_request)

    return contacts


def add_as_primary(identity_request: IdentityRequestModel):
    """
        Function to trigger insert of new contact as primary contact.

        :param identity_request: IdentityRequestModel
        :return: nothing
    """

    insert_contact(identity_request.phoneNumber, identity_request.email)


def add_as_secondary(identity_request: IdentityRequestModel):
    """
        Function to trigger insert of new contact as secondary contact.

        :param identity_request: IdentityRequestModel
        :return: nothing
    """

    primary_contact = Contact.query.filter(or_(Contact.email == identity_request.email,
                                               Contact.phoneNumber == identity_request.phoneNumber)).order_by(
        Contact.id).first()
    insert_contact(identity_request.phoneNumber, identity_request.email, primary_contact.id, os.getenv('SECONDARY'))


def insert_contact(phoneNumber, email, linkedId=None, linkPrecedence=os.getenv('PRIMARY')):
    """
        Function to push new contact to DB.

        :param phoneNumber: str
        :param email: str
        :param linkedId: str
        :param linkPrecedence: str
        :return: nothing
    """

    # Create a new Contact instance
    new_contact = Contact(
        phoneNumber=phoneNumber,
        email=email,
        linkedId=linkedId,
        linkPrecedence=linkPrecedence,
        createdAt=datetime.now(),
        updatedAt=datetime.now()
    )

    # Add the new contact to the session and commit
    db.session.add(new_contact)
    db.session.commit()


def primary_to_secondary(identity_request: IdentityRequestModel):
    """
        Function to check and convert contacts primary to secondary.

        :param identity_request: IdentityRequestModel
        :return: nothing
    """

    # Step 1- Find min id object for both email and phoneNumber.
    min_email_contact = Contact.query.filter(Contact.email == identity_request.email).order_by(Contact.id).first()
    min_phone_contact = Contact.query.filter(Contact.phoneNumber == identity_request.phoneNumber).order_by(
        Contact.id).first()

    # Step 2- Check if id is same. No action if same id.
    if min_phone_contact.id != min_email_contact.id:
        min_email_contact_id = min_email_contact.id
        min_phone_contact_id = min_phone_contact.id
        if min_email_contact_id < min_phone_contact_id:
            smaller_id = min_email_contact_id
            larger_contact = min_phone_contact
        else:
            smaller_id = min_phone_contact_id
            larger_contact = min_email_contact

        # Step 3- Change the larger ID's linkPrecedence to secondary and add smaller ID in its linkedId
        larger_contact.linkPrecedence = os.getenv('SECONDARY')
        larger_contact.linkedId = smaller_id

        # Update linkedId of records whose linkedIds where larger_contact's id
        update_contacts = Contact.query.filter(Contact.linkedId == larger_contact.id).all()
        [setattr(update_contact, 'linkedId', smaller_id) for update_contact in update_contacts]

        db.session.commit()


def bfs_contact_search(identity_request: IdentityRequestModel):
    """
        Perform a BFS to find all contacts with the same email or phone number,
        and return all connected contacts.

        :param identity_request: IdentityRequestModel
        :return: all_related_contacts: Contact[]
    """

    queue = deque([(identity_request.email, identity_request.phoneNumber)])
    visited, all_related_contacts = set(), list()

    while queue:
        current_email, current_phone_number = queue.popleft()
        contacts = Contact.query.filter(
            or_(Contact.email == current_email, Contact.phoneNumber == current_phone_number)).all()

        for contact in contacts:
            if contact.id not in visited:
                visited.add(contact.id)
                all_related_contacts.append(contact)
                queue.append((contact.email, contact.phoneNumber))

    return all_related_contacts
