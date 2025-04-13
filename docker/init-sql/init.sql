CREATE DATABASE mlflow_db;
CREATE USER mlflow_user WITH ENCRYPTED PASSWORD 'mlflow';
GRANT ALL PRIVILEGES ON DATABASE mlflow_db TO mlflow_user;

-- CREATE DATABASE mlops;
-- CREATE USER airbyte WITH ENCRYPTED PASSWORD 'airbyte';
-- GRANT ALL PRIVILEGES ON DATABASE mlops TO airbyte;
-- GRANT ALL ON SCHEMA public TO airbyte;
-- GRANT USAGE ON SCHEMA public TO airbyte;
-- ALTER DATABASE mlops OWNER TO airbyte;

CREATE DATABASE mlops;
CREATE USER "dodobeatle@gmail.com" WITH ENCRYPTED PASSWORD 'airbyte';
GRANT ALL PRIVILEGES ON DATABASE mlops TO "dodobeatle@gmail.com";
GRANT ALL ON SCHEMA public TO "dodobeatle@gmail.com";
GRANT USAGE ON SCHEMA public TO "dodobeatle@gmail.com";
ALTER DATABASE mlops OWNER TO "dodobeatle@gmail.com";

-- \du
