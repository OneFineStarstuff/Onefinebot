from src.moe_pipeline import MoEPipeline

class AGISystemSTEM:
    """
    Unified AGI System Entry Point with Omni-Sentinel G-Stack Governance.
    """
    def __init__(self):
        print("Omni-Sentinel G-Stack Initialized (Governance v2.4.1)")
        self.pipeline = MoEPipeline()

    def process_request(self, data, sensitive_attributes=None):
        print("Processing request through Governance-secured MoE pipeline...")
        result = self.pipeline.process_data(data, sensitive_attributes)

        audit = result["audit"]
        print(f"G-SRI Risk Score: {audit['gsri_score']} - Status: {audit['system_status']}")
        print(f"Gamma Heartbeat: {audit['heartbeat']['status']} (Token: {audit['heartbeat']['governance_token'][:12]}...)")

        return result

    def shutdown(self):
        print("Shutting down... Committing final governance audit batch.")
        commit_info = self.pipeline.finalize_session()
        print(f"Audit Committed. Batch ID: {commit_info['batch_id']}")
        return commit_info

def main():
    print("--- Omni-Sentinel G-Stack Governance Demonstration (AXI-10) ---")
    agi = AGISystemSTEM()

    # Simulated data and sensitive attributes
    data = [1, 2, 3, 4, 5]
    sensitive_attributes = [0, 1, 0, 1, 0]

    # 1. Normal Operation
    print("\n[Audit 1: Normal Operation]")
    agi.process_request(data, sensitive_attributes)

    # 2. Mitigation Mode
    print("\n[Audit 2: Mitigation Mode Active]")
    agi.pipeline.orchestrator.gsri.set_mitigations(True)
    agi.process_request(data, sensitive_attributes)

    # Shutdown and Commit
    print("\n[Finalization]")
    agi.shutdown()

if __name__ == "__main__":
    main()
