#!/usr/bin/python3
"""
Test script for BaseModel with dictionary serialization/deserialization.
"""

from models.base_model import BaseModel

# Create an instance of BaseModel
my_model = BaseModel()
my_model.name = "My_First_Model"
my_model.my_number = 89

# Print initial attributes
print(my_model.id)
print(my_model)
print(type(my_model.created_at))

print("--")

# Convert to dictionary
my_model_json = my_model.to_dict()
print(my_model_json)

# Print JSON representation
print("JSON of my_model:")
for key in my_model_json.keys():
    print("\t{}: ({}) - {}".format(key, type(my_model_json[key]), my_model_json[key]))

print("--")

# Recreate an instance from the dictionary
my_new_model = BaseModel(**my_model_json)

# Print recreated instance attributes
print(my_new_model.id)
print(my_new_model)
print(type(my_new_model.created_at))

print("--")

# Verify if the two instances are the same object
print(my_model is my_new_model)

