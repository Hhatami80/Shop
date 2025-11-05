1. cd to shop_backend-main directory
2. if you want to have seperate virtual enviroment run : `python -m venv .venv`
3. then run `.venv\Scripts\activate' to activate venv
4. if you dont need a venv skip steps 2 and 3
5. Run `pip install -r requirements.txt` 
6. Finally run `python manage.py runserver`
7. as our db is sqlite you won't need to run migration commands (this will changed later on to mysql)