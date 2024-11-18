import json

class FileStorage:
    """Serializes instances to a JSON file & deserializes JSON file to instances"""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the dictionary of objects"""
        return self.__objects

    def new(self, obj):
        """Adds a new object to the dictionary"""
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file"""
        json_objects = {key: obj.to_dict() for key, obj in self.__objects.items()}
        with open(self.__file_path, "w") as f:
            json.dump(json_objects, f)

    def reload(self):
        """Deserializes the JSON file to __objects if the file exists"""
        try:
            with open(self.__file_path, "r") as f:
                loaded_data = json.load(f)
                from models.base_model import BaseModel
                from models.user import User
                from models.state import State
                from models.city import City
                from models.amenity import Amenity
                from models.place import Place
                from models.review import Review

                # Mapping class names to classes
                classes = {
                    "BaseModel": BaseModel,
                    "User": User,
                    "State": State,
                    "City": City,
                    "Amenity": Amenity,
                    "Place": Place,
                    "Review": Review,
                }

                for key, value in loaded_data.items():
                    cls_name = value["__class__"]
                    cls = classes[cls_name]
                    self.__objects[key] = cls(**value)
        except FileNotFoundError:
            pass

