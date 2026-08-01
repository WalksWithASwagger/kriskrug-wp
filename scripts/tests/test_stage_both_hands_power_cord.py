from pathlib import Path
import importlib.util


SCRIPT = Path(__file__).parents[1] / "stage_both_hands_power_cord.py"
SPEC = importlib.util.spec_from_file_location("stage_both_hands_power_cord", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


def test_render_gutenberg_builds_video_and_policy_list():
    body = """# Title

## Subtitle

## Watch

https://www.youtube.com/watch?v=n_aGBFGnPzo

1. **One.** First term.

2. **Two.** Second term.
"""

    html = MODULE.render_gutenberg(body, "Subtitle")

    assert html.count('providerNameSlug":"youtube"') == 1
    assert html.count("<li>") == 2
    assert '<strong>One.</strong>' in html
    assert "<h1" not in html


def test_render_gutenberg_keeps_internal_and_external_link_rules():
    body = """# Title

## Subtitle

[Home](https://kriskrug.co/) and [IEA](https://www.iea.org/).
"""

    html = MODULE.render_gutenberg(body, "Subtitle")

    assert 'href="https://kriskrug.co/">Home</a>' in html
    assert 'href="https://www.iea.org/" target="_blank" rel="noopener noreferrer">IEA</a>' in html
