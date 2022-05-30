import os
import sys

from django.core.management import execute_from_command_line

MODULE_NAME = "django_poetry_example"


def _execute(*sys_args):
    """fiddles around with the sys and os.path before calling the django command."""
    root = os.path.join(os.getcwd(), MODULE_NAME)
    sys.path.insert(0, root)
    os.chdir(root)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
    sys.argv = sys_args
    execute_from_command_line(sys.argv)


def run_server():
    """Run django build in server for local development"""
    # we need to overwrite the original sys.argv because of the
    # auto reload feature
    _execute("manage.py", "runserver", "8800")


def manage():
    _execute("manage.py", *sys.argv[1:])


def shell_plus():
    _execute("manage.py", "shell_plus", *sys.argv[1:])
