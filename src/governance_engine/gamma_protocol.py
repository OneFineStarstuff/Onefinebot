import hashlib
import time

class GammaProtocol:
    """
    Unified Gamma Protocol for governance tokenization and heartbeat.
    """
    def __init__(self, node_id="master-01"):
        self.node_id = node_id
        self.heartbeat_count = 0

    def generate_governance_token(self, entropy_source):
        """
        Generates a secure SHA256 governance token.
        """
        raw_token = f"{self.node_id}-{entropy_source}-{time.time()}".encode()
        return hashlib.sha256(raw_token).hexdigest()

    def pulse(self, mitigations_active):
        """
        Heartbeat mechanism.
        Returns health status and token.
        """
        self.heartbeat_count += 1
        status = "HEALTHY" if mitigations_active else "DEGRADED"
        token = self.generate_governance_token(str(self.heartbeat_count))

        return {
            "heartbeat_index": self.heartbeat_count,
            "status": status,
            "governance_token": token,
            "timestamp": time.time()
        }
