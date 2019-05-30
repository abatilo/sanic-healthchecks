workflow "Publish sanic-healthchecks" {
  on = "push"
  resolves = ["publish"]
}

action "publish" {
  uses = "abatilo/actions-poetry@3.7.3"
  secrets = ["PYPI_USERNAME", "PYPI_PASSWORD"]
  args = ["publish", "--build", "--no-interaction", "-vv", "--username", "$PYPI_USERNAME", "--password", "$PYPI_PASSWORD"]
}
