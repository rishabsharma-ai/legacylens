"""The OKF bundle in knowledge/: valid pages, working links, and in sync with the graph."""

import re

import pytest
import yaml

from legacylens.okf import generate

PAGES = sorted(generate.OUT.rglob("*.md"))


def test_bundle_exists():
    assert (generate.OUT / "index.md").exists()
    assert len(PAGES) > 200


def test_every_page_has_frontmatter_with_type():
    for page in PAGES:
        text = page.read_text()
        assert text.startswith("---\n"), page
        meta = yaml.safe_load(text.split("---\n")[1])
        assert meta["type"], page
        assert meta["title"] and meta["description"], page


def test_every_internal_link_resolves():
    broken = []
    for page in PAGES:
        for target in re.findall(r"\]\(([^)]+)\)", page.read_text()):
            if target.startswith("http"):
                continue
            if not (page.parent / target.split("#")[0]).resolve().exists():
                broken.append(f"{page.relative_to(generate.OUT)} -> {target}")
    assert not broken, broken[:10]


def test_read_page_stays_inside_the_bundle():
    assert "error" in generate.read_page("../README.md")
    assert "POSTTRAN" in generate.read_page("jobs/POSTTRAN.md")["text"]


@pytest.mark.emulator
def test_committed_bundle_matches_the_graph(knowledge_db):
    """If this fails, the graph changed: run `make okf` and commit knowledge/."""
    pages = generate.build_pages(generate.load(knowledge_db))
    on_disk = {str(p.relative_to(generate.OUT)): p.read_text() for p in PAGES}
    assert sorted(pages) == sorted(on_disk)
    stale = [path for path, text in pages.items() if on_disk[path] != text]
    assert not stale, stale[:10]
