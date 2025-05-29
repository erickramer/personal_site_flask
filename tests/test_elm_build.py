import subprocess
import pytest

pytestmark = pytest.mark.unit


def test_elm_build():
    result = subprocess.run(
        ["elm", "make", "elm/Home.elm", "--output=/dev/null"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert result.returncode == 0, result.stderr.decode()
