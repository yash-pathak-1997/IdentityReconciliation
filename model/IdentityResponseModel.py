# Define the Identity API Response model class
class IdentityResponseModel:
    def __init__(self, primaryContactId, emails, phoneNumbers, secondaryContactIds):
        self.primaryContactId = primaryContactId
        self.emails = emails
        self.phoneNumbers = phoneNumbers
        self.secondaryContactIds = secondaryContactIds

    def to_dict(self):
        return {
            "contact": {
                'primaryContactId': self.primaryContactId,
                'emails': self.emails,
                'phoneNumbers': self.phoneNumbers,
                'secondaryContactIds': self.secondaryContactIds
            }
        }
