import unittest
import sys
import os

# Adjust paths to import from omni_sentinel
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from omni_sentinel.fairness import FairnessValidator, ZKFairnessProof
from omni_sentinel.interpretability import ContextualAttributionEnvelope, ASAInterpretabilityLayer

class TestOmniSentinelCompliance(unittest.TestCase):

    def test_demographic_parity(self):
        expert_assignments = [
            [0.8, 0.2],
            [0.7, 0.3],
            [0.4, 0.6],
            [0.5, 0.5]
        ]
        sensitive_attributes = [0, 0, 1, 1]
        dpd = FairnessValidator.calculate_demographic_parity(expert_assignments, sensitive_attributes)
        self.assertAlmostEqual(dpd, 0.3, places=5)

    def test_zk_proof_generation(self):
        prover = ZKFairnessProof()
        weights = [0.1, 0.2]
        fairness_score = 0.05
        proof = prover.generate_proof(weights, fairness_score)

        self.assertTrue(proof["is_compliant"])
        self.assertEqual(proof["algorithm"], "ZK-Fairness-DP-v1")

        valid, msg = prover.verify(proof)
        self.assertTrue(valid)

    def test_asa_layer_report(self):
        cae = ContextualAttributionEnvelope()
        asa = ASAInterpretabilityLayer(cae)

        attributions = [0.5, -0.2]
        feature_names = ["annual_income", "user_age"]

        report = asa.generate_stakeholder_report(attributions, feature_names)

        self.assertEqual(report["compliance_status"], "HKMA-Ethics-Compliant")
        self.assertEqual(len(report["explanations"]), 2)

        self.assertEqual(report["explanations"][0]["compliance_guideline"], "financial_inclusion")
        self.assertEqual(report["explanations"][1]["compliance_guideline"], "data_privacy")

if __name__ == "__main__":
    unittest.main()
