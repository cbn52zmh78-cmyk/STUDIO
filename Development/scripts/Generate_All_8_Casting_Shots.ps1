# Generate_All_8_Casting_Shots.ps1
# Prepares prompts and folders for all 8 actresses in Studio/actors_roster.
# Image generation: run this script via Grok agent (casting-shot workflow) to create files.

$ErrorActionPreference = "Stop"
$StudioRoot = Split-Path $PSScriptRoot -Parent
$Root = Join-Path $StudioRoot "actors_roster"
$Subfolders = @(
    "01_casting_shots", "02_wardrobe_tests", "03_scenes", "04_promo", "05_reference"
)

$Actresses = [ordered]@{
    "Eleanor_Whitlock" = "casting shot 31-year-old White British woman with fair porcelain skin, light freckles, oval face, high cheekbones, straight narrow nose, full lips, defined jawline, bright blue-green eyes, shoulder-length wavy ash-blonde hair, slim athletic build, wearing a high-waisted black bikini, professional casting shot reference, photorealistic, studio lighting"
    "Rachel_Cohen" = "casting shot 36-year-old Jewish-American woman with warm olive skin, heart-shaped face, prominent cheekbones, slightly prominent nose, full plush lips, large dark brown eyes, voluminous dark wavy hair, curvy hourglass build, wearing a high-waisted emerald green bikini, professional casting shot reference, photorealistic, studio lighting"
    "Aiko_Nakamura" = "casting shot 26-year-old Japanese-American woman with smooth fair-to-light olive skin, heart-shaped face, small straight nose, almond-shaped dark brown eyes, straight jet-black silky hair in a long bob, petite athletic build, wearing a high-waisted navy blue bikini, professional casting shot reference, photorealistic, studio lighting"
    "Zara_Adebayo" = "casting shot 28-year-old Nigerian-American woman with rich deep brown skin, oval face, broad nose, full plump lips, large expressive dark brown eyes, voluminous coiled hair, athletic curvy build, wearing a high-waisted burgundy bikini, professional casting shot reference, photorealistic, studio lighting"
    "Isabella_Vargas" = "casting shot 29-year-old Mexican-American woman with warm golden olive skin, round-to-oval face, straight nose, full heart-shaped lips, warm hazel-brown eyes, long thick wavy dark brown hair, soft hourglass build, wearing a high-waisted terracotta bikini, professional casting shot reference, photorealistic, studio lighting"
    "Priya_Malhotra" = "casting shot 37-year-old Indian-American woman with medium warm brown skin, oval face, elegant high cheekbones, straight refined nose, full shaped lips, large almond-shaped deep brown eyes, long straight black hair, elegant slim-curvy build, wearing a high-waisted deep teal bikini, professional casting shot reference, photorealistic, studio lighting"
    "Nadia_Okoro" = "casting shot 42-year-old Nigerian-British woman with rich deep ebony skin, strong oval face, broad nose, full lips, large expressive dark brown eyes, short cropped natural hair, powerful athletic-curvy build, wearing a high-waisted black bikini, professional casting shot reference, photorealistic, studio lighting"
    "Valentina_Moreau" = "casting shot 47-year-old French-Algerian American woman with warm olive skin, elongated oval face, straight refined nose, full expressive lips, large almond-shaped hazel-green eyes, shoulder-length wavy dark chestnut hair with natural silver strands, elegant mature hourglass build, wearing a high-waisted deep wine red bikini, professional casting shot reference, photorealistic, studio lighting"
}

New-Item -ItemType Directory -Force -Path "$Root\female", "$Root\male", "$Root\transgender" | Out-Null

Write-Host "=== Generate All 8 Casting Shots ===`n"

foreach ($name in $Actresses.Keys) {
    foreach ($sub in $Subfolders) {
        New-Item -ItemType Directory -Force -Path (Join-Path $Root "female\$name\$sub") | Out-Null
    }

    $promptText = $Actresses[$name]
    $outDir = Join-Path $Root "female\$name\01_casting_shots"
    $promptFile = Join-Path $outDir "casting_prompt.txt"
    $imageFile = Join-Path $outDir "casting_turnaround_v1.jpg"

    Set-Content -Path $promptFile -Value $promptText -Encoding UTF8

    if (Test-Path $imageFile) {
        Write-Host "[OK] $name - casting_turnaround_v1.jpg exists"
    } else {
        Write-Host "[PENDING] $name - prompt saved, image pending generation"
        Write-Host "        $promptText"
    }
}

Write-Host "`nPrompts saved under Studio/actors_roster/female/*/01_casting_shots/"
Write-Host "Run via Grok agent to generate missing casting_turnaround_v1.jpg files."