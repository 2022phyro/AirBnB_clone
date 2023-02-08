#!/usr.bin.python3
import cmd
from models.base_model import BaseModel
from models import storage


class HBNBCommand(cmd.Cmd):
    prompt = '(hbnb) '
    classes = {'BaseModel': BaseModel}

    def do_quit(self, value):
        """Quit whenever someone press quit"""
        return True

    def do_EOF(self, value):
        """When EOf is encountered, return True and quit"""
        return True

    def emptyline(self):
        """When encountering an empty line, do nothing"""
        pass

    def do_create(self, value):
        """Creates a new class value
        BaseModel - Creates a new BaseModel Class"""
        if not value:
            print('** class name missing **')
        elif value not in self.classes.keys():
            print("** class doesn't exist **")
        else:
            new = self.classes[value]()

    def do_all(self, value):
        """It shows all created instances of the class"""
        line = value.split()
        if not line:
            for item in storage.all().values():
                print(item)
        elif line[0] not in self.classes.keys():
            print("** class doesn't exist **")
        else:
            for item in storage.all().values():
                if item.to_dict()['__class__'] == line[0]:
                    print(item)

    def do_show(self, value):
        """Shows all instances of a particular class"""
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


if __name__ == '__main__':
    HBNBCommand().cmdloop()
