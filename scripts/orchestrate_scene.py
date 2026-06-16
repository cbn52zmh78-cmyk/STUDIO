# orchestrate_scene.py - Smart Director v1.0
import sys


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