workflow "Publish sanic-healthchecks" {
  on = "push"
  resolves = ["publish"]
}

action "Master branch" {
  uses = "actions/bin/filter@master"
  args = "branch master"
}

action "publish" {
  needs = "Master branch"
  uses = "abatilo/actions-poetry@3.7.3"
  secrets = ["PYPI_USERNAME", "PYPI_PASSWORD"]
  args = ["publish", "--build", "--no-interaction", "-vv", "--username", "$PYPI_USERNAME", "--password", "$PYPI_PASSWORD"]
}
