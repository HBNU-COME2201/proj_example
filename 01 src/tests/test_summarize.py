from polyprompt.prompt_manager import build_from_folder

def test_render_snapshot():
    prompts = build_from_folder("prompts")
    p = prompts["summarize.base"]
    txt = p.render(text="abc", length=20)
    assert "Summarize the following text in 20 words" in txt
    assert "abc" in txt

def test_slot_validation_bounds():
    prompts = build_from_folder("prompts")
    p = prompts["summarize.base"]
    try:
        p.render(text="x", length=5)
        assert False, "should have failed length lower bound"
    except Exception as e:
        assert "length" in str(e).lower()
