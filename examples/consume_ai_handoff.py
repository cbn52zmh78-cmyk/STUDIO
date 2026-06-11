# Consume AI Federation Handoff Example

"""Example showing how STUDIO consumes a prepared animation package from the Visualization Federation."""

from studio.cinematic_styles import ImpastoStyle, FreeCamStyle, NegativeSpaceStyle


def consume_federation_handoff(studio_package: dict):
 print("=== STUDIO: Consuming AI Federation Handoff ===")
 print(f"Source: {studio_package.get('source')}")
 print(f"Task: {studio_package.get('task')}")
 print(f"Cinematic Style Requested: {studio_package.get('cinematic_style')}")
 
 # Apply STUDIO cinematic styles
 impasto = ImpastoStyle(texture_strength=0.9)
 free_cam = FreeCamStyle(dolly_speed=0.4)
 negative_space = NegativeSpaceStyle(emphasis=0.75)
 
 print("\nApplying cinematic styles...")
 print(f"Impasto: {impasto}")
 print(f"Free Cam: {free_cam}")
 print(f"Negative Space: {negative_space}")
 
 print("\nReady for rendering with STUDIO pipeline.")
 return {"status": "ready_for_render", "styles_applied": [impasto, free_cam, negative_space]}