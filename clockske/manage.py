#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import subprocess
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clockske.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?") from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    # Execute the Tailwind CSS CLI command
    tailwind_command = [
        './tailwindcss',
        '-i',
        '/home/stewie/Clocks_Ke/clockske/static/css/input.css',
        '-o',
        '/home/stewie/Clocks_Ke/clockske/static/css/output.css',
    ]
    subprocess.Popen(tailwind_command)
    main()
