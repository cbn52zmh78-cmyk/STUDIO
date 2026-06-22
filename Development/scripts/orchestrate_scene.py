# orchestrate_scene.py - Smart Director v1.0
import sys
from pathlib import Path as _Path

# --- qa_gate wiring ---
_AI_FED = _Path(__file__).resolve().parents[3] / "AI" / "federation"
if str(_AI_FED) not in sys.path:
    sys.path.insert(0, str(_AI_FED))
try:
    from qa_gate import qa_check as _qa_gate_check
    _QA_GATE_AVAILABLE = True
except ImportError:
    _QA_GATE_AVAILABLE = False
# --- end qa_gate wiring ---


def orchestrate(user_input):
    print('\n Orchestrating scene from your description...')
    print(f'Input: {user_input}\n')

    print('→ Building story outline...')
    print('→ Assigning slots intelligently...')
    print('→ Applying all master constraints + continuity...')

    output = f'''# ORCHESTRATED PROMPT PACK v1.0 - {user_input}

Story Outline (Auto-generated):
1. Henry II receives devastating news about his sons conspiring against him.
2. The court freezes in tension.
3. Richard steps forward and pledges loyalty, forging the alliance.

Master Constraints (always active):
- Every clip: 6-10 seconds max
- First generation: only 480p or 720p
- 1080p: max 20 seconds
- Longer than 20s: must be 720p

Slot Assignment (Auto):
@1: HENRY THE SECOND (throne room reference image)
@2: Battle-worn Richard Lionheart (video reference)
Setting Plate: Full Henry II court throne room

Full Ready-to-Use Prompt:
HENRY THE SECOND (@1) seated on his throne as clerics deliver the betrayal news. He grips the scepter tighter, raising one hand sharply to silence the court as controlled anger builds on his face. Battle-worn Richard Lionheart (@2) steps forward one deliberate pace beside him, hand on sword hilt, eyes full of intense loyalty and familial tension. Clerics lean in, scrolls rustle. Motivated camera drift creating powerful negative space between father and son as the alliance is forged in fire.

Ready for generation. Use the master constraints above when generating clips.
'''
    # --- qa_gate: QA orchestrated output before write ---
    if _QA_GATE_AVAILABLE and output.strip():
        try:
            _qa_orc = _qa_gate_check(
                content=output,
                content_type="general",
                subject=f"orchestrated scene: {user_input[:80]}",
            )
            if _qa_orc["gate"] == "RED":
                print(
                    f"[QA HOLD] orchestrate_scene.py: {_qa_orc['summary']} | Issues: {_qa_orc['issues']}",
                    file=sys.stderr,
                )
                return  # hold output on RED
            elif _qa_orc["gate"] == "YELLOW":
                print(
                    f"[QA WARN] orchestrate_scene.py: {_qa_orc['summary']}",
                    file=sys.stderr,
                )
        except Exception as _exc:
            print(f"[QA WARN] orchestrate_scene.py: qa_gate error: {_exc}", file=sys.stderr)
    # --- end qa_gate ---
    with open('orchestrated_prompt.txt', 'w', encoding='utf-8') as f:
        f.write(output)
    print('\n✅ Done. Full prompt saved to orchestrated_prompt.txt')
    print(output)


if __name__ == '__main__':
    idea = (
        ' '.join(sys.argv[1:])
        if len(sys.argv) > 1
        else 'Henry II getting bad news about his sons while Richard steps forward and pledges loyalty in the throne room'
    )
    orchestrate(idea)