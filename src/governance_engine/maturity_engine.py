class EthicsMaturityEngine:
    """
    Calculates the Ethics Maturity Score based on compliance metrics.
    Targets MAS FEAT and HKMA Ethics guidelines.
    """
    def __init__(self):
        self.weights = {
            "fairness": 0.4,
            "interpretability": 0.3,
            "audit_integrity": 0.3
        }

    def calculate_score(self, dpd, has_cae=True, audit_committed=True):
        """
        Calculates a maturity score from 0.0 to 5.0.

        Args:
            dpd (float): Demographic Parity Difference (lower is better).
            has_cae (bool): Whether Contextual Attribution Envelopes are active.
            audit_committed (bool): Whether the audit has been committed to secure storage.

        Returns:
            float: Maturity score rounded to 2 decimal places.
        """
        # Fairness component (MAS FEAT)
        # Low DPD (Demographic Parity Difference) is better.
        fairness_raw = (1.0 - min(dpd, 1.0)) * 5.0

        # Interpretability component (HKMA ASA/CAE)
        interpretability_raw = 5.0 if has_cae else 0.0

        # Audit Integrity component (WORM/Gamma)
        audit_raw = 5.0 if audit_committed else 0.0

        score = (
            fairness_raw * self.weights["fairness"] +
            interpretability_raw * self.weights["interpretability"] +
            audit_raw * self.weights["audit_integrity"]
        )

        return round(score, 2)
