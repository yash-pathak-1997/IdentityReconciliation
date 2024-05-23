from sqlalchemy import or_
from entity import Contact
from model import IdentityRequestModel


def identity_dao(identity_request):
    # Extract email and phoneNumber from the IdentityRequestModel
    email = identity_request.email
    phoneNumber = identity_request.phoneNumber

    # Query the Contact entity for objects with the same email or phoneNumber
    contacts = Contact.query.filter(or_(Contact.email == email, Contact.phoneNumber == phoneNumber)).all()

    return contacts
