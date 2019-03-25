from dateutil.parser import parse


class Lead(object):

    def __init__(self, dct):
        """
        A class representing a lead.
        """
        self.id = dct["_id"]
        self.email = dct["email"]
        self.first_name = dct["firstName"]
        self.last_name = dct["lastName"]
        self.address = dct["address"]
        self.entry_date = dct["entryDate"]

    def to_dict(self):
        """
        Returns the lead as dictionary with the original keywords included in the json.
        """
        return {
            "_id": self.id,
            "email": self.email,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "address": self.address,
            "entryDate": self.entry_date
        }

    def datetime(self):
        return parse(self.entry_date)
