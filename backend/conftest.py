import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--integration",
        action="store_true",
        default=False,
        help="Запустить интеграционные тесты (требуют поднятый postgres).",
    )


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "integration: интеграционные тесты, требующие postgres (запуск через --integration).",
    )


def pytest_collection_modifyitems(config, items):
    if config.getoption("--integration"):
        return  # флаг передан — запускаем всё

    skip_integration = pytest.mark.skip(reason="нужен флаг --integration (требует postgres)")
    for item in items:
        if item.get_closest_marker("integration"):
            item.add_marker(skip_integration)
