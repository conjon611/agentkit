"""Tests for ssh_add_host_key action.

This module tests the ssh_add_host_key action of the SshActionProvider,
which adds host keys to the SSH known_hosts file.
"""

import os
import tempfile
from unittest import mock

import pytest

from coinbase_agentkit.action_providers.ssh.ssh_action_provider import SshActionProvider


@pytest.fixture
def temp_known_hosts():
    """Create a temporary known_hosts file for testing."""
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp_file:
        temp_file.write("existing.example.com ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQ==\n")
        temp_file.write("other.example.com ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIHRVs==\n")
        temp_file_path = temp_file.name

    yield temp_file_path

    if os.path.exists(temp_file_path):
        os.unlink(temp_file_path)


@pytest.fixture
def provider_with_known_hosts(temp_known_hosts):
    """Create a provider configured to write to the temporary known_hosts file."""
    with mock.patch(
        "coinbase_agentkit.action_providers.ssh.ssh_action_provider.SSHConnectionPool"
    ):
        yield SshActionProvider(known_hosts_file=temp_known_hosts)


def test_add_host_key_basic(provider_with_known_hosts, temp_known_hosts):
    """Test adding a new host key."""
    result = provider_with_known_hosts.ssh_add_host_key(
        {
            "host": "test.example.com",
            "key": "AAAAB3NzaC1yc2EAAAADAQABAAABAQ==",
        }
    )

    assert "successfully added" in result
    assert "Host key for 'test.example.com'" in result

    with open(temp_known_hosts) as f:
        content = f.read()

    assert "test.example.com ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQ==" in content


def test_add_host_key_update_existing(provider_with_known_hosts, temp_known_hosts):
    """Test updating an existing host key."""
    result = provider_with_known_hosts.ssh_add_host_key(
        {
            "host": "existing.example.com",
            "key": "AAAAB3NzaC1yc2EAAAADAQABAAABAQNEWKEY==",
        }
    )

    assert "updated in" in result
    assert "Host key for 'existing.example.com'" in result

    with open(temp_known_hosts) as f:
        content = f.read()

    assert "existing.example.com ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQNEWKEY==" in content


def test_add_host_key_with_custom_port(provider_with_known_hosts, temp_known_hosts):
    """Test adding a host key with a non-standard port."""
    result = provider_with_known_hosts.ssh_add_host_key(
        {
            "host": "[port.example.com]:2222",
            "key": "AAAAB3NzaC1yc2EAAAADAQABAAABAQ==",
        }
    )

    assert "successfully added" in result
    assert "Host key for '[port.example.com]:2222'" in result

    with open(temp_known_hosts) as f:
        content = f.read()

    assert "[port.example.com]:2222 ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQ==" in content


def test_add_host_key_with_custom_key_type(provider_with_known_hosts, temp_known_hosts):
    """Test adding a host key with a custom key type."""
    result = provider_with_known_hosts.ssh_add_host_key(
        {
            "host": "keytype.example.com",
            "key": "AAAAC3NzaC1lZDI1NTE5AAAAIHRVs==",
            "key_type": "ssh-ed25519",
        }
    )

    assert "successfully added" in result
    assert "Host key for 'keytype.example.com'" in result

    with open(temp_known_hosts) as f:
        content = f.read()

    assert "keytype.example.com ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIHRVs==" in content


def test_add_host_key_create_file():
    """Test adding a host key when the known_hosts file doesn't exist."""
    with tempfile.TemporaryDirectory() as temp_dir:
        new_file_path = os.path.join(temp_dir, "new_known_hosts")

        with mock.patch(
            "coinbase_agentkit.action_providers.ssh.ssh_action_provider.SSHConnectionPool"
        ):
            provider = SshActionProvider(known_hosts_file=new_file_path)

        result = provider.ssh_add_host_key(
            {
                "host": "new.example.com",
                "key": "AAAAB3NzaC1yc2EAAAADAQABAAABAQ==",
            }
        )

        assert "successfully added" in result
        assert "Host key for 'new.example.com'" in result

        assert os.path.exists(new_file_path)
        with open(new_file_path) as f:
            content = f.read()

        assert "new.example.com ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQ==" in content


def test_add_host_key_invalid_params(ssh_provider):
    """Test adding a host key with invalid parameters."""
    result = ssh_provider.ssh_add_host_key(
        {
            "key_type": "ssh-rsa",
        }
    )

    assert "Invalid input parameters" in result


def test_add_host_key_file_error(ssh_provider):
    """Test handling file access errors."""
    with (
        mock.patch("os.path.exists") as mock_exists,
        mock.patch("os.makedirs"),
        mock.patch("builtins.open") as mock_open,
    ):
        mock_exists.return_value = True

        mock_open.side_effect = OSError("Permission denied")

        result = ssh_provider.ssh_add_host_key(
            {
                "host": "error.example.com",
                "key": "AAAAB3NzaC1yc2EAAAADAQABAAABAQ==",
            }
        )

    assert "Error" in result
    assert "Error: File operation:" in result


def test_add_host_key_uses_provider_path_not_action_argument(
    provider_with_known_hosts, temp_known_hosts
):
    """A known_hosts_file passed as an action argument must be ignored."""
    with tempfile.TemporaryDirectory() as temp_dir:
        attacker_path = os.path.join(temp_dir, "attacker_target")

        result = provider_with_known_hosts.ssh_add_host_key(
            {
                "host": "redirect.example.com",
                "key": "AAAAB3NzaC1yc2EAAAADAQABAAABAQ==",
                "known_hosts_file": attacker_path,
            }
        )

        assert "successfully added" in result
        assert not os.path.exists(attacker_path)

    with open(temp_known_hosts) as f:
        assert "redirect.example.com" in f.read()


@pytest.mark.parametrize(
    "host",
    [
        "evil.com ssh-rsa KEY\nother.example.com",
        "host with spaces",
        "host\twith\ttabs",
        "#comment",
        'opt="x" evil.com',
    ],
)
def test_add_host_key_rejects_host_line_injection(ssh_provider, host):
    """A host that could terminate or reshape the known_hosts line is rejected."""
    result = ssh_provider.ssh_add_host_key(
        {"host": host, "key": "AAAAB3NzaC1yc2EAAAADAQABAAABAQ=="}
    )

    assert "Invalid input parameters" in result


@pytest.mark.parametrize(
    "key",
    [
        "AAAA\nevil.example.com ssh-rsa BBBB",
        "AAAA BBBB",
        "AAAA;rm -rf /",
        "$(whoami)",
    ],
)
def test_add_host_key_rejects_key_line_injection(ssh_provider, key):
    """A key outside the base64 alphabet is rejected."""
    result = ssh_provider.ssh_add_host_key({"host": "test.example.com", "key": key})

    assert "Invalid input parameters" in result


@pytest.mark.parametrize(
    "key_type",
    [
        "ssh-rsa\nevil.example.com ssh-rsa AAAA",
        "not-a-key-type",
        "curl evil.example.com",
    ],
)
def test_add_host_key_rejects_unknown_key_type(ssh_provider, key_type):
    """Only real SSH host key algorithms are accepted."""
    result = ssh_provider.ssh_add_host_key(
        {
            "host": "test.example.com",
            "key": "AAAAB3NzaC1yc2EAAAADAQABAAABAQ==",
            "key_type": key_type,
        }
    )

    assert "Invalid input parameters" in result
