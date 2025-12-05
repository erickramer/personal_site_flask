import subprocess
import pytest

pytestmark = pytest.mark.deploy


def test_makefile_deploy_target():
    """Ensure the deploy target builds assets and calls gcloud."""
    result = subprocess.run(["make", "--dry-run", "deploy"], capture_output=True, text=True, check=False)
    output = result.stdout
    assert "elm make elm/Home.elm" in output
    assert "elm make elm/Asteroids.elm" in output
    assert "gcloud app deploy" in output
