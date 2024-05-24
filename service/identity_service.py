import json
import os

from dao import identity_dao
from model import IdentityRequestModel, IdentityResponseModel


def identity_service(identity_request: IdentityRequestModel):

    # DAO Call
    contacts = identity_dao(identity_request)

    # Business Logic - Extract emails, phone numbers, and secondary contact IDs
    emails = []
    phone_numbers = []
    secondary_contact_ids = []
    primary_contact_id = ""

    for contact in contacts:
        if contact.linkPrecedence == os.getenv('PRIMARY'):
            primary_contact_id = contact.id

    for contact in contacts:
        emails.append(contact.email)
        phone_numbers.append(contact.phoneNumber)
        if contact.id != primary_contact_id:
            secondary_contact_ids.append(contact.id)

    # Create the response
    response_model = IdentityResponseModel(
        primaryContactId=primary_contact_id,
        emails=list(set(emails)),
        phoneNumbers=list(set(phone_numbers)),
        secondaryContactIds=secondary_contact_ids
    )

    # Convert the response model to a dictionary and then to JSON
    response = response_model.to_dict()
    return response
