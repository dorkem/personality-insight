from snowflake.snowpark import Session
from dotenv import load_dotenv
import os

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


session.sql("""
    CREATE OR REPLACE FILE FORMAT my_csv_format
    TYPE = 'CSV'
    FIELD_OPTIONALLY_ENCLOSED_BY = '"'
    SKIP_HEADER = 1
    FIELD_DELIMITER = ','
""").collect()

# session.sql("""
# CREATE OR REPLACE STORAGE INTEGRATION S3_INT
#   TYPE = EXTERNAL_STAGE
#   STORAGE_PROVIDER = S3
#   ENABLED = TRUE
#   STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::696051617446:role/snowflake_s3_access_role'
#   STORAGE_ALLOWED_LOCATIONS = ('s3://personality-insight-bucket/raw/'); 
# """).collect()

desc_result = session.sql("DESC INTEGRATION s3_int").collect()
for row in desc_result:
    print(row)

# session.sql("""
#     CREATE OR REPLACE TABLE personality_survey (
#         Time_spent_Alone FLOAT,
#         Stage_fear STRING,
#         Social_event_attendance FLOAT,
#         Going_outside FLOAT,
#         Drained_after_socializing STRING,
#         Friends_circle_size FLOAT,
#         Post_frequency FLOAT,
#         Personality STRING
#     )
# """).collect()

# session.sql(f"""
#     CREATE OR REPLACE STAGE my_s3_stage
#     URL='s3://personality-insight-bucket/raw/'
#     STORAGE_INTEGRATION = S3_INT
#     FILE_FORMAT = my_csv_format
# """).collect()
 
# # 2. S3에서 Snowflake 테이블로 데이터 복사
# session.sql("""
#     COPY INTO personality_survey
#     FROM @my_s3_stage/personality_datasert.csv
#     FILE_FORMAT = my_csv_format
# """).collect()

# # 3. 제대로 들어갔는지 확인
# df = session.table("personality_survey")
# df.show()