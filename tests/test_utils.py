"""Unit tests for MyLittleAnsible modules."""

import pytest
from mylittleansible.utils import CmdResult, TaskResult, PlaybookResult


class TestCmdResult:
    """Test CmdResult class."""

    def test_cmd_result_success(self):
        """Test successful command result."""
        result = CmdResult(stdout="OK", stderr="", exit_code=0, changed=True)
        assert result.is_success is True
        assert result.changed is True
        assert "OK" in str(result)

    def test_cmd_result_failure(self):
        """Test failed command result."""
        result = CmdResult(stdout="", stderr="Error", exit_code=1, changed=False)
        assert result.is_success is False
        assert result.changed is False
        assert "FAILED" in str(result)

    def test_cmd_result_str(self):
        """Test string representation."""
        result = CmdResult(stdout="Package installed", stderr="", exit_code=0, changed=True)
        assert "✓ OK" in str(result)
        assert "[CHANGED]" in str(result)


class TestTaskResult:
    """Test TaskResult class."""

    def test_task_result_ok(self):
        """Test OK task result."""
        result = TaskResult(host="web01", task_name="apt", status="OK", changed=True)
        assert result.status == "OK"
        assert result.changed is True

    def test_task_result_failed(self):
        """Test FAILED task result."""
        result = TaskResult(
            host="web01", task_name="apt", status="FAILED", message="Connection timeout"
        )
        assert result.status == "FAILED"
        assert result.message == "Connection timeout"

    def test_task_result_str(self):
        """Test string representation."""
        result = TaskResult(host="web01", task_name="apt", status="OK", changed=True)
        assert "[OK]" in str(result)
        assert "web01" in str(result)
        assert "[CHANGED]" in str(result)


class TestPlaybookResult:
    """Test PlaybookResult class."""

    def test_playbook_result_add_ok(self):
        """Test adding OK results."""
        result = PlaybookResult()
        task = TaskResult(host="web01", task_name="apt", status="OK")
        result.add_result(task)
        assert result.ok_count == 1
        assert result.failed_count == 0

    def test_playbook_result_add_failed(self):
        """Test adding FAILED results."""
        result = PlaybookResult()
        task = TaskResult(host="web01", task_name="apt", status="FAILED")
        result.add_result(task)
        assert result.failed_count == 1
        assert result.is_success is False

    def test_playbook_result_add_changed(self):
        """Test tracking changed tasks."""
        result = PlaybookResult()
        task = TaskResult(host="web01", task_name="apt", status="OK", changed=True)
        result.add_result(task)
        assert result.changed_count == 1

    def test_playbook_result_summary(self):
        """Test playbook summary."""
        result = PlaybookResult()
        result.add_result(TaskResult(host="web01", task_name="apt", status="OK", changed=True))
        result.add_result(TaskResult(host="web02", task_name="service", status="OK"))
        result.add_result(TaskResult(host="web03", task_name="command", status="FAILED"))

        assert result.ok_count == 2
        assert result.failed_count == 1
        assert result.changed_count == 1
        assert result.is_success is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
