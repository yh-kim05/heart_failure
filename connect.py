import psycopg2

conn = psycopg2.connect(
    host="ruby.db.elephantsql.com",
    database="ygxgjydv",
    user="ygxgjydv",
    password="8XoBM50c3mG-pVuMSbZ0eHYemc6-ZEXp")

cur = conn.cursor()

cur.execute("""
    DROP TABLE IF EXISTS heart;
    CREATE TABLE heart (
        Age INT,
        Sex VARCHAR(5),
        ChestPain VARCHAR(5),
        RestingBP INT,
        Cholesterol INT,
        FastingBS INT,
        RestingECG VARCHAR(30),
        MaxHR INT,
        ExerciseAngina VARCHAR(30),
        Oldpeak FLOAT,
        ST_slope VARCHAR(30),
        Heartdisease INT
    )"""
)
## column name 도 함께 복사 되어서 int 가 오류난다. -> HEADER 로 해결

conn.commit()

data = """
    COPY heart FROM STDIN DELIMITER ',' CSV HEADER; 
"""

with open('/Users/yunheekim/codestates/Section3/project3/heart_900.csv', 'r') as raw_df:
    cur.copy_expert(data, raw_df)

conn.commit()

conn.close()

## csv -> postgreSQL DB 업로드 완료!!