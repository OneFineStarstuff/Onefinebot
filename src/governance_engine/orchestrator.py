from .gsri_engine import GSRIEngine
from .gamma_protocol import GammaProtocol
from .worm_logger import PQCWORMLogger
import sys
import os

# Import from parent for compliance components if needed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from omni_sentinel.fairness import ZKFairnessProof

class GovernanceOrchestrator:
    """
    Unified Governance Orchestrator integrating all compliance layers.
    """
    def __init__(self):
        self.gsri = GSRIEngine()
        self.gamma = GammaProtocol()
        self.worm = PQCWORMLogger()
        self.zk_fairness = ZKFairnessProof()

    def perform_audit(self, expert_weights, fairness_score):
        """
        Executes a full governance audit cycle.
        """
        # 1. GSRI Risk Assessment
        score = self.gsri.calculate_score()
        status = self.gsri.get_status(score)

        # 2. Gamma Heartbeat
        heartbeat = self.gamma.pulse(self.gsri.mitigations_active)

        # 3. ZK-Fairness Proof
        proof = self.zk_fairness.generate_proof(expert_weights, fairness_score)

        # 4. WORM Logging
        audit_data = {
            "gsri_score": score,
            "system_status": status,
            "heartbeat": heartbeat,
            "fairness_proof": proof
        }
        self.worm.log_event("GOVERNANCE_AUDIT", audit_data)

        return audit_data

    def finalize_audit(self):
        """
        Commits audit batch to WORM storage.
        """
        return self.worm.commit_batch()
