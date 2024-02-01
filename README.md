#Launch Instructions

1. Install Python 3.10
2. Open terminal and enter `pip install -r requirements.txt`
3. Enter proper database configuration in settings.py
4. Run migrations with `python manage.py makemigrations` and `python manage.py migrate`.
5. Run development server with `python manage.py runserver`

#Entity Relationship Diagram
![alt text](ERD.png "ERD")

#API Doc
| Endpoint | Action | Description | Permission |
| --- | --- | ----------- | -- |
| admin | | The django admin panel | Superuser |
| accounts/auth/token/ | POST | send email and password to get token | Authenticated |
| accounts/auth/token/refresh/ | POST | send email and password to get token | Authenticated |
| accounts/users/ | GET,POST | GET: list all users POST: create user | Superuser |
| accounts/users/\<int:pk>/ | GET,POST,PUT,PATCH | CRUD on a single user | Superuser or Self
| restaurants/ | GET,POST | GET: list all POST: create | Superuser can create else Authenticated
| restaurants/\<int:pk>/ | GET,POST,PUT,PATCH | CRUD on a single restaurant | Superuser or restaurant Manager
| restaurants/\<int:rpk>/menu/ | GET,POST | GET: list all POST: create | Authenticated
| restaurants/menu/\<int:pk>/ | GET,POST,PUT,PATCH | CRUD on a single menu | Superuser or restaurant Manager
| restaurants/menu/\<int:menu_pk>/offers/ | GET,POST | GET: list all POST: create | Authenticated |
| restaurants/menu/\<int:menu_pk>/offers/\<int:pk>/ | GET,POST,PUT,PATCH | CRUD on a single offer item | Superuser or Manager |
| votes/ | GET,POST | GET: list all POST: create | Superuser can see all votes, Employees can only vote |
| votes/current_standings/ | GET | See today's top 3 voted menu | Authenticated |
| votes/<int:pk>/ | GET,POST,PUT,PATCH | CRUD on a single vote | Superuser or Self |
| votes/select_todays_winner/ | GET | Finalize today's winner | Superuser |
