# Define the Contact model class
class ContactModel:
    def __init__(self, phoneNumber, email, linkedId=None, linkPrecedence=None):
        self.phoneNumber = phoneNumber
        self.email = email
        self.linkedId = linkedId
        self.linkPrecedence = linkPrecedence
