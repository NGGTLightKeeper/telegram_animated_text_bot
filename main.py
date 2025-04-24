import argparse
import threading
import subprocess

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent

def runserver():
    subprocess.call(["python", str(BASE_DIR) + "/bot.py"])

def makemigrations():
    subprocess.call(["python", str(BASE_DIR) + "/manage.py", "makemigrations"])

def migrate():
    subprocess.call(["python", str(BASE_DIR) + "/manage.py", "migrate"])

mess_help = '''
Available commands:
    runserver
    makemigrations
    migrate
    help
'''
mess_error = '''
Command error:
    Unknown command: '{command}'
    Usage command 'help' to view available commands
'''

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', type=str)
    command = parser.parse_args().command

    if command == 'runserver':
        thread1 = threading.Thread(target=runserver)

        thread1.start()
        thread1.join()

    elif command == 'makemigrations':
        print(f"Running command: {command}")
        makemigrations()

    elif command == 'migrate':
        print(f"Running command: {command}")
        migrate()

    elif command == 'help':
        print(mess_help)
    else:
        print(mess_error)

if __name__ == '__main__':
    main()
