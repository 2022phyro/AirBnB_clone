#!/usr/bin/python3
"""The HBNB console"""
import cmd
from models.base_model import BaseModel
from models.review import Review

from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from models.user import User
from models import storage
import re


class HBNBCommand(cmd.Cmd):
    """This defines the structure of our AirBnB clone interpreter
    It has the attributes:
        prompt: the prompt (hbnb)
        classes: a dictionary of all our classes"""
    prompt = '(hbnb)'
    classes = {'BaseModel': BaseModel, "Review": Review, "Amenity": Amenity,
               "User": User, "Place": Place, "City": City, "State": State}

    def do_quit(self, value):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, value):
        """EOF signal to exit the program"""
        print("")
        return True

    def emptyline(self):
        """When encountering an empty line, do nothing"""
        pass

    def do_create(self, value):
        """Creates a new class value and prints out its id
        Usage: create <classname>"""
        if not value:
            print('** class name missing **')
        elif value not in self.classes.keys():
            print("** class doesn't exist **")
        else:
            new = self.classes[value]()
            new.save()
            print(new.id)

    def do_all(self, value):
        """It shows all created instances of the class
    Usage: all <classname>
               This will show all instancces of the specified class
        all
               This will show al created instances
        """
        line = value.split()
        if not line:
            end = [str(item) for item in storage.all().values()]
            print(end)
        elif line[0] not in self.classes.keys():
            print("** class doesn't exist **")
        else:
            end = [str(item) for item in storage.all().values()
                   if item.to_dict()['__class__'] == line[0]]
            print(end)

    def count(self, value):
        line = value.split()
        if line[1] not in self.classes.keys():
            print("** class doesn't exist **")
        else:
            i = 0
            for item in storage.all().values():
                if item.to_dict()['__class__'] == line[1]:
                    i += 1
            print(i)

    def do_show(self, value):
        """Shows all instances of a particular class
        Usage: show <classname> <object id>
            """
        line = value.split()
        if not line:
            print("** class name missing **")
        elif line[0] not in self.classes.keys():
            print("** class doesn't exist **")
        elif len(line) < 2:
            print("** instance id missing **")
        else:
            key = f"{line[0]}.{line[1]}"
            try:
                print(storage.all()[key])
            except KeyError:
                print("** no instance found **")

    def do_destroy(self, value):
        """Deletes the specified object
        Usage destroy <class name> <id>"""
        line = value.split()
        if not line:
            print("** class name missing **")
        elif line[0] not in self.classes.keys():
            print("** class doesn't exist **")
        elif len(line) < 2:
            print("** instance id missing **")
        else:
            key = f"{line[0]}.{line[1]}"
            try:
                del storage.all()[key]
                storage.save()
            except KeyError:
                print("** no instance found **")

    def do_update(self, value):
        """Update the specified object
        Usage: update <class name> <id> <attribute> <value>"""
        line = value.split()
        if len(line) >= 2:
            key = f"{line[0]}.{line[1]}"
        if not line:
            print("** class name missing **")
        elif line[0] not in self.classes.keys():
            print("** class doesn't exist **")
        elif len(line) < 2:
            print("** instance id missing **")
        elif key not in storage.all().keys():
            print("** no instance found **")
        elif len(line) < 3:
            print("** attribute name missing **")
        elif len(line) < 4:
            print("** value missing **")
        else:
            storage.all()[key].__dict__.update({line[2]: line[3]})
            storage.save()

    def precmd(self, line):
        ac = r"^\S+\.(all)|(count)\(\)$"
        # val = re.findall(, line.strip())
        ma = r"^\S+\.(show)|(destroy)\(\S*\)$"
        up = r"^\S+\.update\(.*\)$"
        # all_regex = [ac, ma]
        # ma = r"^\S+\.show\(\S*\)$"
        val = re.findall(ma, line.strip())
        # val = re.findall("^\S+\.\w+\(.*\)$", line.strip())
        if val:
            command = re.split(r"[\s()\"\'.,]", line)
            temp = command[1]
            command[1] = command[0]
            command[0] = temp
            print(val)
            end = " ".join(command).strip()
            if command[0] == 'count':
                self.count(end)
                return ""
            else:

                return end
        return line


if __name__ == '__main__':
    HBNBCommand().cmdloop()
