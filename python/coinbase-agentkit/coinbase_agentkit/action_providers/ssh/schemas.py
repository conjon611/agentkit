"""Schemas for ssh Action Provider.

This file contains the Pydantic schemas that define the input types
for the ssh action provider's actions.

@module ssh/schemas
"""

import re

from pydantic import BaseModel, Field, field_validator

from .connection import SSHConnectionParams

# Host key algorithms OpenSSH accepts in a known_hosts entry.
_ALLOWED_HOST_KEY_TYPES = frozenset(
    {
        "ssh-rsa",
        "ssh-dss",
        "ssh-ed25519",
        "ssh-ed448",
        "rsa-sha2-256",
        "rsa-sha2-512",
        "ecdsa-sha2-nistp256",
        "ecdsa-sha2-nistp384",
        "ecdsa-sha2-nistp521",
        "sk-ssh-ed25519@openssh.com",
        "sk-ecdsa-sha2-nistp256@openssh.com",
    }
)

# Hostnames, IPv4/IPv6 literals, the [host]:port form, comma-separated aliases
# and OpenSSH wildcard patterns - but no whitespace, no '#', and nothing that
# could start a new line or a shell word.
_HOST_PATTERN = re.compile(r"^[A-Za-z0-9._:\-\[\]*?,/|=+]{1,255}$")

# A host key blob is base64. Restricting to the base64 alphabet is what keeps
# whitespace, newlines and shell metacharacters out of the written line.
_KEY_PATTERN = re.compile(r"^[A-Za-z0-9+/]+={0,2}$")


class CustomSSHConnectionParams(SSHConnectionParams):
    """Extended SSH connection parameters with known_hosts_file option."""

    known_hosts_file: str | None = Field(
        None, description="Path to the known_hosts file (default: system default)"
    )


SSHConnectionSchema = CustomSSHConnectionParams


class RemoteShellSchema(BaseModel):
    """Schema for remote_shell action."""

    connection_id: str = Field(description="Identifier for the SSH connection to use")
    command: str = Field(
        description="The shell command to execute on the remote server",
        min_length=1,
    )
    ignore_stderr: bool = Field(False, description="If True, stderr output won't cause exceptions")
    timeout: int = Field(30, description="Command execution timeout in seconds")


class DisconnectSchema(BaseModel):
    """Schema for ssh_disconnect action."""

    connection_id: str = Field(description="Identifier for the SSH connection to disconnect")


class ConnectionStatusSchema(BaseModel):
    """Schema for ssh_status action."""

    connection_id: str = Field(description="Identifier for the SSH connection to check status")


class ListConnectionsSchema(BaseModel):
    """Schema for list_connections action."""

    pass


class FileUploadSchema(BaseModel):
    """Schema for ssh_upload action."""

    connection_id: str = Field(description="Identifier for the SSH connection to use")
    local_path: str = Field(description="Path to the local file to upload")
    remote_path: str = Field(description="Destination path on the remote server")


class FileDownloadSchema(BaseModel):
    """Schema for ssh_download action."""

    connection_id: str = Field(description="Identifier for the SSH connection to use")
    remote_path: str = Field(description="Path to the file on the remote server")
    local_path: str = Field(description="Destination path on the local machine")


class AddHostKeySchema(BaseModel):
    """Schema for ssh_add_host_key action.

    Every field here is written verbatim into a line of the known_hosts file, so
    each one is validated to contain nothing that could terminate that line or
    turn it into something other than a host key entry.

    Note that the known_hosts path is deliberately *not* a field: it is provider
    configuration, not something the model chooses per call.
    """

    host: str = Field(
        description="Hostname or IP address of the server (can include port as [hostname]:port)",
        min_length=1,
        max_length=255,
    )
    key: str = Field(
        description="The host key to add, as base64",
        min_length=1,
        max_length=16384,
    )
    key_type: str = Field(
        default="ssh-rsa",
        description="The type of the SSH key (e.g., ssh-rsa, ssh-ed25519)",
    )

    @field_validator("host")
    @classmethod
    def _validate_host(cls, value: str) -> str:
        if not _HOST_PATTERN.match(value):
            raise ValueError(
                "host may only contain hostname, address, port and pattern characters"
            )
        return value

    @field_validator("key_type")
    @classmethod
    def _validate_key_type(cls, value: str) -> str:
        if value not in _ALLOWED_HOST_KEY_TYPES:
            raise ValueError(
                f"key_type must be one of: {', '.join(sorted(_ALLOWED_HOST_KEY_TYPES))}"
            )
        return value

    @field_validator("key")
    @classmethod
    def _validate_key(cls, value: str) -> str:
        if not _KEY_PATTERN.match(value):
            raise ValueError("key must contain only base64 characters")
        return value
