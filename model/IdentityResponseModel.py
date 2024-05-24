# Define the Identity API Response model class
class IdentityResponseModel:
    def __init__(self):
        self.primaryContactId = None
        self.emails = []
        self.phoneNumbers = []
        self.secondaryContactIds = []

    def to_dict(self):
        return {
            "contact": {
                'primaryContactId': self.primaryContactId,
                'emails': self.emails,
                'phoneNumbers': self.phoneNumbers,
                'secondaryContactIds': self.secondaryContactIds
            }
        }
