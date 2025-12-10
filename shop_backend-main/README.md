1. cd to shop_backend-main directory
2. if you want to have seperate virtual enviroment run : `python -m venv .venv`
3. then run `.venv\Scripts\activate' to activate venv
4. if you dont need a venv skip steps 2 and 3
5. Run `pip install -r requirements.txt` 
6. Finally run `python manage.py runserver`
7. as our db is sqlite you won't need to run migration commands (this will changed later on to mysql)
8. if you want to start from beginning, just delete the sqlite file , then run `python manage.py migrate`
9. some static migrations were created to populate site with some inistial data. you can find them at site_module/migrations
10. to create initial superuser just run `python manage.py create_superuser_from_file` this will create admin with creds from 
a json file inside site_module/initial_data/superuser.json
11. the username and password are admin and admin123
12. there you will also find other static files for initial population