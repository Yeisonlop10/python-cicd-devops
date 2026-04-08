from click.testing import CliRunner
from pytest_mock import MockerFixture
from simple_http_checker.cli import main

def test_no_urls():
    runner = CliRunner()
    result = runner.invoke(main, [])
    assert result.exit_code == 0
    assert "Please provide at least one URL to check." in result.output

def test_main_single_url_success(mocker: MockerFixture):
    url = "http://www.example.com"
    
    mock_check = mocker.patch("simple_http_checker.cli.check_urls")

    mock_check.return_value = {url: "200 OK"}

    runner = CliRunner()
    result = runner.invoke(main, [url])

    assert result.exit_code == 0
    mock_check.assert_called_once_with((url,), timeout=5)
    assert "--- Results ---" in result.output
    assert url in result.output
    assert "-> 200 OK" in result.output

def test_main_timeout_option(mocker: MockerFixture):
    url = "http://www.example.com"
    
    mock_check = mocker.patch("simple_http_checker.cli.check_urls")

    mock_check.return_value = {url: "TIMEOUT"}

    runner = CliRunner()
    result = runner.invoke(main, [url, "--timeout", "10"])

    assert result.exit_code == 0
    mock_check.assert_called_once_with((url,), timeout=10)
    assert "--- Results ---" in result.output
    assert url in result.output
    assert "-> TIMEOUT" in result.output