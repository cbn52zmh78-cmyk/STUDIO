"""Giallo / Brian De Palma cinematic techniques and prompting language."""


class GialloDePalma:
    """Signature techniques and prompting patterns for Giallo and De Palma style."""

    SIGNATURE_TECHNIQUES = [
        "Stylized, operatic violence",
        "Expressionistic color and lighting",
        "Subjective/voyeuristic camera, bold tracking, dramatic zooms",
    ]

    @staticmethod
    def get_prompting_language() -> str:
        return (
            "Giallo-inspired stylized murder sequence with bold tracking shot and lurid red lighting, "
            "De Palma-style subjective camera and dramatic zoom on the gloved hand."
        )
