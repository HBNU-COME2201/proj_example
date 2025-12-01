# Project Example: PolyPrompt — Prompt as Python Object
PolyPrompt는 프롬프트를 불변(immutable) 파이썬 객체로 모델링하고, YAML 기반 Base/Derived 정의를 타입 검증 가능한 Prompt 인스턴스로 컴파일하여 재사용성, 전문화, 거버넌스, 테스트 가능성을 극대화하는 프레임워크입니다. 캡슐화, 상속, 합성, 다형성 등 객체지향 원칙을 적용해 연구, 산업 환경에서 일관된 프롬프트 운영을 지원합니다.
 본 프로젝트는 소프트웨어설계 수업의 예시 프로젝트로 `before` 브랜치는 소프트웨어 디자인 패턴이 적용되지 않은 프로젝트에 대한 내용을 담고 있으며 `after` 브랜치는 소프트웨어 디자인 패턴이 적용되지 않은 프로젝트에서 리팩토링을 통하여 개선된 프로젝트를 담고 있습니다. 

## 설치 및 빠른 시작
```bash
# (선택) 가상환경
python -m venv .venv && . .venv/bin/activate      # Windows: .venv\Scripts\activate

# 개발 모드 설치
pip install -e .[dev]

# 테스트
pytest -q

# 예제 실행
python examples/run_summarize.py
```

## 디렉토리 구조
```bash
polyprompt/
  core.py           # Prompt/Section/SlotSchema (불변 객체, render/infer)
  sections.py       # System/Instruction/Constraint/Example 섹션 (Composite)
  strategies.py     # OpenAIInferencer(모의), JSONParser(예시)
  registry.py       # PromptRegistry (name:version)
  prompts.py        # 예시 Prompt 객체
  prompt_manager.py # YAML 로더/상속 병합/컴파일 (Base/Derived)
  schemas/
    prompt_spec.py  # Base/Derived YAML 스키마(Pydantic)

prompts/
  summarize.base.yaml     # Base 예시
  summarize.legal.yaml    # Derived 예시

tests/
  test_summarize.py
  test_yaml_compile.py    # YAML 빌드 E2E 테스트 (권장)
```