"""Wes Anderson cinematic techniques and prompting language.

This module encapsulates the core visual and narrative techniques associated with
Wes Anderson's distinctive style, optimized for use in AI video prompt engineering.

Key references drawn from analysis of films including The Grand Budapest Hotel,
Moonrise Kingdom, The Royal Tenenbaums, and The French Dispatch.
"""


class WesAnderson:
    """Signature techniques and prompting patterns for Wes Anderson style.

    Provides structured access to planimetric composition, dollhouse framing,
    color theory, performance style, and camera behavior typical of Anderson's work.
    """

    # Core visual and narrative signatures
    SIGNATURE_TECHNIQUES = [
        "Planimetric composition + perfect symmetry (camera perpendicular to scene planes)",
        "Dollhouse framing / frontal staging (theatrical, constructed depth)",
        "Controlled, vibrant color palettes (often pastel or primary with high saturation)",
        "Meticulous production design (every object intentional and symmetrical)",
        "Deadpan performance + slow, mechanical camera movement",
        "Whip pans and compass-point editing in 90-degree increments",
        "Symmetrical one-point perspective and clinical detachment",
    ]

    @staticmethod
    def get_core_principles() -> str:
        """Returns a concise summary of Anderson's core cinematic principles."""
        return (
            "Anderson's style emphasizes artifice and control. The camera is often static or moves "
            "laterally/vertically in flat space. Symmetry is used as both aesthetic and thematic device. "
            "Color is highly controlled and symbolic. Performances are stylized and deadpan, creating "
            "emotional distance that contrasts with the characters' inner turmoil."
        )

    @staticmethod
    def get_prompting_language(style: str = "standard") -> str:
        """Returns ready-to-use prompting language for Wes Anderson style shots.

        Args:
            style: "standard", "dollhouse", "symmetrical", or "whip_pan"
        """
        prompts = {
            "standard": (
                "Planimetric symmetrical composition with perfect frontal staging and horizontal layering, "
                "Wes Anderson-style dollhouse framing, vibrant controlled pastel palette, deadpan performance."
            ),
            "dollhouse": (
                "Dollhouse framing with perfect frontal staging, characters arranged in horizontal layers, "
                "vibrant but controlled color palette, meticulous production design, slow mechanical camera if movement."
            ),
            "symmetrical": (
                "Perfectly symmetrical one-point perspective, clinical detachment, characters centered in frame, "
                "high saturation pastel colors, slow deliberate camera movement maintaining composition."
            ),
            "whip_pan": (
                "Static symmetrical wide shot, sudden whip pan in 90-degree increments to reveal new symmetrical composition, "
                "Wes Anderson color palette and production design."
            ),
        }
        return prompts.get(style, prompts["standard"])

    @staticmethod
    def get_example_shot(description: str = "") -> str:
        """Returns an example shot description incorporating Anderson techniques."""
        base = (
            "Static wide shot, perfectly symmetrical framing, characters centered or arranged in horizontal layers, "
            "vibrant but controlled pastel color palette, meticulous and intentional production design, "
            "deadpan performances, slow mechanical tracking if any camera movement occurs."
        )
        if description:
            return f"{base} {description}"
        return base

    @staticmethod
    def get_negative_space_guidance() -> str:
        """Guidance on using negative space in Anderson-inspired compositions."""
        return (
            "While Anderson often fills the frame with symmetrical elements, negative space can be used "
            "strategically to emphasize isolation or absurdity. Maintain strong horizontal layering and "
            "avoid breaking the planimetric plane unless for deliberate comic or dramatic effect."
        )
