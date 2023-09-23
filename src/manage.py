#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys 
from django.apps import apps
def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LPRS_Core.settings')
    try:
        from django.core.management import execute_from_command_line
        # try:
        #     print(apps.check_apps_ready())
        # except:
        #     from django.core.exceptions import AppRegistryNotReady
        #     print("WTF what are you doing")
        #     raise AppRegistryNotReady("Apps aren't loaded yet.")
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
