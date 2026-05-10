---
layout: post
title: Fuzzing and Fuzzer
description: 
date: 2026-05-09
categories: [BugBounty]
tags: [fuzzing,fuzzer]
---
<style>
  .point {
  color: #111111;
  font-weight: 700;
  text-decoration-line: underline;
  text-decoration-color: #dc2626;
  text-decoration-thickness: 2px;
  text-underline-offset: 3px;
}
.footnote-text {
  font-size: 0.9rem;
  color: #666666;
  margin-top: -4px;
  margin-bottom: 16px;
  line-height: 1.6;
}
</style>

## 1. Fuzzing이란?
Fuzzing은 프로그램에 <span class="point">변형된 값이나 정상적이지 않은 값</span>들을 계속 넣어보면서 프로그램의 예외나 크래시,보안 취약점을 찾는 소프트웨어 테스트 기법이다.  

예를 들어 이미지를 조금씩 줄이거나 늘리고, 픽셀단위를 변경하여 프로그램에 전송해보며 보안 취약점을 찾는 것이다.

fuzzing을 할때에는 사람이 직접 값을 변경하는 것이 아니라 Fuzzer라는 도구를 사용한다. 

---

## 2. Fuzzing과 관련된 용어 정리

| 구분          | 의미                                    |
| ----------- | ------------------------------------- |
| Fuzzing     | 변형된 입력을 자동으로 넣어 버그를 찾는 테스트 방법         |
| Fuzzer      | fuzzing을 실제로 수행하는 프로그램 또는 프레임워크       |
| Fuzz target | fuzzer가 테스트할 대상 함수, 라이브러리, 바이너리, 프로그램 |
| Corpus      | fuzzer가 참고하거나 점점 개선해 나가는 입력 샘플 모음     |
| Mutation    | 기존 입력값을 변형해 새로운 입력을 만드는 과정            |
| Coverage    | 입력이 프로그램 내부의 어느 코드 경로까지 실행했는지 나타내는 정보 |
| Crash       | 입력으로 인해 프로그램이 비정상 종료한 결과              |

<p class="footnote-text">
※ 추가설명 coverge : 예를 들어 5줄의 코드가 있을때 샘플 이미지의 픽셀을 10px로 변경한 경우에는 코드의 3번째줄까지만 실행되고, 픽셀을 4px로 변경한 경우 5번째줄까지 실행된다고 할때 coverge는 코드가 어디까지 실행되었는지를 나타내는 정보인 것이다. </p>

---

## 3. Fuzzig의 기본 동작과정
1. 먼저 테스트할 프로그램이나 함수를 선정한다.
2. 초기 입력값을 정한다.
3. fuzzer가 초기 입력값을 기준으로 값을 변경하여 생성한다.
4. 변경된 값을 프로그램에 넣어 실행시켜본다.
5. 크래시, timeout, 메모리 오류, assertion failure 등을 감지한다. 
* coverage-guided fuzzer라면 새 코드 경로를 발견한 입력을 저장한다.
6. 3,4번의 과정을 반복하며 더 깊은 경로를 탐색하고 오류를 찾는다.

---

## 4. Fuzzing을 통해 발견할 수 있는 오류 


| 발견 가능한 문제 | 설명 |
| --- | --- |
| Buffer overflow | 입력 길이를 제대로 검사하지 않아 메모리를 침범하는 문제 |
| Use-after-free | 해제된 메모리를 다시 사용하는 문제 |
| Null pointer dereference | NULL 포인터를 참조해 프로그램이 죽는 문제 |
| Integer overflow | 정수 계산이 범위를 넘어 잘못된 값이 되는 문제 |
| Assertion failure | 개발자가 가정한 조건이 깨지는 문제 |
| Hang / infinite loop | 특정 입력에서 프로그램이 멈추거나 무한 루프에 빠지는 문제 |
| Logic bug | 크래시는 없지만 비정상적인 동작을 하는 문제 |
| Parser bug | 파일, 네트워크 패킷, 프로토콜 파싱 중 발생하는 오류 |



특히 <span class="point">C언어처럼 메모리 안전성이 낮은 언어로 작성된 프로그램의 경우 fuzzing이 매우 효과적이다. </span>

> github oss-fuzz 자료에 따르면 2025년 5월 기준 1,000개 이상의 프로젝트에서 13,000개 이상의 취약점과 50,000개 이상의 버그를 찾고 수정하는 데 기여했다고 한다.


---

