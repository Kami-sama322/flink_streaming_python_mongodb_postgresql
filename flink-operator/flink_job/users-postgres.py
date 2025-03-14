import logging
import sys
from random import choice

from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import DataTypes, StreamTableEnvironment
from pyflink.table.expressions import col
from pyflink.table.udf import udf

logger = logging.getLogger(__name__)


@udf(result_type=DataTypes.BOOLEAN())
def check_valid(name: str, surname: str) -> bool:
    """
        Some validation logic + logging for example
    """
    pool = [True, False]
    validation_res = choice(pool)
    msg = f'{name} {surname} is valid' if validation_res \
        else f'{name} {surname} is not valid'
    logger.info(msg)
    return validation_res


def main():
    # Base config
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(1)

    table_env = StreamTableEnvironment.create(stream_execution_environment=env)

    # Set source from MongoDB collection
    table_env.execute_sql("""
    CREATE TABLE users_mongo (
        _id STRING,
        service STRING,
        name STRING,
        surname STRING,
        age INT,
        PRIMARY KEY (_id) NOT ENFORCED
    ) WITH (
        'connector' = 'mongodb-cdc',
        'database' = 'database',
        'collection' = 'users',
        'hosts' = 'mongodb-headless.mongodb.svc.cluster.local:27017'
    )
    """)

    # Set temp table for processed data
    table_env.create_temporary_view(
        'processed_data',
        table_env.from_path('users_mongo')
        .select(
            col('_id'),
            col('service'),
            col('name'),
            col('surname'),
            col('age'),
            check_valid(col('name'), col('surname')).alias('is_valid')
        )
    )

    # Set sink PostgreSQL table
    table_env.execute_sql("""
    CREATE TABLE users_postgres (
        _id STRING,
        service STRING,
        name STRING,
        surname STRING,
        age INT,
        is_valid BOOLEAN,
        PRIMARY KEY (_id) NOT ENFORCED
    ) WITH (
        'connector' = 'jdbc',
        'driver' = 'org.postgresql.Driver',
        'url' = 'jdbc:postgresql://postgresql-clusterip.postgresql.svc.cluster.local:5432/mydb',
        'table-name' = 'users_postgres',
        'username' = 'user',
        'password' = 'password'
    )
    """)

    # Insert data from MongoDB to PostgreSQL
    table_env.execute_sql("""
        INSERT INTO users_postgres
        SELECT * FROM processed_data
        WHERE age BETWEEN 18 AND 65
    """)


if __name__ == '__main__':
   logging.basicConfig(
       stream=sys.stdout,
       level=logging.INFO,
       format="%(message)s"
    )
   main()
