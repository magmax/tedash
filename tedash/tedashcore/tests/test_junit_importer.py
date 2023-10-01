import io
from django.test import TestCase
from unittest import TestCase as SimpleTestCase

from tedashcore.importers.junit import JunitImporter

JUNIT = """<?xml version="1.0" encoding="UTF-8"?>
<testsuites name="Test run" tests="8" failures="1" errors="1" skipped="1"
    assertions="20" time="16.082687" timestamp="2021-04-02T15:48:23">
    <testsuite name="Tests.Registration" tests="8" failures="1" errors="1" skipped="1"
        assertions="20" time="16.082687" timestamp="2021-04-02T15:48:23"
        file="tests/registration.code">
        <properties>
            properties with text values instead of value attributes. -->
            <property name="version" value="1.774" />
            <property name="commit" value="ef7bebf" />
            <property name="browser" value="Google Chrome" />
            <property name="ci" value="https://github.com/actions/runs/1234" />
            <property name="config">
                Config line #1
                Config line #2
                Config line #3
            </property>
        </properties>
        <system-out>Data written to standard out.</system-out>
        <system-err>Data written to standard error.</system-err>
        <testcase name="testCase1" classname="Tests.Registration" assertions="2"
            time="2.436" file="tests/registration.code" line="24" />
        <testcase name="testCase2" classname="Tests.Registration" assertions="6"
            time="1.534" file="tests/registration.code" line="62" />
        <testcase name="testCase3" classname="Tests.Registration" assertions="3"
            time="0.822" file="tests/registration.code" line="102" />
        <testcase name="testCase4" classname="Tests.Registration" assertions="0"
            time="0" file="tests/registration.code" line="164">
            <!-- <skipped> Indicates that the test was not executed. Can have an optional
            message describing why the test was skipped. -->
            <skipped message="Test was skipped." />
        </testcase>
        <testcase name="testCase5" classname="Tests.Registration" assertions="2"
            time="2.902412" file="tests/registration.code" line="202">
            <failure message="Expected value did not match." type="AssertionError">
            </failure>
        </testcase>
        <testcase name="testCase6" classname="Tests.Registration" assertions="0"
            time="3.819" file="tests/registration.code" line="235">
            <error message="Division by zero." type="ArithmeticError">
            </error>
        </testcase>

        <testcase name="testCase7" classname="Tests.Registration" assertions="3"
            time="2.944" file="tests/registration.code" line="287">
            <system-out>Data written to standard out.</system-out>

            <system-err>Data written to standard error.</system-err>
        </testcase>

        <testcase name="testCase8" classname="Tests.Registration" assertions="4"
            time="1.625275" file="tests/registration.code" line="302">
            <properties>
                <property name="priority" value="high" />
                <property name="language" value="english" />
                <property name="author" value="Adrian" />
                <property name="attachment" value="screenshots/dashboard.png" />
                <property name="attachment" value="screenshots/users.png" />
                <property name="description">
                    This text describes the purpose of this test case and provides
                    an overview of what the test does and how it works.
                </property>
            </properties>
        </testcase>
    </testsuite>
</testsuites>
"""


class JunitImporterTest(SimpleTestCase):
    def setUp(self):
        self.sut = JunitImporter(io.StringIO(JUNIT))

    def test_root(self):
        assert "metadata" in self.sut.data
        assert "testsuites" in self.sut.data

    def test_metadata(self):
        metadata = self.sut.data["metadata"]
        assert metadata["name"] == "Test run"
        assert metadata["tests"] == 8
        assert metadata["failures"] == 1
        assert metadata["errors"] == 1
        assert metadata["skipped"] == 1
        assert metadata["assertions"] == 20
        assert int(metadata["duration"]) == 16
        assert metadata["timestamp"] == "2021-04-02T15:48:23"
        assert "file" not in metadata

    def test_testsuite_metadata(self):
        assert len(self.sut.data["testsuites"]) == 1
        assert "metadata" in self.sut.data["testsuites"][0]
        metadata = self.sut.data["testsuites"][0]["metadata"]
        assert metadata["name"] == "Tests.Registration"
        assert metadata["tests"] == 8
        assert metadata["failures"] == 1
        assert metadata["errors"] == 1
        assert metadata["skipped"] == 1
        assert metadata["assertions"] == 20
        assert int(metadata["duration"]) == 16
        assert metadata["timestamp"] == "2021-04-02T15:48:23"
        assert metadata["file"] == "tests/registration.code"

    def test_testsuite_properties(self):
        assert "properties" in self.sut.data["testsuites"][0]
        properties = self.sut.data["testsuites"][0]["properties"]
        assert properties["version"] == "1.774"
        assert properties["commit"] == "ef7bebf"
        assert "Config line #1" in properties["config"]

    def test_testsuite_sysout(self):
        assert "system-out" in self.sut.data["testsuites"][0]
        assert self.sut.data["testsuites"][0]["system-out"] == "Data written to standard out."
        assert self.sut.data["testsuites"][0]["system-err"] == "Data written to standard error."

    def test_testsuite_testcases(self):
        assert "testcases" in self.sut.data["testsuites"][0]
        testcases = self.sut.data["testsuites"][0]["testcases"]
        assert len(testcases) == 8

    def test_testsuite_testcase_0(self):
        testcase = self.sut.data["testsuites"][0]["testcases"][0]
        assert testcase["name"] == "testCase1"
        assert testcase["classname"] == "Tests.Registration"
        assert testcase["assertions"] == 2
        assert 2.4 < testcase["duration"] < 2.5
        assert testcase["file"] == "tests/registration.code"
        assert testcase["line"] == 24
        assert not testcase["skipped"]
        assert "skip_message" not in testcase
        assert not testcase["failure"]
        assert "failure_message" not in testcase
        assert "failure_type" not in testcase
        assert "error_message" not in testcase
        assert "error_type" not in testcase

    def test_testsuite_testcase_skipped(self):
        testcase = self.sut.data["testsuites"][0]["testcases"][3]
        assert testcase["name"] == "testCase4"
        assert testcase["skipped"]
        assert testcase["skipped_message"] == "Test was skipped."

    def test_testsuite_testcase_failed(self):
        testcase = self.sut.data["testsuites"][0]["testcases"][4]
        assert testcase["name"] == "testCase5"
        assert not testcase["skipped"]
        assert testcase["failure"]
        assert testcase["failure_message"] == "Expected value did not match."
        assert testcase["failure_type"] == "AssertionError"

    def test_testsuite_testcase_errored(self):
        testcase = self.sut.data["testsuites"][0]["testcases"][5]
        assert testcase["name"] == "testCase6"
        assert not testcase["skipped"]
        assert not testcase["failure"]
        assert testcase["error"]
        assert testcase["error_message"] == "Division by zero."
        assert testcase["error_type"] == "ArithmeticError"

    def test_testsuite_testcase_outputs(self):
        testcase = self.sut.data["testsuites"][0]["testcases"][6]
        assert testcase["name"] == "testCase7"
        assert not testcase["skipped"]
        assert not testcase["failure"]
        assert not testcase["error"]
        assert testcase["stdout"] == "Data written to standard out."
        assert testcase["stderr"] == "Data written to standard error."

    def test_testsuite_testcase_with_properties(self):
        testcase = self.sut.data["testsuites"][0]["testcases"][7]
        assert testcase["name"] == "testCase8"
        assert testcase["properties"]["priority"] == "high"
        assert "This text describes the purpose of" in testcase["properties"]["description"]
