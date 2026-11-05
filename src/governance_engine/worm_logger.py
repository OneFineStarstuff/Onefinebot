"""Local in-memory audit batch simulator.

This module intentionally does not claim WORM storage or post-quantum security.
The historical class name is retained for import compatibility only.
"""
from datetime import datetime, timezone
import hashlib
import json


class PQCWORMLogger:
    """Legacy-compatible name for a non-persistent audit batch simulator.

    No durable storage, immutability controls, signatures, or post-quantum
    cryptography are implemented by this class.
    """

    INTEGRITY_MODE = "LOCAL_IN_MEMORY_SIMULATION_NO_WORM_OR_PQC"

    def __init__(self):
        self.log_batch = []

    def log_event(self, event_type, details):
        """Append an event to the local process memory only."""
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "details": details,
            "integrity_mode": self.INTEGRITY_MODE,
        }
        self.log_batch.append(entry)
        return entry

    def commit_batch(self):
        """Return a deterministic fingerprint; this does not persist data."""
        serialized = json.dumps(
            self.log_batch,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            default=str,
        )
        fingerprint = hashlib.sha384(serialized.encode("utf-8")).hexdigest()
        summary = {
            "batch_id": f"sim-{fingerprint[:16]}",
            "fingerprint_sha384": fingerprint,
            "size": len(self.log_batch),
            "status": "SIMULATED_ONLY_NOT_PERSISTED",
            "integrity_mode": self.INTEGRITY_MODE,
        }
        # Preserve the legacy lifecycle behavior. The returned summary is not
        # a durable evidence record; events are discarded from process memory.
        self.log_batch = []
        return summary
