"""
Database Connector Module

This module provides a connection to the database, as well as methods to execute queries with error catching.

Authors:
    Aidan Queng (jaidanqueng@gmail.com), Texas A&M University
    Michael Orgunov (michaelorgunov@gmail.com), Texas A&M University

Date:
    November 2024
"""

from os import getenv
from sqlalchemy import create_engine, Engine, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from . import queries as qu
import logging
import time


# Database connection URI
PG_DB_URI = "postgresql://{0}:{1}@{2}:{3}/{4}".format(
    getenv("POSTGRES_USER", "test_user"),
    getenv("POSTGRES_PASSWORD", None),
    getenv("POSTGRES_HOST", "localhost"),
    getenv("POSTGRES_PORT", 5432),
    getenv("POSTGRES_DB", "test")
)

logging.basicConfig(level=logging.DEBUG)


class DBConnector:
    """
    DBConnector is responsible for managing the connection and interaction with a database
    using SQLAlchemy. It provides methods to execute queries, handle transactions, and
    manage the database session lifecycle.

    Attributes:
    ----------
    engine : sqlalchemy.engine.Engine
        The SQLAlchemy engine that connects to the database.
    Session : sqlalchemy.orm.sessionmaker
        A configured session factory for creating new sessions.
    """

    def __init__(self):
        self.engine: Engine = create_engine(PG_DB_URI)
        self.Session: sessionmaker = sessionmaker(bind=self.engine)
        # If tables don't exist, initialize them
        self.initialize_db_with_retry()

    # Try to initialize the db 'max_retries' number of times with a delay between attempt of 'delay'.
    # If tables exist, quit
    def initialize_db_with_retry(self, max_retries=5, delay=2):
        """
        Attempts to initialize the database with schema.

        Args:
            max_retries (int, optional): Maximum number of retries. Defaults to 5.
            delay (int, optional): Delay between retries in seconds. Defaults to 2.
        """
        retries = 0
        while retries < max_retries:
            try:
                # Initial check of db tables
                tables = inspect(self.engine).get_table_names()
                logging.debug(f"Tables in database: {tables}")

                # If tables exist, quit
                if len(tables) > 0:
                    logging.info("Tables created successfully.")
                    return

                # If tables do not exist, attempt to create them
                logging.debug("Attempting to create tables...")
                self.execute_query(qu.create_tables)

                # Recheck if the tables now exist
                tables = inspect(self.engine).get_table_names()
                if len(tables) > 0:
                    logging.info("Tables created successfully.")
                    return
                else:
                    logging.warning(f"Attempt {retries + 1} failed: Tables still not created.")

            except OperationalError as e:
                # Connection failure (db most likely booting up)
                logging.error(f"Attempt {retries + 1} failed: {e}")
                retries += 1
                if retries >= max_retries:
                    logging.critical("Max retries reached. Could not connect to database.")
                    break
                logging.info(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            except SQLAlchemyError as e:
                # Handle other SQLAlchemy errors
                logging.error(f"SQLAlchemy error: {e}")
                retries += 1
                if retries >= max_retries:
                    logging.critical("Max retries reached. Could not perform the operation.")
                    break
                logging.info(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            except Exception as e:
                # Catch any unexpected errors
                logging.exception(f"Unexpected error: {e}")
                break
        else:
            logging.critical("Failed to initialize database after multiple retries.")

    def execute_query(self, query_func, *args, **kwargs):
        """
        Executes a query that will modify the database as a single transaction.

        Args:
            query_func (callable): The function that performs the query. It takes the session as
                the first argument, followed by any additional arguments.
            *args (tuple): Additional positional arguments to pass to `query_func`.
            **kwargs (dict): Additional keyword arguments to pass to `query_func`.

        Returns:
            None: Will output a debug or warning log
        """
        with self.Session() as session:
            session.begin()
            try:
                query_func(session, *args, **kwargs)
            except Exception as e:
                session.rollback()
                logging.warning(f"Could not execute query: {e}")
                logging.exception(e)
            else:
                session.commit()
                logging.debug("Executed query successfully.")

    def execute_query_readonly(self, query_func, *args, **kwargs):
        """
        Executes a query that will read the database.

        Args:
            query_func (callable): The function that performs the query. It takes the session as
                the first argument, followed by any additional arguments.

        Returns:
            Any: Passes the result of `query_func`
        """
        with self.Session() as session:
            try:
                result = query_func(session, *args, **kwargs)
            except Exception as e:
                logging.warning(f"Could not execute query: {e}")
                logging.exception(e)
                return None
            else:
                logging.debug("Executed query successfully.")
                return result


if __name__ == "__main__":
    conn = DBConnector()
