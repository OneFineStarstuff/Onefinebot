import hashlib
import os

class FairnessValidator:
    """
    Implements MAS FEAT Compliance checks, specifically Demographic Parity
    for Mixture of Experts (MoE) routing.
    """
    @staticmethod
    def calculate_demographic_parity(expert_assignments, sensitive_attributes):
        """
        Calculates the Demographic Parity Difference (DPD) for expert routing.
        """
        groups = list(set(sensitive_attributes))
        group_expert_probs = []
        for g in groups:
            indices = [i for i, x in enumerate(sensitive_attributes) if x == g]
            group_assignments = [expert_assignments[i] for i in indices]
            num_samples = len(group_assignments)
            if num_samples == 0:
                continue
            num_experts = len(group_assignments[0])
            probs = [sum(row[j] for row in group_assignments) / num_samples for j in range(num_experts)]
            group_expert_probs.append(probs)

        dpd = 0
        for i in range(len(group_expert_probs)):
            for j in range(i + 1, len(group_expert_probs)):
                diffs = [abs(group_expert_probs[i][k] - group_expert_probs[j][k]) for k in range(len(group_expert_probs[0]))]
                dpd = max(dpd, max(diffs))

        return dpd

class ZKFairnessProof:
    """
    A simulated Zero-Knowledge Proof mechanism for fairness compliance.
    """
    def __init__(self, secret_salt=None):
        # Remediated: Use environment variable instead of hardcoded salt
        self.secret_salt = secret_salt or os.getenv("OMNI_SENTINEL_SALT", "default_safe_salt_placeholder")

    def generate_proof(self, expert_weights, fairness_score):
        """
        Generates a 'proof' without revealing the internal weights.
        """
        weight_hash = hashlib.sha256(str(expert_weights).encode() + self.secret_salt.encode()).hexdigest()
        is_compliant = fairness_score < 0.1

        proof = {
            "commitment": weight_hash,
            "fairness_score": fairness_score,
            "is_compliant": is_compliant,
            "algorithm": "ZK-Fairness-DP-v1"
        }
        return proof

    def verify(self, proof, expert_weights=None):
        """
        Verifies the proof. If expert_weights is provided, validates data integrity.
        """
        if not proof.get("is_compliant"):
            return False, "Proof indicates non-compliance with fairness threshold."

        if expert_weights is not None:
            expected_hash = hashlib.sha256(str(expert_weights).encode() + self.secret_salt.encode()).hexdigest()
            if expected_hash != proof.get("commitment"):
                return False, "Data integrity failure: Expert weights do not match the commitment."

        return True, "Fairness proof verified successfully."
