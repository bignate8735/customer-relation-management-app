Local Docker → Nginx + Gunicorn → .env config → Staging Environment → GitHub Repo + Actions → Secure + CI/CD → Cloud Deployment


docker pull nathansack/crm-web:latest

docker run -d --name crm-test nathansack/crm-web:latest
docker logs crm-test > test.txt 2>&1

DOCKER EXEC
docker compose exec web python manage.py migrate
docker compose exec web bash
python manage.py createsuperuser


POSTGRES
Command         Description

\1 or \list      List all databases
\c <dbname>      Connect to a specific database
\dt              List tables in the current DB
\du              List roles (users)
\q                Quit



MYSQL
mysql -uroot -p<password> -h db
Here:
	•	-u is the username (root)
	•	-p<password> is the password
	•	-h db assumes your MySQL service is named db in your Docker Compose file

🔁 If your MySQL service has a different name, replace db with that service name.

Task                           Command

Switch to a database        USE <dbname>;

List tables in current DB   SHOW TABLES;

Describe table structure    DESCRIBE <table>;

Exit MySQL                  EXIT; or QUIT;



