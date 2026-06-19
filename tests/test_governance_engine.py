import unittest
from src.governance_engine.gsri_engine import GSRIEngine
from src.governance_engine.gamma_protocol import GammaProtocol
from src.governance_engine.worm_logger import PQCWORMLogger
from src.governance_engine.orchestrator import GovernanceOrchestrator

class TestGovernanceEngine(unittest.TestCase):
    def test_gsri_scoring(self):
        engine = GSRIEngine()
        score1 = engine.calculate_score()
        engine.set_mitigations(True)
        score2 = engine.calculate_score()
        self.assertLess(score2, score1)
        self.assertIn(engine.get_status(score1), ["GREEN (NOMINAL)", "YELLOW (ELEVATED)", "RED (CRITICAL)"])

    def test_gamma_protocol(self):
        gamma = GammaProtocol(node_id="test-node")
        pulse1 = gamma.pulse(mitigations_active=False)
        pulse2 = gamma.pulse(mitigations_active=True)
        self.assertEqual(pulse1["heartbeat_index"], 1)
        self.assertEqual(pulse2["heartbeat_index"], 2)
        self.assertEqual(pulse1["status"], "DEGRADED")
        self.assertEqual(pulse2["status"], "HEALTHY")
        self.assertNotEqual(pulse1["governance_token"], pulse2["governance_token"])

    def test_worm_logger(self):
        logger = PQCWORMLogger()
        event = logger.log_event("TEST_EVENT", {"key": "value"})
        self.assertIn("timestamp", event)
        self.assertEqual(event["event_type"], "TEST_EVENT")

        commit = logger.commit_batch()
        self.assertEqual(commit["size"], 1)
        self.assertEqual(commit["status"], "COMMITTED")
        self.assertEqual(len(logger.log_batch), 0)

    def test_governance_orchestrator(self):
        orchestrator = GovernanceOrchestrator()
        audit = orchestrator.perform_audit([[0.5, 0.5]], 0.05)
        self.assertIn("gsri_score", audit)
        self.assertIn("heartbeat", audit)
        self.assertIn("fairness_proof", audit)

        commit = orchestrator.finalize_audit()
        self.assertEqual(commit["size"], 1)

if __name__ == "__main__":
    unittest.main()