## 5. Fuzzig의 종류 
fuzzzig의 종류는 분류하는 기준에 따라 다양하게 나눌 수 있다. 이번 포스트에서 모든 종류의 fuzzig을 구체적으로 다룰 순 없기때문에 간략하게만 정리하였다. 

---

### 5.1 입력 생성 방식에 따른 분류 
1) Mutation-based fuzzing

Mutation-based fuzzing는 <span class="point">기존 입력값을 조금씩 변경하여 새로운 입력을 만드는 방식</span>이다. 
fuzzig이란 무엇인지 설명하며 들었던 예시가 바로 이 경우에 해당한다. 

**장점** : 구현이 쉽고, 실제 프로그램이 받아들이는 입력 형식에서 출발하기 때문에 어느 정도 유효한 입력을 만들기 쉽다. 
<p class="footnote-text">
※대표적으론 AFL++가 있다. </p>

**단점** : 입력 포맷이 매우 복잡하거나 엄격한 경우, 단순 변형만으로는 깊은 코드 경로까지 도달하기 어렵다. 

---

2) Generation-based fuzzing

Generation-based fuzzing은 <span class="point">입력 형식, 문법, 프로토콜 구조를 미리 정의해 두고 그 규칙에 맞춰 입력을 새로 생성하는 방식</span>이다. 

예를 들어 입력구조를 미리 알고 있다면 fuzzer가 그 구조를 유지하면서 필드 값만 비정상적으로 바꿀 수 있다. 

**장점** : 구조적으로 유효한 입력을 만들기때문에 더 깊은 경로로 접근할 수 있다. 

**단점** : 입력포멧에 대한 모델이나 문법을 직접 작성해야한다.

---

### 5.2 프로그램 내부 정보를 사용하는지에 따른 분류

1) Black-box fuzzing

Black-box fuzzing은 프로그램 내부 구조나 coverage 정보를 거의 보지 않고 <span class="point">입력과 결과만 관찰하는 방식</span>이다.

예를 들어 웹 사이트에 여러 http요청을 보내고, 응답을 확인하는 방식이다.

**장점** : 소스코드가 없어도 된다.

**단점** : 어떤 입력이 새로운 코드 경로를 탐색했는지 모르기 때문에 효율이 낮을 수 있다.

---

2) White-box fuzzing

White-box fuzzing은 소스코드, 제어 흐름, 조건문, symbolic execution 같은 <span class="point">내부 정보를 적극적으로 사용</span>한다.

symbolic execution 기반 fuzzing은 프로그램의 조건문을 분석해 “이 분기를 타려면 어떤 입력이 필요할까?”를 계산한다. 
<p class="footnote-text">
※symbolic execution 기반 fuzzing: 무작위 입력 기반의 퍼징(Fuzzing)과 코드의 논리적 경로를 분석하는 기호 실행의 장점을 결합한 고급 소프트웨어 보안 취약점 탐지 기술 </p>

**장점** : 깊은 경로을 탐색할 수 있다.

**단점** : 분석 비용이 크고, 실제 대형 프로그램에서는 path explosion 문제가 발생할 수 있다. 
<p class="footnote-text">
※path explosion(경로 폭발) 문제 : 기호 실행(Symbolic Execution)이나 정적 분석에서 프로그램의 제어 흐름 경로가 프로그램 크기 증가에 따라 기하급수적으로 늘어나 분석이 불가능해지는 근본적인 확장성 제한 문제 </p>

---

3) Grey-box fuzzing

Grey-box fuzzing은 내부 정보를 전부 분석하지는 않지만, coverage 같은 가벼운 실행 피드백을 활용한다.

---

### 5.3 Coverage 사용 여부에 따른 분류

1) Coverage-guided fuzzing

Coverage-guided fuzzer는 입력값을 넣어본 뒤, 그 입력이 <span class="point">새로운 코드 경로를 실행했는지</span> 확인한다.

그 후, 새로운 경로를 발견한 입력은 의미 있는 입력으로 판단하고 저장한다.
그리고 그 입력을 다시 변형해서 더 깊은 코드 경로를 탐색한다.

즉, 단순히 랜덤 값을 넣는 것이 아니라,

“이 입력이 새로운 코드를 실행했는가?”

를 기준으로 더 좋은 입력을 골라내는 방식이다.

**장점** : 무작위 fuzzing보다 더 깊은 코드 경로를 탐색하기 좋다.

---

### 5.4 실행 방식에 따른 분류
1) In-process fuzzing

In-process fuzzing은 fuzzer와 테스트 대상 코드가 <span class="point">같은 프로세스 안에서 실행</span>되는 방식이다.

