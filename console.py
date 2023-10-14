#!/usr/bin/python3
"""contains the entry point of the command interpreter"""

import json
import re
import cmd
from models import storage
from models.base_model import BaseModel
from models.state import State
from models.user import User
from models.review import Review
from models.place import Place
from models.amenity import Amenity
from models.city import City


def parse(arg):
    """split argument"""
    return arg.split()


class HBNBCommand(cmd.Cmd):
    """class definition"""
    prompt = "(hbnb)"
    __classes = {
            "BaseModel",
            "State",
            "User",
            "City",
            "Amenity",
            "Place",
            "Review"
            }

    def default(self, line):
        argdict = {
            "all": self.do_all,
            "count": self.do_count,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "update": self.do_update
        }
        parts = line.strip().split('(')
        if len(parts) == 2:
            class_method_part, args_part = parts[0], parts[1][:-1]
            class_name, method_name = class_method_part.split('.')
            args = args_part.split(', ')
            if method_name in argdict:
                if method_name == 'update':
                    if args[1].startswith('"'):
                        a = ' '.join(args)
                        args_list = [arg.strip(',"') for arg in a.split(' ')]
                        id_now = args_list[0]
                        a = args_list[1]
                        v = args_list[2]
                        argdict[method_name](f"{class_name} {id_now} {a} {v}")
                    else:
                        arg1 = ','.join(args)
                        arg1_split = arg1.split('{')
                        id_now = arg1_split[0]
                        id_1 = id_now.strip('" ')
                        id_0 = id_1.replace('"', '', 1)
                        i = id_0.replace(',', '', 1)
                        dictionary_str = '{' + arg1_split[1]
                        dictionary = eval(dictionary_str)
                        for key, value in dictionary.items():
                            v = str(value)
                            argdict[method_name](f"{class_name} {i} {key} {v}")
                else:
                    arg1 = args[0].strip('"')
                    argdict[method_name](f"{class_name} {arg1}")
            else:
                print("** class doesn't exist **")
        else:
            print("Unknown syntax:", line)

    def do_quit(self, arg):
        """to exit the program"""
        return True

    def do_EOF(self, arg):
        """to exit the program"""
        print("")
        return True

    def emptyline(self):
        """shouldn’t execute anything"""
        pass

    def do_create(self, arg):
        """
        Creates a new instance of BaseModel,
        saves it (to the JSON file) and prints the id
        """
        line = parse(arg)
        if len(line) == 0:
            print("** class name missing **")
        elif line[0] not in self.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(line[0])().id)
            storage.save()

    def do_show(self, arg):
        """Prints the string representation of an instance
        based on the class name and id
        """
        arguments = parse(arg)
        """Get all instances from the storage"""
        all_instances = storage.all()
        """Check if the class name and instance ID are provided"""
        if len(arguments) < 2:
            return
        class_name = arguments[0]
        instance_id = arguments[1]
        """Check if the provided class name is valid"""
        if class_name not in self.__classes:
            print("** class doesn't exist **")
            return
        """Check if the instance with the given class name and ID exists"""
        instance_key = "{}.{}".format(class_name, instance_id)
        if instance_key not in all_instances:
            print("** no instance found **")
            print("{}.{}".format(class_name, instance_id))
            return

        instance = all_instances[instance_key]
        print(instance)

    def do_all(self, arg):
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects."""
        line = parse(arg)
        if len(line) > 0 and line[0] not in self.__classes:
            print("** class doesn't exist **")
            """checks if the class given is present"""
        else:
            instance = []
            for obj in storage.all().values():
                if len(line) == 0:
                    instance.append(obj.__str__())
                elif len(line) > 0 and line[0] == obj.__class__.__name__:
                    instance.append(obj.__str__())

            print(instance)

    def do_count(self, arg):
        """ retrieve all instances of a class"""
        line = parse(arg)
        if len(line) == 0:
            print("** class name missing **")
        elif len(line) > 0 and line[0] not in self.__classes:
            print("** class doesn't exist **")
        else:
            count = 0
            for obj in storage.all():
                if len(line) > 0 and line[0] == obj.__class__.__name__:
                    count += 1
                    """checks if the current obj in the loop is the
                    provided class then it adds it to ount"""
            print(count)

    def do_destroy(self, arg):
        """
        Deletes an instance based on the class name and id
        """
        line = parse(arg)
        od = storage.all()

        if len(line) == 0:
            print("** class name missing **")
        elif len(line) == 1:
            print("** instance id missing **")
        else:
            class_name = line[0].split('(')[0]
        if class_name not in self.__classes:
            print("** class doesn't exist **")
        else:
            instance_id = line[1]
            instance_key = "{}.{}".format(class_name, instance_id)
            if instance_key not in od:
                print("** no instance found **")
            else:
                del od[instance_key]
                storage.save()

    def do_update(self, arg):
        """
        Updates an instance based on the class name
        and id by adding or updating attribute
        """
        line = parse(arg)
        od = storage.all()

        if len(line) == 0:
            print("** class name missing **")
            return False
        if line[0] not in self.__classes:
            print("** class doesn't exist **")
            return False
        if len(line) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(line[0], line[1]) not in od.keys():
            print("** no instance found **")
            return False
        if len(line) == 2:
            print("** attribute name missing **")
            return False
        if len(line) == 3 and not isinstance(eval(line[2]), dict):
            print("** value missing **")
            return False
        if len(line) == 4:
            obj = od["{}.{}".format(line[0], line[1])]
            if line[2] in obj.__class__.__dict__.keys():
                vlt = type(obj.__class__.__dict__[line[2]])
                obj.__dict__[line[2]] = vlt(line[3])
            else:
                obj.__dict__[line[2]] = line[3]
        elif isinstance(eval(line[2]), dict):
            obj = od["{}.{}".format(line[0], line[1])]
            for w, z in eval(line[2]).items():
                if (w in obj.__class.__dict__.keys() and
                        type(obj.__class.__dict__[w]) in {str, int, float}):
                    vlt = type(obj.__class.__dict__[w])
                    obj.__dict__[w] = vlt(z)
                else:
                    obj.__dict__[w] = z
            storage.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
