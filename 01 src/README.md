# Project Example: PolyPrompt — Prompt as Python Object
PolyPrompt는 프롬프트를 불변(immutable) 파이썬 객체로 모델링하고, YAML 기반 Base/Derived 정의를 타입 검증 가능한 Prompt 인스턴스로 컴파일하여 재사용성, 전문화, 거버넌스, 테스트 가능성을 극대화하는 프레임워크입니다. 캡슐화, 상속, 합성, 다형성 등 객체지향 원칙을 적용해 연구, 산업 환경에서 일관된 프롬프트 운영을 지원합니다.
 본 프로젝트는 소프트웨어설계 수업의 예시 프로젝트로 `before` 브랜치는 소프트웨어 디자인 패턴이 적용되지 않은 프로젝트에 대한 내용을 담고 있으며 `after` 브랜치는 소프트웨어 디자인 패턴이 적용되지 않은 프로젝트에서 리팩토링을 통하여 개선된 프로젝트를 담고 있습니다. 

## 주요 특징
 - Prompt = 객체: Prompt(name, version, sections, slot_schema, parser)
 - 합성 가능한 섹션: System/Instruction/Constraint/Example(Composite 패턴)
 - 타입 검증: Pydantic으로 슬롯(입력 변수) 스키마 동적 생성
 - 전략 주입: 백엔드(Inferencer)·파서(Parser) 교체 가능(Strategy 패턴)
 - YAML 상속: Base/Derived YAML 정의 → 병합/검증 → Prompt로 컴파일
 - 테스트 용이성: 렌더 스냅샷·슬롯 검증·YAML 컴파일 E2E 테스트
 - 불변성/재현성: dataclass(frozen=True) 기반, render()는 순수 함수로 유지

## 요구 사항
 - Python 3.10 이상
 - pip (선택: venv, pytest, ruff, mypy)
