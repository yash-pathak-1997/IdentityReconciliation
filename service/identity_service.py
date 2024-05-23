from dao import identity_dao
from model import IdentityRequestModel


def identity_service(identity_request: IdentityRequestModel):

    # DAO Call
    contacts = identity_dao(identity_request)

    # Business Logic - Extract emails, phone numbers, and secondary contact IDs
    emails = []
    phone_numbers = []
    secondary_contact_ids = []
    primary_contact_id = ""
    for contact in contacts:
        if contact.linkPrecedence == "primary":
            primary_contact_id = contact.id

    for contact in contacts:
        emails.append(contact.email)
        phone_numbers.append(contact.phoneNumber)
        if contact.id != primary_contact_id:
            secondary_contact_ids.append(contact.id)

    # Create the response
    response = {
        'contact': {
            'primaryContactId': primary_contact_id,
            'emails': emails,
            'phoneNumbers': list(set(phone_numbers)),
            'secondaryContactIds': secondary_contact_ids
        }
    }

    return response
