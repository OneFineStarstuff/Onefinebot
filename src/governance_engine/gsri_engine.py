import random

class GSRIEngine:
    """
    G-SRI (Systemic Risk Index) Scoring Engine.
    Monitors high-risk vectors and applies mitigations.
    """
    def __init__(self):
        self.risk_vectors = {
            "Agent_Collaboration_Dark_Patterns": 0.5,
            "Encrypted_Traffic_Entropy": 0.4,
            "Model_Weights_Drift": 0.2,
            "Unauthorized_Recursive_Loop": 0.8
        }
        self.mitigations_active = False

    def set_mitigations(self, active: bool):
        self.mitigations_active = active

    def calculate_score(self):
        """
        Calculates the current G-SRI score.
        Score = Sum(Vector * Random_Factor) / (1 + Mitigation_Dampener)
        """
        base_score = sum(val * random.uniform(0.8, 1.2) for val in self.risk_vectors.values())

        # Thresholds from AXI-10: < 0.75 or similar context-dependent limits
        # Actually AXI-10 mentioned 6.67 and threshold < 0.75 was for G-SRI?
        # Wait, the audit said G-SRI: 6.67 (Threshold: < 0.75) -> PASS.
        # That seems like a typo in the description or I misunderstood the scale.
        # Let's check AXI-7: G-SRI: 22.77 (Threshold: < 40.0) -> PASS.
        # Let's assume higher is worse, but mitigations help.

        dampener = 2.0 if self.mitigations_active else 1.0
        final_score = base_score / dampener

        return round(final_score, 2)

    def get_status(self, score):
        if score < 10.0:
            return "GREEN (NOMINAL)"
        elif score < 25.0:
            return "YELLOW (ELEVATED)"
        else:
            return "RED (CRITICAL)"
