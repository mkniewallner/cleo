from __future__ import annotations

import pytest

from cleo.application import Application
from cleo.commands.command import Command
from cleo.helpers import argument
from cleo.helpers import option
from cleo.testers.application_tester import ApplicationTester


class FooCommand(Command):
    """
    Foo command
    """

    name = "foo"

    description = "Foo command"

    arguments = [argument("foo")]

    options = [option("--bar")]

    def handle(self) -> int:
        self.line(self.argument("foo"))

        if self.option("bar"):
            self.line("--bar activated")
        return 0


class FooBarCommand(Command):
    """
    Foo Bar command
    """

    name = "foo bar"

    description = "Foo Bar command"

    arguments = [argument("foo")]

    options = [option("--baz")]

    def handle(self) -> int:
        self.line(self.argument("foo"))

        if self.option("baz"):
            self.line("--baz activated")
        return 0


@pytest.fixture()
def app() -> Application:
    app = Application()
    app.add(FooCommand())
    app.add(FooBarCommand())

    return app


@pytest.fixture()
def tester(app: Application) -> ApplicationTester:
    return ApplicationTester(app)


def test_execute(tester: ApplicationTester) -> None:
    assert tester.execute("foo baz --bar") == 0
    assert tester.status_code == 0
    assert tester.io.fetch_output() == "baz\n--bar activated\n"


def test_execute_namespace_command(tester: ApplicationTester) -> None:
    tester.application.catch_exceptions(False)
    assert tester.execute("foo bar baz --baz") == 0
    assert tester.status_code == 0
    assert tester.io.fetch_output() == "baz\n--baz activated\n"