예를 들어 라이브러리 함수나 parser 함수처럼, 입력 데이터를 받아 처리하는 코드를 테스트할 때 적합하다.
<p class="footnote-text">
※parser 함수: 입력된 데이터(문자열, 로그, 코드 등)를 분석하여 구조화된 형태(JSON, 트리 등)로 변환하거나, 정의된 문법에 따라 의미 있는 데이터를 추출하는 함수 </p>

**장점**: 빠르다. 프로그램을 매번 새로 실행하지 않고 같은 프로세스 안에서 반복 실행하기 때문이다.

**단점**:  테스트 대상 코드가 전역 상태를 바꾸거나, 이전 입력의 영향이 다음 실행에 남으면 결과가 불안정할 수 있다.

---

2) Out-of-process fuzzing

Out-of-process fuzzing은 fuzzer가 테스트 대상 프로그램을 <span class="point">별도 프로세스로 실행</span>하는 방식이다.

**장점**: 실제 프로그램 실행 방식과 비슷하고, 프로그램이 크래시 나도 fuzzer 자체는 계속 동작할 수 있다

**단점**: 프로그램을 반복해서 실행해야 하므로 in-process 방식보다 느릴 수 있다.

---

## 6. 주요 Fuzzer 정리 

### 6.1 AFL++

AFL++는 대표적인 coverage-guided fuzzer이다.
기존 AFL을 발전시킨 도구로, 입력을 변형하면서 프로그램을 실행하고, 새로운 코드 경로를 발견한 입력을 저장한다.

| 항목    | 설명                                   |
| ----- | ------------------------------------ |
| 방식    | Coverage-guided fuzzing              |
| 입력 생성 | Mutation-based                       |
| 주요 대상 | C/C++ 프로그램, 실행 파일, 바이너리              |
| 장점    | 빠르고 실전에서 많이 사용됨                      |
| 특징    | QEMU mode, Frida mode 등 다양한 실행 방식 지원 |

<p class="footnote-text">
※QEMU mode : 최적화 기법으로, 퍼징 과정의 효율성을 크게 높이기 위해 프로그램을 반족적으로 재시작 하지 않고 지속적으로 실행하는 방식 </p>
<p class="footnote-text">
※소스코드가 없는 프로그램을 fuzzing할 수 있게 도와주는 AFL++의 실행 방식 </p>

---

### 6.2 libFuzzer

libFuzzer는 LLVM 프로젝트에서 제공하는 in-process coverage-guided fuzzer이다.

libFuzzer는 작은 함수나 라이브러리 내부 로직을 깊게 테스트할 때 적합하다.

<span class="point">AFL++가 프로그램 전체나 실행 파일을 대상으로 fuzzing하는 느낌이라면, libFuzzer는 보통 함수 단위로 fuzzing할 때 많이 사용된다. </span>

| 항목    | 설명                                  |
| ----- | ----------------------------------- |
| 방식    | In-process, coverage-guided fuzzing |
| 주요 대상 | 라이브러리 함수, parser 함수                 |
| 장점    | 빠르고 sanitizer와 함께 쓰기 좋음             |
| 단점    | fuzz target 코드를 직접 작성해야 함           |


---

### 6.3 Jackalope

Jackalope는 Google Project Zero에서 공개한 binary coverage-guided fuzzer이다.

가장 큰 특징은 <span class="point">소스코드가 없는 바이너리도 fuzzing할 수 있다는 점</span>이다.
Windows, macOS, Linux, Android 등 여러 환경을 지원한다.

| 항목    | 설명                                  |
| ----- | ----------------------------------- |
| 방식    | Binary coverage-guided fuzzing      |
| 주요 대상 | 소스코드가 없는 바이너리                       |
| 장점    | closed-source 프로그램 fuzzing 가능       |
| 단점    | 설정이 AFL++나 libFuzzer보다 어렵게 느껴질 수 있음 |


---

### 6.4 OSS-Fuzz
OSS-Fuzz는 fuzzer 자체라기보다는 Google이 운영하는 오픈소스 프로젝트용 continuous fuzzing 인프라이다.

즉, AFL++나 libFuzzer 같은 fuzzer를 사용해서 오픈소스 프로젝트를 지속적으로 테스트해주는 플랫폼이라고 볼 수 있다.

여러 fuzzer를 이용해 오픈소스 프로젝트를 계속 fuzzing하는 Google의 인프라이다.

