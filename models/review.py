from models.base_model import BaseModel

class Review(BaseModel):
    """Review class inherits from BaseModel"""
    place_id = ""  # Will be the Place.id
    user_id = ""  # Will be the User.id
    text = ""

