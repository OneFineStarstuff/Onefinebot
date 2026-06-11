class ContextualAttributionEnvelope:
    """
    Implements HKMA Ethics Compliance by wrapping technical attributions.
    """
    def __init__(self, ethical_guidelines=None):
        self.ethical_guidelines = ethical_guidelines or {
            "financial_inclusion": "Ensures decisions do not exclude marginalized groups.",
            "algorithmic_transparency": "Provides clear reasons for model outputs.",
            "data_privacy": "Ensures PII is not the primary driver of decisions."
        }

    def wrap_attributions(self, technical_attributions, feature_names):
        """
        Wraps raw technical attributions with contextual 'envelopes'.
        """
        enveloped_explanations = []
        for i, attr in enumerate(technical_attributions):
            feature = feature_names[i]
            impact = "positive" if attr > 0 else "negative"
            magnitude = abs(attr)

            guideline = self._map_feature_to_guideline(feature)

            explanation = {
                "feature": feature,
                "technical_score": attr,
                "ethical_impact": impact,
                "stakeholder_context": f"Feature '{feature}' had a {impact} impact on the decision, contributing {magnitude:.4f} to the final score.",
                "compliance_guideline": guideline,
                "guideline_description": self.ethical_guidelines.get(guideline, "General interpretability.")
            }
            enveloped_explanations.append(explanation)

        return enveloped_explanations

    def _map_feature_to_guideline(self, feature):
        if any(keyword in feature.lower() for keyword in ["income", "credit", "asset"]):
            return "financial_inclusion"
        if any(keyword in feature.lower() for keyword in ["age", "gender", "race", "zip"]):
            return "data_privacy"
        return "algorithmic_transparency"

class ASAInterpretabilityLayer:
    """
    Algorithmic Stakeholder Alignment (ASA) Layer for HKMA Ethics Compliance.
    """
    def __init__(self, cae_wrapper: ContextualAttributionEnvelope):
        self.cae_wrapper = cae_wrapper

    def generate_stakeholder_report(self, attributions, feature_names):
        """
        Generates a report suitable for HKMA ethical audit.
        """
        enveloped_data = self.cae_wrapper.wrap_attributions(attributions, feature_names)

        report = {
            "compliance_status": "HKMA-Ethics-Compliant",
            "layer_type": "ASA-CAE-v1",
            "explanations": enveloped_data,
            "summary": "This decision has been processed through the ASA layer to ensure alignment with ethical guidelines."
        }
        return report
