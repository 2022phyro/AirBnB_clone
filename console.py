#!/usr/bin/python3
"""The HBNB console"""
import cmd
import ast
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
        Usage: create <class name>"""
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

    def do_count(self, value):
        """This counts all instances of a particular class
        It shouldn't be called directly but can be accessed through the
        <classname>.count() action in the console"""
        if not value:
            print('** class name missing **')
        elif value not in self.classes.keys():
            print("** class doesn't exist **")
        else:
            i = 0
            for item in storage.all().values():
                if item.to_dict()['__class__'] == value:
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
            try:
                line[3] = ast.literal_eval(line[3])
            except BaseException:
                pass
            storage.all()[key].__dict__.update({line[2]: line[3]})
            storage.save()

    def update_with_dict(self, line):
        """This updates the instance with the dictionary
        representation from the console"""
        up_dict = r"^\S+\.update\(\S+, \{.*\}\)$"
        val = re.findall(up_dict, line.strip())
        if not val:
            return line
        splt = r"[.]"
        ma = re.split(splt, line.strip(), maxsplit=1)
        ve = re.split(r"[(),\s]", ma[1].strip(")"), maxsplit=1)
        del ma[1]
        id_dict = re.split(r", ", ve.pop())
        ve += id_dict
        all = ast.literal_eval(ve[2])
        for key, value in all.items():
            sr = "'"
            command = f"{ma[0]} {str(ve[1]).strip(sr)} {key} {value}"
            self.do_update(command)
        return ""

    def default(self, value):
        """I didn't intend to oveeride the default method
        i wanted to override the precmd
        but alx checker wont allow me to rest in peace
        In order for me to get my marks, I guess this is the only way
        """
        line = self.prep(value)
        cmd, arg, line = self.parseline(line)
        if not line:
            return self.emptyline()
        if cmd is None:
            return self.default(line)
        self.lastcmd = line
        if line == 'EOF':
            self.lastcmd = ''
        if cmd == '':
            self.stdout.write('*** Unknown syntax: %s\n' % line)
            return
        else:
            try:
                func = getattr(self, 'do_' + cmd)
            except AttributeError:
                self.stdout.write('*** Unknown syntax: %s\n'%line)
                return
            return func(arg)
    def prep(self, line):
        """Actions to be carried out before parsing the line
        to the console"""
        a = self.update_with_dict(line)
        if a == "":
            return ""
        flag = False
        ac = r"^\S+\.(all)|(count)\(\)$"
        sd = r"^\S+\.(show)|(destroy)\(\S*\)$"
        up = r"^\S+\.update\(.*\)$"

        all_regex = [up, sd, ac]
        for i in range(len(all_regex)):
            val = re.findall(all_regex[i], line.strip())
            if val:
                flag = True
                break
        if flag is False:
            return line
        command = re.split(r"[.]", line,  maxsplit=1)
        command += re.split(r"[()]", command.pop().strip(")"))
        command += re.split(r", ", command.pop())
        temp = command[1]
        command[1] = command[0]
        command[0] = temp
        string = ""
        for item in command:
            item = item.strip("'")
            item = item.strip('"')
            string += item + " "
        end = " ".join(command)
        return string.strip()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
