# Consume AI Federation Handoff Example

"""Example showing how STUDIO consumes a prepared animation package from the Visualization Federation."""

import json
import os
from datetime import datetime

from studio.cinematic_styles import ImpastoStyle, FreeCamStyle, NegativeSpaceStyle


def consume_federation_handoff(studio_package: dict):
    print("=== STUDIO: Consuming AI Federation Handoff ===\n")
    
    # Extract key information from the AI package
    source = studio_package.get("source", "Unknown")
    task = studio_package.get("task", "Unknown task")
    cinematic_style = studio_package.get("cinematic_style", "default")
    frame_paths = studio_package.get("frame_paths", [])
    particle_data = studio_package.get("particle_data", {})
    ai_directives = studio_package.get("render_directives", {})
    
    print(f"Source: {source}")
    print(f"Task: {task}")
    print(f"Cinematic Style Requested: {cinematic_style}")
    print(f"Frames received: {len(frame_paths)}")
    print(f"Particle data keys: {list(particle_data.keys()) if particle_data else 'None'}")
    
    # Apply STUDIO cinematic styles (enhanced application)
    impasto = ImpastoStyle(texture_strength=0.9)
    free_cam = FreeCamStyle(dolly_speed=0.4)
    negative_space = NegativeSpaceStyle(emphasis=0.75)
    
    print("\nApplying STUDIO cinematic styles...")
    print(f"  • Impasto: texture_strength={impasto.texture_strength}, brush_visible={impasto.brush_visible}")
    print(f"  • FreeCam: dolly_speed={free_cam.dolly_speed}, subtle_dolly={free_cam.subtle_dolly}")
    print(f"  • NegativeSpace: emphasis={negative_space.emphasis}")
    
    # Merge directives: AI directives + STUDIO styles
    merged_directives = {
        "source": source,
        "task": task,
        "cinematic_style": cinematic_style,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "studio_applied_styles": {
            "impasto": {
                "texture_strength": impasto.texture_strength,
                "brush_visible": impasto.brush_visible
            },
            "free_cam": {
                "dolly_speed": free_cam.dolly_speed,
                "subtle_dolly": free_cam.subtle_dolly
            },
            "negative_space": {
                "emphasis": negative_space.emphasis
            }
        },
        "ai_render_directives": ai_directives,
        "frame_count": len(frame_paths),
        "particle_data_summary": {
            "keys": list(particle_data.keys()) if isinstance(particle_data, dict) else "N/A",
            "count": len(particle_data) if isinstance(particle_data, (list, dict)) else 0
        }
    }
    
    # Save the merged render directives
    output_path = "render_directives.json"
    with open(output_path, "w") as f:
        json.dump(merged_directives, f, indent=2)
    
    print(f"\n✓ Merged render directives saved to: {os.path.abspath(output_path)}")
    
    print("\n=== STUDIO Summary ===")
    print(f"Received {len(frame_paths)} frames from AI Federation.")
    print(f"Applied STUDIO cinematic treatment for '{cinematic_style}' style.")
    print("Ready for high-end rendering pipeline with physics-accurate motion and visual storytelling intent.")
    
    return {
        "status": "ready_for_render",
        "output_file": output_path,
        "styles_applied": [impasto, free_cam, negative_space],
        "merged_directives": merged_directives
    }