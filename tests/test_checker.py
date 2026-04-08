import pytest
import requests
from pytest_mock import MockerFixture

from simple_http_checker.checker import check_urls

def test_check_urls_success(mocker: MockerFixture):
    mocker_requests_get = mocker.patch("simple_http_checker.checker.requests.get")


    mock_response = mocker.MagicMock(spec=requests.Response)
    mock_response.status_code = 200
    mock_response.reason = "OK"
    mock_response.ok = True

    mocker_requests_get.return_value = mock_response

    urls = ["http://www.example.com"]
    results = check_urls(urls)

    mocker_requests_get.assert_called_once_with(urls[0], timeout=5)
    assert results[urls[0]] == "200 OK"

def test_check_urls_client_error(mocker: MockerFixture):
    mocker_requests_get = mocker.patch("simple_http_checker.checker.requests.get")

    mock_response = mocker.MagicMock(spec=requests.Response)
    mock_response.status_code = 404
    mock_response.reason = "Not Found"
    mock_response.ok = False

    mocker_requests_get.return_value = mock_response

    urls = ["http://www.example.com/nonexistent"]
    results = check_urls(urls)

    mocker_requests_get.assert_called_once_with(urls[0], timeout=5)
    assert results[urls[0]] == "FAIL (Status Code: 404) Not Found"

@pytest.mark.parametrize(
        "error_exception, expected_status",
        [
            (requests.exceptions.Timeout, "TIMEOUT after 5 seconds"),
            (requests.exceptions.ConnectionError, "CONNECTION_ERROR"),
            (requests.exceptions.RequestException, "REQUEST_ERROR"),
        ],
)
def test_check_urls_request_exception(mocker: MockerFixture, error_exception: type[requests.exceptions.RequestException], expected_status: str):
    mocker_requests_get = mocker.patch("simple_http_checker.checker.requests.get")

    mocker_requests_get.side_effect = error_exception(
        f"Simulated {expected_status}"
    )

    urls = ["http://www.problem.com"]
    results = check_urls(urls)

    mocker_requests_get.assert_called_once_with(urls[0], timeout=5)
    assert results[urls[0]] == expected_status

def test_check_urls_multiple_urls(mocker: MockerFixture):
    mocker_requests_get = mocker.patch("simple_http_checker.checker.requests.get")

    # First call: OK
    mocker_response = mocker.MagicMock(spec=requests.Response)
    mocker_response.status_code = 200
    mocker_response.reason = "OK"
    mocker_response.ok = True
    
    # Second call: Timeout
    timeout_exception = requests.exceptions.Timeout("Simulated timeout")

    # Third call: 500 Server Error
    mocker_response_fail = mocker.MagicMock(spec=requests.Response)
    mocker_response_fail.status_code = 500
    mocker_response_fail.reason = "Server Error"
    mocker_response_fail.ok = False

    mocker_requests_get.side_effect = [mocker_response, timeout_exception, mocker_response_fail]

    urls = ["http://www.success.com", "http://www.timeout.com", "http://www.servererror.com"]
    results = check_urls(urls)
    assert len(results) == 3
    assert mocker_requests_get.call_count == 3
    assert results[urls[0]] == "200 OK"
    assert results[urls[1]] == "TIMEOUT after 5 seconds"
    assert results[urls[2]] == "FAIL (Status Code: 500) Server Error"

def test_check_urls_empty_list():
    results = check_urls([])
    assert results == {}

def test_check_urls_custom_timeout(mocker: MockerFixture):
    mocker_requests_get = mocker.patch("simple_http_checker.checker.requests.get")

    mock_response = mocker.MagicMock(spec=requests.Response)
    mock_response.status_code = 200
    mock_response.reason = "OK"
    mock_response.ok = True

    mocker_requests_get.return_value = mock_response

    urls = ["http://www.example.com"]
    timeout = 10
    results = check_urls(urls, timeout=timeout)

    mocker_requests_get.assert_called_once_with(urls[0], timeout=timeout)
    assert results[urls[0]] == "200 OK"