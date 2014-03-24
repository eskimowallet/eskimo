from sys import stdout

def prnt(printstring, silent=False):
    """
    STDOUT console printing with an option to disable
    """
    if not silent:
        stdout.write(printstring)