import os
import sys
import subprocess
from src.log.logger import logging

logger3 = logging.getLogger('Setup')
logger3.setLevel(logging.DEBUG)

class Setup_():
    def __init__(self, venv_name='.env', py_version=None):
        
        if py_version == None:
            py_version = self.get_version()
        
        if not os.path.exists(venv_name):  # Check if .env directory doesn't exist
            print(f"Current directory: {os.getcwd()}")
            logger3.info(f"Current directory: {os.getcwd()}")
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'virtualenv'])
                print("Virtualenv package installed successfully!")
                logger3.info("Virtualenv package installed successfully!")
            except subprocess.CalledProcessError as e:
                print(f"Virtualenv package installation failed, error: {e}")
                logger3.error(f"Virtualenv package installation failed, error: {e}")
                return  

            command = ['virtualenv', '-p', f'python{py_version}', venv_name]
            try:
                subprocess.check_call(command)
                logger3.info(f"Virtual environment '{venv_name}' created successfully!")
                print(f"Virtual environment '{venv_name}' created successfully!")
            except subprocess.CalledProcessError as e:
                print(f"Virtual environment creation failed, error: {e}")
                logger3.error(f"Virtual environment creation failed, error: {e}")
                return  # Stop execution if virtualenv creation fails

        activate_script = os.path.join(venv_name, 'Scripts', 'activate')  
        activate_command = [activate_script]

        try:
            subprocess.check_call(activate_command, shell=True)
            print(f"Virtual environment '{venv_name}' activated!")
            logger3.info(f"Virtual environment '{venv_name}' activated!")
        except subprocess.CalledProcessError as e:
            print(f"Failed to activate virtual environment '{venv_name}', error: {e}")
            logger3.error(f"Failed to activate virtual environment '{venv_name}', error: {e}")
            return

        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
            print("Requirements installed successfully!")
            logger3.info("Requirements installed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while installing requirements: {e}")
            logger3.warning(f"Error occurred while installing requirements: {e}")
    
    def get_version(self):
        try:
            version = sys.version_info
            return f'{version.major}.{version.minor}'
        except:
            logger3.critical('No python version found, Kindly download pyhon')
            print('No python version found, Kindly download pyhon')

if __name__ == "__main__":
    setup = Setup_('.venv')
    logger3.info('Setting up the environment')