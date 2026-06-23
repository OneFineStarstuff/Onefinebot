import unittest
from src.governance_engine.maturity_engine import EthicsMaturityEngine
from src.moe_pipeline import MoEPipeline

class TestEthicsMaturityAndHITL(unittest.TestCase):
    def test_maturity_calculation(self):
        engine = EthicsMaturityEngine()

        # Perfect compliance
        score = engine.calculate_score(dpd=0.0, has_cae=True, audit_committed=True)
        self.assertEqual(score, 5.0)

        # Low compliance
        score = engine.calculate_score(dpd=0.5, has_cae=False, audit_committed=False)
        # Fairness: (1.0 - 0.5) * 5 * 0.4 = 0.5 * 5 * 0.4 = 1.0
        # Interpretability: 0 * 0.3 = 0.0
        # Audit: 0 * 0.3 = 0.0
        # Total: 1.0
        self.assertEqual(score, 1.0)

    def test_hitl_override(self):
        pipeline = MoEPipeline()
        data = [1, 2]

        # Normal execution (random assignments)
        result1 = pipeline.process_data(data)
        self.assertEqual(len(result1["assignments"]), 2)

        # HITL Override
        override = [
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0]
        ]
        result2 = pipeline.process_data(data, override_assignments=override)
        self.assertEqual(result2["assignments"], override)

    def test_zk_proof_integrity(self):
        from omni_sentinel.fairness import ZKFairnessProof
        prover = ZKFairnessProof()
        weights = [[0.5, 0.5]]
        proof = prover.generate_proof(weights, 0.05)

        # Correct weights
        valid, msg = prover.verify(proof, expert_weights=weights)
        self.assertTrue(valid)

        # Tampered weights
        tampered_weights = [[0.6, 0.4]]
        valid, msg = prover.verify(proof, expert_weights=tampered_weights)
        self.assertFalse(valid)
        self.assertIn("integrity failure", msg)

if __name__ == "__main__":
    unittest.main()
