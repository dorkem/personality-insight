from snowflake.snowpark import Session
from dotenv import load_dotenv
import os
import snowflake_setup

# .env 파일 로드
load_dotenv(dotenv_path=".env")

# 세션 연결 설정
connection_parameters = {
    "account": os.getenv("SNOWFLAKE_ACCOUNT"),
    "user": os.getenv("SNOWFLAKE_USER"),
    "password": os.getenv("SNOWFLAKE_PASSWORD"),
    "role": os.getenv("SNOWFLAKE_ROLE"),
    "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
    "database": os.getenv("SNOWFLAKE_DATABASE"),
    "schema": os.getenv("SNOWFLAKE_SCHEMA")
}

session = Session.builder.configs(connection_parameters).create()

# 처음 한 번만 실행
snowflake_setup.initialize_snowflake_environment(session)

df = session.table("personality_survey")

df_pd = df.to_pandas()
