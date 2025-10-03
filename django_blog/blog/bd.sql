-- in your terminal run: psql -U postgres
CREATE DATABASE django_blog_db;
CREATE USER bloguser WITH PASSWORD 'strongpassword';
GRANT ALL PRIVILEGES ON DATABASE django_blog_db TO bloguser;
\q
