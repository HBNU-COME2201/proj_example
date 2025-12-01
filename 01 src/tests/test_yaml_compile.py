from polyprompt.prompt_manager import build_from_folder

def test_yaml_build_and_derived_override():
    prompts = build_from_folder("prompts")
    assert "summarize.base" in prompts
    assert "summarize.legal" in prompts
    p = prompts["summarize.legal"]
    txt = p.render(text="abc", length=80)
    assert "legal summarizer" in txt
    assert "Summarize the following text in 80 words" in txt
