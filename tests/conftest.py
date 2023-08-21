import os
from typing import Any, Generator

import pytest
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.db.base import get_session
from app.main import get_application
from app.migrations.models.base_model import BareBaseModel  # noqa
from app.storage.fs_handler import FsHandler
from app.storage.minio_handler import MinioHandler

load_dotenv(verbose=True)

SQLALCHEMY_DATABASE_URL = os.getenv(
    'SQL_DATABASE_URL_TEST', 'sqlite:///./test.db?check_same_thread=False')

engine = create_engine(
    url=SQLALCHEMY_DATABASE_URL, pool_pre_ping=True, future=True,
)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, 'test_outcome', rep)


@pytest.fixture(autouse=True)
def app() -> Generator[FastAPI, Any, None]:
    """
    Create a fresh database on each test case.
    """
    BareBaseModel.metadata.create_all(engine)  # Create the tables.
    query = ["SET FOREIGN_KEY_CHECKS = 0;"]
    for tbl in reversed(BareBaseModel.metadata.sorted_tables):
        query.append(f"DELETE FROM `{tbl}` where 1 = 1;")
    query.append("SET FOREIGN_KEY_CHECKS = 1;")
    query_str = "\n".join(query)

    session = TestingSessionLocal(bind=engine.connect())
    session.execute(text(query_str))
    session.commit()
    _app = get_application()
    yield _app
    # BareBaseModel.metadata.drop_all(engine)


@pytest.fixture
def db_session(app: FastAPI) -> Generator[TestingSessionLocal, Any, None]:
    """
    Creates a fresh sqlalchemy session for each test that operates in a
    transaction. The transaction is rolled back at the end of each test ensuring
    a clean state.
    """

    # connect to the database
    connection = engine.connect()
    # begin a non-ORM transaction
    # transaction = connection.begin()
    # bind an individual Session to the connection
    session = TestingSessionLocal(bind=connection)
    yield session  # use the session in tests.
    session.close()
    # rollback - everything that happened with the
    # Session above (including calls to commit())
    # is rolled back.
    # transaction.rollback()
    # return connection to the Engine
    connection.close()


def get_test_db():
    try:
        yield db_session
    finally:
        pass


@pytest.fixture()
def client(app: FastAPI, db_session: TestingSessionLocal) -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_session] = _get_test_db
    app.dependency_overrides[MinioHandler] = FsHandler
    with TestClient(app) as client:
        yield client


@pytest.mark.usefixtures('app_class')
class APITestCase:

    def set_permanent_header(self, client: TestClient, key: str, value: str):
        client.headers.update({str(key): str(value)})


@pytest.fixture
def app_class(request, app):
    if request.cls is not None:
        request.cls.app = app


"""
available fixtures:
    _session_faker, anyio_backend, anyio_backend_name, anyio_backend_options, app,
    app_class, cache, capfd, capfdbinary, caplog, capsys, capsysbinary, client, db_session,
    doctest_namespace, faker, monkeypatch, pytestconfig, record_property, record_testsuite_property,
    record_xml_attribute, recwarn, tmp_path, tmp_path_factory, tmpdir, tmpdir_factory
"""


@pytest.mark.usefixtures('each_test_case', 'each_test_suite')
class Jira:
    pass
