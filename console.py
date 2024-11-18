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
import ast
import re

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

    def default(self, line):
        """Handle class name commands"""
        if '.' in line:
            class_name, command = line.split('.', 1)
            if command.startswith("count()"):
                self.do_count(class_name)
            elif command.startswith("show("):
                self.do_show_class(class_name, command)
            elif command.startswith("destroy("):
                self.do_destroy_class(class_name, command)
            elif command.startswith("update("):
                self.do_update_class(class_name, command)
            elif command.startswith("all()"):
                self.do_all_class(class_name)
            else:
                print(f"*** Unknown syntax: {line}")
        else:
            print(f"*** Unknown syntax: {line}")

    def do_count(self, class_name):
        """Count the number of instances of a class"""
        if class_name not in self.classes:
            print("** class doesn't exist **")
            return
        objects = storage.all()
        count = sum(1 for key in objects if key.startswith(class_name + '.'))
        print(count)

    def do_show_class(self, class_name, command):
        """Show the string representation of an instance based on class name and ID"""
        if class_name not in self.classes:
            print("** class doesn't exist **")
            return
        try:
            id_str = command[command.find('(') + 1:command.find(')')]
            id_str = id_str.strip('"').strip("'")
            key = f"{class_name}.{id_str}"
            if key not in storage.all():
                print("** no instance found **")
                return
            print(storage.all()[key])
        except Exception as e:
            print(f"*** Invalid syntax: {command}")

    def do_destroy_class(self, class_name, command):
        """Destroy an instance based on class name and ID"""
        if class_name not in self.classes:
            print("** class doesn't exist **")
            return
        try:
            id_str = command[command.find('(') + 1:command.find(')')]
            id_str = id_str.strip('"').strip("'")
            key = f"{class_name}.{id_str}"
            if key not in storage.all():
                print("** no instance found **")
                return
            del storage.all()[key]
            storage.save()
        except Exception as e:
            print(f"*** Invalid syntax: {command}")

    def do_update_class(self, class_name, command):
        """Update an instance based on class name, ID, attribute name, and attribute value"""
        if class_name not in self.classes:
            print("** class doesn't exist **")
            return
        try:
            # Use regex to parse the command string
            match = re.match(r"update\((.*?)\)", command)
            if not match:
                print(f"*** Invalid syntax: {command}")
                return
            args_str = match.group(1)
            args_list = args_str.split(',', 2)
            id_str = args_list[0].strip('"').strip("'")
            key = f"{class_name}.{id_str}"
            if key not in storage.all():
                print("** no instance found **")
                return
            obj = storage.all()[key]
            if len(args_list) == 3:
                attr_name = args_list[1].strip('"').strip("'")
                attr_value = eval(args_list[2].strip('"').strip("'"))
                setattr(obj, attr_name, attr_value)
            elif len(args_list) == 2:
                dict_str = args_list[1].strip('"').strip("'")
                update_dict = ast.literal_eval(dict_str)
                for attr_name, attr_value in update_dict.items():
                    setattr(obj, attr_name, attr_value)
            obj.save()
        except Exception as e:
            print(f"*** Invalid syntax: {command}")

    def do_all_class(self, class_name):
        """Retrieve all instances of a class by using: <class name>.all()"""
        if class_name not in self.classes:
            print("** class doesn't exist **")
            return
        objects = storage.all()
        result = [str(obj) for key, obj in objects.items() if key.startswith(class_name + '.')]
        print(result)

if __name__ == "__main__":
    HBNBCommand().cmdloop()
