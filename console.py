import cmd


class HBNBCommand(cmd.Cmd):
    """defines the structure of
    the holberton command interpreter
    Attributes:
        prompt (str): The command prompt
    """

    prompt = "(hbnb)"

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the prgram"""
        print("")
        return true

    def ignoreEmptyInput(self):
        """Do nothing about empty input"""
        pass


if __name__ == '__main__':
    HBNBCommand().cmdloop()
