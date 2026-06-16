# Cinematic Style Systems

"""Core cinematic style definitions aligned with SPIT canon and AI Federation handoff."""

from dataclasses import dataclass

@dataclass
class ImpastoStyle:
 texture_strength: float = 0.85
 brush_visible: bool = True

@dataclass
class FreeCamStyle:
 dolly_speed: float = 0.3
 subtle_dolly: bool = True

@dataclass
class NegativeSpaceStyle:
 emphasis: float = 0.7

@dataclass
class DollhouseStyle:
 scale: float = 0.6
 intimacy: float = 0.9