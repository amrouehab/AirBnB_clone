#!/usr/bin/env python3

import cmd
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

class HBNBCommand(cmd.Cmd):
    """Command interpreter"""

    prompt = "(hbnb) "
    classes = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review,
    }

    def do_create(self, args):
        """Create a new instance of a class"""
        if not args:
            print("** class name missing **")
            return
        if args not in self.classes:
            print("** class doesn't exist **")
            return
        new_instance = self.classes[args]()
        new_instance.save()
        print(new_instance.id)

    def do_show(self, args):
        """Show the string representation of an instance"""
        tokens = args.split()
        if not tokens:
            print("** class name missing **")
            return
        if tokens[0] not in self.classes:
            print("** class doesn't exist **")
            return
        if len(tokens) < 2:
            print("** instance id missing **")
            return
        key = f"{tokens[0]}.{tokens[1]}"
        if key not in storage.all():
            print("** no instance found **")
            return
        print(storage.all()[key])

    def do_destroy(self, args):
        """Destroy an instance"""
        tokens = args.split()
        if not tokens:
            print("** class name missing **")
            return
        if tokens[0] not in self.classes:
            print("** class doesn't exist **")
            return
        if len(tokens) < 2:
            print("** instance id missing **")
            return
        key = f"{tokens[0]}.{tokens[1]}"
        if key not in storage.all():
            print("** no instance found **")
            return
        del storage.all()[key]
        storage.save()

    def do_all(self, args):
        """Show all instances or instances of a specific class"""
        if args and args not in self.classes:
            print("** class doesn't exist **")
            return
        objects = storage.all()
        result = []
        for key, obj in objects.items():
            if not args or key.startswith(args):
                result.append(str(obj))
        print(result)

    def do_update(self, args):
        """Update an instance"""
        tokens = args.split()
        if not tokens:
            print("** class name missing **")
            return
        if tokens[0] not in self.classes:
            print("** class doesn't exist **")
            return
        if len(tokens) < 2:
            print("** instance id missing **")
            return
        key = f"{tokens[0]}.{tokens[1]}"
        if key not in storage.all():
            print("** no instance found **")
            return
        if len(tokens) < 3:
            print("** attribute name missing **")
            return
        if len(tokens) < 4:
            print("** value missing **")
            return
        obj = storage.all()[key]
        attr_name = tokens[2]
        attr_value = eval(tokens[3])  # Safely cast to correct type
        setattr(obj, attr_name, attr_value)
        obj.save()

    def do_quit(self, args):
        """Quit the command interpreter"""
        return True

    def do_EOF(self, args):
        """Quit the command interpreter with EOF"""
        print()
        return True

if __name__ == "__main__":
    HBNBCommand().cmdloop()

