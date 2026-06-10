"""Wes Anderson cinematic techniques and prompting language."""


class WesAnderson:
    """Signature techniques and prompting patterns for Wes Anderson style."""

    SIGNATURE_TECHNIQUES = [
        "Planimetric composition + perfect symmetry",
        "Dollhouse framing / frontal staging",
        "Controlled, vibrant color palettes",
        "Meticulous production design",
        "Deadpan performance + slow, mechanical camera",
    ]

    @staticmethod
    def get_prompting_language() -> str:
        return (
            "Planimetric symmetrical composition with perfect frontal staging and horizontal layering, "
            "Wes Anderson-style dollhouse framing, vibrant controlled pastel palette, deadpan performance."
        )

    @staticmethod
    def get_example_shot() -> str:
        return "Static wide shot, perfectly symmetrical, characters centered in frame, vibrant pastel color palette, slow mechanical tracking if movement occurs."
