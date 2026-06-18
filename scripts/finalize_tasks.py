"""Hand-author specimen `final_answer` strings for skeleton tasks.

A specimen answer is what a knowledgeable human would write for the task.
It is *illustrative*, not ground truth — the `final_answer_check` is the
authoritative grader. Re-runnable: this script is idempotent (it only
writes a `final_answer` field if one is absent, so re-runs don't clobber
edits you've made by hand).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


# Specimen answer per task. Tied to the drift-resistant needles in
# `final_answer_check.value` so a real answer naturally contains them.
ANSWERS: dict[str, str] = {
    # ---------- search ----------
    "current-weather-sf": (
        "San Francisco current weather (per weather.com): 64°F, partly cloudy, "
        "humidity 71%, wind 12 mph from the west. (Snapshot 2026-06.)"
    ),
    "stock-price-apple": (
        "AAPL last trade $214.32 (Yahoo Finance, 2026-06-17 close). "
        "Day range $212.40–$216.10, market cap ~$3.21T."
    ),
    "ceo-of-nvidia": (
        "Jensen Huang is the President and CEO of NVIDIA, a co-founder of the "
        "company in 1993, and has served as CEO since inception (January 1993)."
    ),
    "world-cup-2026-host": (
        "The 16 host cities for the 2026 FIFA World Cup (USA/Canada/Mexico) "
        "include Atlanta, Boston, Dallas, Houston, Kansas City, Los Angeles, "
        "Miami, Monterrey, New York/New Jersey, Philadelphia, San Francisco, "
        "Seattle, Toronto, Vancouver, Guadalajara, and Mexico City."
    ),
    "distance-earth-moon": (
        "Mean distance Earth–Moon: 384,400 km (≈238,855 miles). "
        "Perigee ~363,300 km, apogee ~405,500 km. (Wikipedia, Moon.)"
    ),
    "bitcoin-price-now": (
        "Bitcoin (BTC) spot price: $67,420 USD (CoinDesk index, 2026-06-17). "
        "24h range $66,890–$68,012, market cap ~$1.33T."
    ),
    "definition-rag": (
        "Retrieval-Augmented Generation (RAG) is a generation approach that "
        "conditions a sequence-to-sequence model on documents retrieved from "
        "an external corpus at inference time, so the model's output is "
        "grounded in up-to-date or domain-specific knowledge. "
        "Original paper: Lewis et al., 2020 (arXiv:2005.11401)."
    ),
    "python-latest-version": (
        "Latest stable Python release at time of writing: Python 3.12.x "
        "(3.12.3 as of 2024-04; 3.13 in pre-release). Supports back to 3.9."
    ),
    "iphone-latest-model": (
        "Apple's currently-shipping flagship iPhone: iPhone 16 Pro and iPhone "
        "16 Pro Max. iPhone 16 Pro starts at $999, Pro Max at $1,199 "
        "(apple.com/iphone)."
    ),
    "top-imdb-movie": (
        "Current #1 on IMDb Top 250: The Shawshank Redemption (1994), "
        "rating 9.3, 2.8M votes. The Godfather (9.2) and The Dark Knight "
        "(9.0) follow."
    ),
    "us-president-current": (
        "The current US President is Donald J. Trump, inaugurated for his "
        "second term on January 20, 2025 (whitehouse.gov)."
    ),
    "hubble-telescope-launch": (
        "The Hubble Space Telescope was launched on April 24, 1990 aboard "
        "Space Shuttle Discovery (STS-31) and deployed the following day."
    ),
    "average-coffee-price": (
        "Average price of a regular latte in New York City: $5.20 USD "
        "(Numbeo mid-2025 estimate, range $4.50–$6.00)."
    ),
    "webb-telescope-first-image": (
        "JWST's first publicly-released deep-field image was released on "
        "July 11, 2022: galaxy cluster SMACS 0723 as it appeared 4.6 billion "
        "years ago. (NASA, ESA, CSA.)"
    ),

    # ---------- shopping ----------
    "running-shoes-under-100": (
        "ASICS Gel-Contend 9, $79.99, 4.5★ on REI, available in standard "
        "US men's sizes. Also consider Brooks Trace 3 at $84.95 (4.6★)."
    ),
    "noise-cancelling-headphones": (
        "Sony WH-1000XM5, $328 (often discounted to $278 on Amazon), active "
        "noise cancellation, Bluetooth multipoint, 30h battery. (RTINGS top "
        "ANC pick under $300.)"
    ),
    "espresso-machine-home": (
        "Breville Bambino Plus, $499 (frequently $399 on Amazon), 4.7★, "
        "includes auto-frothing wand. Under the $500 ceiling when on sale."
    ),
    "4k-monitor-27in": (
        "Dell U2723QE 27\" 4K IPS, $429, USB-C hub, 4.5★. Strong text-clarity "
        "rating on RTINGS for coding. Also consider LG 27UP850 at $399."
    ),
    "gift-under-50-mom": (
        "Burpee Self-Watering Tomato Planter Kit, $32.98, 4.6★, Prime "
        "eligible. (Amazon gardening-for-mother category top pick.)"
    ),
    "laptop-stand-ergonomic": (
        "Rain Design mStand, $49.99, 4.7★, fits up to 17\" laptops. "
        "Adjustable height via riser; aluminum single-piece construction."
    ),
    "electric-toaster-4-slice": (
        "Cuisinart CPT-180, $79.95, 4.5★, 4-slot, brushed stainless. "
        "Also: Breville BTA730 ($99, 4.6★)."
    ),
    "air-purifier-large-room": (
        "Coway Airmega 400, $239 (under $250), covers 1,560 sq ft, True "
        "HEPA, 4.6★. (Amazon large-room top pick.)"
    ),

    # ---------- research ----------
    "rags-original-paper": (
        "Lewis, P., et al. (2020). 'Retrieval-Augmented Generation for "
        "Knowledge-Intensive NLP Tasks.' arXiv:2005.11401. Introduces RAG, "
        "a general-purpose fine-tuning recipe that pre-trains a BART "
        "generator with a neural retriever over Wikipedia."
    ),
    "mamba-paper": (
        "Gu, A. and Dao, T. (2023). 'Mamba: Linear-Time Sequence Modeling "
        "with Selective State Spaces.' arXiv:2312.00752. Introduces "
        "selective state-space models that match or exceed Transformers on "
        "language modeling while scaling linearly in sequence length."
    ),
    "mixture-of-experts-survey": (
        "Recent MoE survey: 'A Survey on Mixture of Experts' (arXiv:2407.06204, "
        "2024). Sections: (1) MoE fundamentals, (2) routing mechanisms, "
        "(3) training and inference, (4) applications to LLM and multimodal, "
        "(5) open problems."
    ),
    "diffusion-models-history": (
        "Ho, J., Jain, A., and Abbeel, P. (2020). 'Denoising Diffusion "
        "Probabilistic Models.' arXiv:2006.11239 (NeurIPS 2020). Trained on "
        "CIFAR-10, LSUN, and ImageNet 256×256; achieves FID 3.17 on "
        "ImageNet, comparable to SOTA GANs at the time."
    ),
    "llama-3-paper": (
        "Dubey, A. et al. (2024). 'The Llama 3 Herd of Models.' "
        "arXiv:2407.21783. Released 8B and 70B chat models trained on 15.6T "
        "tokens, plus the larger 405B. Llama 3 70B scores 86.0 on MMLU "
        "(5-shot) per the report."
    ),
    "agentbench-related": (
        "Liu, X. et al. (2023). 'AgentBench: Evaluating LLMs as Agents.' "
        "arXiv:2308.03688. Eight environments across web, code, game, "
        "knowledge-graph, OS, database, shopping, and trading; finds GPT-4 "
        "outperforms open models by a large margin."
    ),
    "openai-o1-report": (
        "OpenAI (2024). 'OpenAI o1 System Card.' Key safety findings: "
        "(1) o1 substantially outperforms GPT-4o on internal bio/chem "
        "captcha-style evals, (2) jailbreak robustness improved via "
        "chain-of-thought monitoring, (3) deliberate 'deliberative "
        "alignment' reduces reward hacking in long-horizon tasks."
    ),
    "gemini-1-5-report": (
        "Gemini Team, Google (2024). 'Gemini 1.5: Unlocking Multimodal "
        "Understanding Across Millions of Tokens of Context.' "
        "arXiv:2403.05530. Gemini 1.5 Pro supports a 1M-token context "
        "window (with 2M in preview for 1.5 Flash), the longest of any "
        "production model at release."
    ),
    "speech-recognition-benchmarks": (
        "LibriSpeech (Panayotov et al., 2015): ~1,000 hours of read English "
        "audio from public-domain audiobooks (LibriVox). License: CC BY 4.0 "
        "for annotations, public domain for audio.\n"
        "Common Voice (Mozilla): crowdsourced multilingual speech, ~30,000+ "
        "hours across 100+ languages by 2024. License: CC0.\n"
        "Differences: LibriSpeech = read speech, single language, audio is "
        "public domain. Common Voice = read + spontaneous, 100+ languages, "
        "CC0 across the board."
    ),

    # ---------- productivity ----------
    "cal-event-create": (
        "Event created: 'Project sync' on Monday 2026-06-22, 14:00–14:30, "
        "Google Calendar (default calendar). Confirmation email sent to "
        "invitees."
    ),
    "gmail-unsubscribe": (
        "Unsubscribed from a promotional email via the Gmail 'Unsubscribe' "
        "header link; the sender is now blocked from sending to this address. "
        "Email remains in the inbox; deletion is a separate step."
    ),
    "drive-share-folder": (
        "Created folder 'AgentBench-K reports' in Drive root, shared with "
        "the requested email at Viewer permission. Share link: "
        "https://drive.google.com/drive/folders/<id>."
    ),
    "notion-template": (
        "Free public Notion OKR template: 'OKRs' by Notion (notion.so/"
        "templates/okrs). Tracks Objectives, Key Results, and progress "
        "percentage. Also recommended: 'Team OKR Tracker' by Thomas Frank."
    ),
    "translate-fr-en": (
        "DeepL French→English: 'Research in artificial intelligence is "
        "advancing rapidly.' (Source: deepl.com/translator.)"
    ),
    "weather-week": (
        "7-day Paris forecast (weather.com, 2026-06-18 onward): Mon 24°/14°, "
        "Tue 26°/15°, Wed 22°/13°, Thu 25°/16°, Fri 28°/17°, Sat 30°/19°, "
        "Sun 27°/16° (°C)."
    ),
    "recipe-chicken-thighs": (
        "Serious Eats 'Weeknight Skillet Chicken Thighs with Mustard and "
        "Shallots', 25 minutes, 4.8★ (320+ reviews). Boneless thighs, "
        "seared in cast iron, finished with a Dijon-shallot pan sauce."
    ),
    "pdf-compress-tool": (
        "Free local-processing PDF compressor: PDFsam Basic (desktop, open "
        "source, AGPL) or Stirling-PDF (self-hosted web UI). Avoids uploading "
        "to remote servers. Browser-based: Smallpdf's desktop app processes "
        "locally."
    ),
    "bookmark-manager": (
        "Privacy-respecting bookmark manager: Linkwarden (self-hosted, AGPL) "
        "— recommended in HN threads as a Pinboard alternative. End-to-end "
        "encryption available. Backup option: Shaarli (single-user, PHP)."
    ),
    "standing-desk-under-300": (
        "Vari Electric Standing Desk Converter, $279, 4.5★ on Amazon, "
        "Prime. Also: Flexispot M2B at $229 (4.4★, 32\" wide)."
    ),

    # ---------- developer ----------
    "github-trending-python": (
        "GitHub trending Python this week (snapshot 2026-06): "
        "(1) unsloth/unsloth — fast LLM fine-tuning, "
        "(2) openai/whisper — speech recognition, "
        "(3) langchain-ai/langgraph — agent orchestration."
    ),
    "stackoverflow-top-question": (
        "Top-voted Python question on Stack Overflow: 'Why is it string.join "
        "(list) instead of list.join(string)?' — asked by Alex Coventry, "
        "1,800,000+ score, tags: python string list join."
    ),
    "npm-package-readme": (
        "Install axios (npm): `npm install axios`. (Source: npmjs.com/"
        "package/axios README.)"
    ),
    "pypi-package-latest": (
        "Latest `requests` on PyPI: 2.32.3 (as of 2024-05). Supports Python "
        "3.8+. (Source: pypi.org/project/requests/.)"
    ),
    "git-clone-instructions": (
        "HTTPS clone URL: https://github.com/openai/whisper.git\n"
        "First three setup steps from the README:\n"
        "  1. `git clone https://github.com/openai/whisper.git`\n"
        "  2. `cd whisper && pip install -e .`\n"
        "  3. `whisper path/to/audio.mp3` (CLI) or `import whisper` (Python API)"
    ),
    "docker-hub-pull": (
        "Official Docker pull command (hub.docker.com/_/postgres):\n"
        "  `docker pull postgres:16`\n"
        "Or run directly: `docker run -d --name pg -e POSTGRES_PASSWORD=... -p 5432:5432 postgres:16`"
    ),
    "vscode-extension-install": (
        "Prettier – Code formatter (esbenp.prettier-vscode) on marketplace.\n"
        "Install via CLI: `code --install-extension esbenp.prettier-vscode`."
    ),
    "find-bug-in-snippet": (
        "Bug: when called with two strings, `add('a', 'b')` returns 'ab1' "
        "(string concatenation, not addition). The trailing `+ 1` is the "
        "defect: it silently misbehaves for strings and yields 'ab1'.\n"
        "Fix: validate the types explicitly and raise a TypeError when the "
        "inputs cannot be added. e.g.\n"
        "  if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):\n"
        "      raise TypeError('add() requires numbers')\n"
        "  return a + b"
    ),
    "rest-api-design": (
        "GitHub REST endpoint to list a user's public repositories:\n"
        "  GET /users/{username}/repos\n"
        "Example: GET https://api.github.com/users/torvalds/repos\n"
        "(Source: docs.github.com/en/rest/repos/repos.)"
    ),
    "kubernetes-get-pods": (
        "kubectl command to list all pods in all namespaces with their node "
        "names: `kubectl get pods -A -o wide`. (Source: kubernetes.io/docs/"
        "reference/generated/kubectl/kubectl-commands#get.)"
    ),
    "regex-email": (
        "Commonly-recommended simple email regex (Stack Overflow top answer, "
        "OWASP):\n"
        "  ^[\\w.+-]+@[\\w-]+\\.[\\w.-]+$\n"
        "Matches the vast majority of real-world addresses without trying to "
        "implement the full RFC 5322 grammar."
    ),
    "open-source-license": (
        "License of microsoft/TypeScript: Apache License 2.0 (LICENSE file at "
        "github.com/microsoft/TypeScript/blob/main/LICENSE)."
    ),
    "semver-meaning": (
        "SemVer (semver.org) rules:\n"
        "  MAJOR version: incompatible API changes,\n"
        "  MINOR version: new backward-compatible functionality,\n"
        "  PATCH version: backward-compatible bug fixes."
    ),
    "crash-interpretation": (
        "Diagnosis: `NameError: name 'x' is not defined` at line 5 means the "
        "script references a variable `x` that was never assigned, or "
        "references it before its assignment. Common causes: typo, missing "
        "`global x` declaration inside a function, or `x` defined inside a "
        "branch/scope that line 5 doesn't see.\n"
        "Fix: define `x` before line 5, check spelling, or import the name "
        "if it was meant to come from another module."
    ),
}


def main() -> int:
    from tasks import iter_tasks

    missing_specimen = []
    for t in iter_tasks():
        if t["id"] in ANSWERS:
            continue
        missing_specimen.append(t["id"])

    # Tasks authored in v0.1/v0.2 already carry a final_answer; this script only fills in skeletons.
    ALREADY_AUTHORED = {
        "good-first-issue-transcription-repo",
        "three-asr-low-resource-papers",
        "wikipedia-population-tokyo",
        "cheap-nonstop-nyc-london",
        "mechanical-keyboard-under-120",
    }
    real_missing = [tid for tid in missing_specimen if tid not in ALREADY_AUTHORED]
    if real_missing:
        print(f"WARN: {len(real_missing)} tasks have no specimen answer in this script:")
        for tid in real_missing:
            print(f"  - {tid}")
        print()
        print("Add them to ANSWERS in scripts/finalize_tasks.py and re-run.")
        return 1

    patched = 0
    skipped = 0
    all_paths = []
    for p in sorted(ROOT.rglob("tasks/**/*.json")):
        if p.name in {"schema.json", "all_tasks.json"}: continue
        all_paths.append(p)
    for p in all_paths:
        d = json.loads(p.read_text())
        if d["id"] not in ANSWERS:
            continue
        if "final_answer" in d:
            skipped += 1
            continue
        d["final_answer"] = ANSWERS[d["id"]]
        p.write_text(json.dumps(d, indent=2) + "\n")
        patched += 1

    print(f"patched {patched} tasks with specimen final_answer strings")
    print(f"skipped {skipped} tasks (already had a final_answer — preserved)")

    # Rebuild the bundled dataset
    all_tasks = []
    all_paths = []
    for p in sorted(ROOT.rglob("tasks/**/*.json")):
        if p.name in {"schema.json", "all_tasks.json"}: continue
        all_paths.append(p)
    for p in all_paths:
        if p.name in {"schema.json", "all_tasks.json"}: continue
        all_tasks.append(json.loads(p.read_text()))
    (ROOT / "tasks" / "all_tasks.json").write_text(json.dumps(all_tasks, indent=2) + "\n")
    print(f"rebuilt tasks/all_tasks.json with {len(all_tasks)} tasks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
