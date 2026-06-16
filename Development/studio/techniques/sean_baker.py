"""Sean Baker cinematic techniques and prompting language.

This module captures the naturalistic, empathetic, and often handheld observational
style of Sean Baker, known for films like Tangerine, The Florida Project, Red Rocket,
and Anora. Emphasis on real locations, non-professional or naturalistic performances,
and long-take energy.
"""


class SeanBaker:
    """Signature techniques and prompting patterns for Sean Baker style.

    Focuses on observational realism, motivated camera work, empathetic framing of
    marginalized characters, and the balance between controlled cinema and serendipity.
    """

    SIGNATURE_TECHNIQUES = [
        "Naturalistic, observational handheld or minimal-crew style (guerilla filmmaking approach)",
        "One-take or long-take energy with fluid, lived-in movement",
        "Gritty yet empathetic framing of real locations and non-professional or naturalistic actors",
        "Minimal lighting, real locations, throw actors into real life and capture happy accidents",
        "Controlled 90% with 10% left to the film gods (serendipity and happy accidents)",
        "Mix of raw realism and compassionate, humanistic framing",
    ]

    @staticmethod
    def get_core_principles() -> str:
        """Returns Sean Baker's core approach to cinematic storytelling."""
        return (
            "Baker's work blends controlled cinematic craft with genuine serendipity. He prioritizes "
            "real locations, minimal crews, and throwing performers into authentic situations. The camera "
            "often feels like a participant — handheld, reactive, and motivated by character action rather than "
            "stylistic flourish. The goal is emotional authenticity and humanistic observation without "
            "exploitation. 90% control, 10% to the film gods."
        )

    @staticmethod
    def get_prompting_language(variation: str = "standard") -> str:
        """Returns ready-to-use prompting language for Sean Baker-inspired shots.

        Args:
            variation: "standard", "handheld", "long_take", or "empathetic"
        """
        prompts = {
            "standard": (
                "Naturalistic handheld camera following her through the crowded street, Sean Baker-style "
                "observational realism, shallow depth of field on her face while background remains chaotic and alive."
            ),
            "handheld": (
                "Slight nervous handheld following the character through a real location, motivated camera movement, "
                "natural lighting, shallow depth of field isolating her expression while the environment feels lived-in and chaotic."
            ),
            "long_take": (
                "Long continuous take following the character through a real environment, fluid but grounded camera movement, "
                "natural performances, minimal intervention, capturing small behavioral details and environmental texture."
            ),
            "empathetic": (
                "Close but respectful observational framing on a marginalized character in a real location, "
                "naturalistic lighting and performance, camera stays with her emotionally without becoming exploitative or overly stylized."
            ),
        }
        return prompts.get(variation, prompts["standard"])

    @staticmethod
    def get_example_shot(context: str = "") -> str:
        """Example shot incorporating Baker's naturalistic approach."""
        base = (
            "Naturalistic handheld camera moving with the character through a real, lived-in location. "
            "Shallow depth of field on her face and micro-expressions while the background remains textured and chaotic. "
            "Motivated camera work, natural lighting, authentic performance."
        )
        if context:
            return f"{base} {context}"
        return base
