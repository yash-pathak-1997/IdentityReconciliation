import os
from dao import identity_dao
from model import IdentityRequestModel, IdentityResponseModel


def identity_service(identity_request: IdentityRequestModel):
    """
    Service layer of /identity endpoint

    :param identity_request: IdentityRequestModel
    :return: response: dict()
    """

    # DAO Layer Call
    contacts = identity_dao(identity_request)

    # Business Logic
    response_model = IdentityResponseModel()

    for contact in contacts:
        if contact.linkPrecedence == os.getenv('PRIMARY'):
            response_model.primaryContactId = int(contact.id)

    for contact in contacts:
        if contact.email:
            response_model.emails.append(contact.email)
        if contact.phoneNumber:
            response_model.phoneNumbers.append(contact.phoneNumber)
        if int(contact.id) != response_model.primaryContactId:
            response_model.secondaryContactIds.append(int(contact.id))

    # Convert the response model to a dictionary and then to JSON
    response = response_model.to_dict()
    return response
