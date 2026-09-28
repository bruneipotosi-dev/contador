-- 1. la estructura (lo que antes hacía init_db)
CREATE TABLE visitas (id INTEGER PRIMARY KEY, total INTEGER NOT NULL);
INSERT INTO visitas (id, total) VALUES (1, 0);

-- 2. el usuario de la app, con la contraseña de su secret
\set app_pw `cat /run/secrets/db_app_password`
CREATE USER contador_app PASSWORD :'app_pw';

-- 3. los permisos mínimos
GRANT SELECT, UPDATE ON visitas TO contador_app;