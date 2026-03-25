from unittest.mock import MagicMock, patch

import pytest

from app import create_app


@pytest.fixture()
def app():
    app = create_app()
    app.config["TESTING"] = True
    return app


@pytest.fixture()
def client(app):
    return app.test_client()


def test_create_app_registers_expected_endpoints(app):
    """Ensure key endpoint names are still registered."""
    endpoint_names = {rule.endpoint for rule in app.url_map.iter_rules()}

    assert "index.index" in endpoint_names
    assert "invoice.invoice" in endpoint_names
    assert "customer.customer" in endpoint_names
    assert "product.product" in endpoint_names
    assert "search.search" in endpoint_names
    assert "index.set_language" in endpoint_names


def _make_mock_connection(fetchall_return=None):
    """Build a mock pymysql connection with a configurable cursor."""
    cursor = MagicMock()
    cursor.fetchall.return_value = fetchall_return or []
    connection = MagicMock()
    connection.cursor.return_value = cursor
    return connection


@pytest.mark.parametrize(
    "path",
    ["/", "/invoice", "/customer", "/product", "/search"],
)
def test_public_pages_return_200(client, path):
    """Validate public GET pages are reachable without a real DB."""
    mock_conn = _make_mock_connection()
    patch_targets = [
        "app.routes.product.get_db_connection",
        "app.routes.customer.get_db_connection",
    ]
    with (
        patch(patch_targets[0], return_value=mock_conn),
        patch(patch_targets[1], return_value=mock_conn),
    ):
        assert client.get(path).status_code == 200
