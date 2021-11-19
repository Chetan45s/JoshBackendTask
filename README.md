## Quick Start
Installation Steps for linux
```bash
git clone https://github.com/Chetan45s/JoshBackendTask.git
cd JoshBackendTask

virtualenv -p python3 venv                  # To create a virtual env
source venv/bin/activate                    # activate it

pip install -r requirements.txt             # installing all required libs

python manage.py crontab add                # adding cron jobs (if doesn't work please execute this line one more time)

python manage.py runserver # starts the server 
```
