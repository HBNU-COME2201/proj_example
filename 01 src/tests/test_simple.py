from polyprompt.simple import build_prompts, render

def test_simple_render():
    prompts = build_prompts("prompts")
    p = prompts["summarize.base"]
    txt = render(p, text="xyz", length=30)
    assert "Summarize the following text in 30 words" in txt
    assert "xyz" in txt