| 항목          | 설명                            |
| ----------- | ----------------------------- |
| 성격          | Continuous fuzzing platform   |
| 대상          | 오픈소스 프로젝트                     |
| 사용하는 fuzzer | libFuzzer, AFL++, Honggfuzz 등 |
| 목적          | 프로젝트를 지속적으로 fuzzing하여 버그를 찾음  |

요약하자면 AFL++는 실행 파일이나 프로그램 fuzzing에 적합하고, libFuzzer는 함수 단위 fuzzing에 적합하다. Jackalope는 소스코드가 없는 바이너리를 fuzzing할 때 유용하며, OSS-Fuzz는 개별 fuzzer가 아니라 여러 fuzzer를 활용해 오픈소스 프로젝트를 지속적으로 테스트하는 인프라이다.

---

## 7. Fuzzing에서 꼭 알아야하는 개념

### 7.1 Harness

Harness는 fuzzer가 테스트 대상 코드를 호출할 수 있도록 연결해주는 코드이다.

예를 들어 어떤 이미지 파서 함수를 fuzzing하고 싶다면, fuzzer가 만든 입력 데이터를 그 파서 함수에 넘겨주는 코드가 필요하다.
이런 중간 연결 코드를 harness라고 한다.

---

### 7.2 Corpus

Corpus는 fuzzing에 사용할 입력 샘플 모음이다.

처음부터 완전히 랜덤한 입력만 사용하는 것보다, <span class="point">정상적인 샘플 파일 몇 개를 seed corpus로 주면 fuzzing 효율이 좋아진다. </span>

예를 들어 PNG 파서를 fuzzing한다면 정상 PNG 파일 몇 개를 corpus로 넣어두고, fuzzer가 그것을 변형하면서 테스트할 수 있다.

---

### 7.3 Sanitizer

Sanitizer는 프로그램 실행 중 발생하는 메모리 오류나 정의되지 않은 동작을 감지해주는 도구이다.

Fuzzing은 sanitizer와 함께 사용할 때 프로그램이 <span class="point">바로 크래시 나지 않더라도 내부의 위험한 동작을 잡아낼 수 있다.</span>

---


### 7.4 Crash triage

Fuzzer가 crash를 찾았다고 해서 바로 끝나는 것은 아니다.
<span class="point">찾은 crash가 어떤 문제인지 **분석하는 과정**</span>이 필요하다.

이를 crash triage라고 한다.

crash triage과정 
1. crash가 재현되는지 확인한다.
2. 같은 원인의 중복 crash인지 확인한다.
3. crash input을 줄인다.
4. stack trace와 sanitizer 로그를 확인한다.
5. 실제 보안 취약점인지 판단한다.

---

## 8.결론
Fuzzing은 프로그램에 다양한 입력값을 자동으로 넣어보면서 crash, memory error, hang 같은 문제를 찾는 테스트 기법이다. 처음에는 단순히 랜덤 값을 넣는 테스트라고 생각했지만, 그 종류가 목적에 따라 정말 다양하고, 각각의 장단점을 공부해보니 어디에 어떤 퍼징을 사용하는지가 매우 중요하다는 생각이 들었다.

AFL++는 실행 파일이나 프로그램을 대상으로 fuzzing하기 좋고, libFuzzer는 함수 단위 fuzzing에 적합하다. Jackalope는 소스코드가 없는 바이너리를 대상으로 fuzzing할 때 유용하다. 또한 OSS-Fuzz는 개별 fuzzer가 아니라 여러 fuzzer를 활용해 오픈소스 프로젝트를 지속적으로 테스트하는 인프라이다.

결국 fuzzer마다 목적과 사용 환경이 다르기 때문에, 소스코드가 있는지, 함수 단위로 테스트할 것인지, 바이너리를 대상으로 할 것인지에 따라 적절한 도구를 선택해야 한다.

---

## 참고 자료

- AFL++ 공식 GitHub: https://github.com/AFLplusplus/AFLplusplus
- AFL++ 공식 문서: https://aflplus.plus/docs/
- Jackalope 공식 GitHub: https://github.com/googleprojectzero/Jackalope
- Google Fuzzing Tutorial: https://github.com/google/fuzzing
- libFuzzer 공식 문서: https://llvm.org/docs/LibFuzzer.html
- OSS-Fuzz 공식 GitHub: https://github.com/google/oss-fuzz
- OSS-Fuzz 공식 문서: https://google.github.io/oss-fuzz/
- OWASP Fuzzing: https://owasp.org/www-community/Fuzzing