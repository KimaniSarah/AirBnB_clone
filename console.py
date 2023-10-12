#!/usr/bin/python3
"""contains the entry point of the command interpreter"""

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
    def default(self, arg):
        """Default behavior for cmd module when input is invalid"""
        argdict = {
            "all": self.do_all,
            "destroy": self.do_destroy,
            "update": self.do_update
        }
        match = re.search(r"\.", arg)
        if match is not None:
            argl = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", argl[1])
            if match is not None:
                command = [argl[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in argdict.keys():
                    call = "{} {}".format(argl[0], command[1])
                    return argdict[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

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
        """
        Prints the string representation of an instance
        based on the class name and id
        """
        line = parse(arg)
        od = storage.all()
        if len(line) == 0:
            print("** class name missing **")
        elif line[0] not in self.__classes:
            print("** class doesn't exist **")
        elif len(line) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(line[0], line[1]) not in od:
            print("** no instance found **")
        else:
            print(od["{}.{}".format(line[0], line[1])])

    def do_all(self, arg):
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects."""
        line = parse(arg)
        if len(line) > 0 and line[0] not in self.__classes:
            print("** class doesn't exist **")
        else:
            instance = []
            for obj in storage.all().values():
                if len(line) == 0:
                    instance.append(obj.__str__())
                elif len(line) > 0 and line[0] == obj.__class__.__name__:
                    instance.append(obj.__str__())

            print(instance)

    def do_destroy(self, arg):
        """
        Deletes an instance based on the class name and id
        """

        line = parse(arg)
        od = storage.all()
        if len(line) == 0:
            print("** class name missing **")
        elif line[0] not in self.__classes:
            print("** class doesn't exist **")
        elif len(line) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(line[0], line[1]) not in od.keys():
            print("** no instance found **")
        else:
            del od["{}.{}".format(line[0], line[1])]
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
                if (w in obj.__class.__dict__.keys() and\
                        type(obj.__class.__dict__[w]) in {str, int, float}):
                    vlt = type(obj.__class.__dict__[w])
                    obj.__dict__[w] = vlt(z)
                else:
                    obj.__dict__[w] = z
            storage.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()

