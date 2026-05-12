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

## 1. Fuzzing(퍼징)이란?

Fuzzing은 자동화된 소프트웨어 테스트 기법으로, 프로그램에 무작위 데이터를 입력하여 소프트웨어의 crash, 메모리 누스 등의 상황을 테스트해 소프트웨어의 견고성을 높이는 데 사용된다. 
 
목적 : 데이터 생성(input)을 자동화하여 testing하고 버그를 유발하는 데이터를 찾는 것이다. 

fuzzing은 소스코드 없이도 버그를 찾을 수 있기때문에 요즘에는 버그를 찾는데 빠지지 않는 방법이다. 

가장 간단한 fuzzing의 예를 들어보겠다. 
```text
이미지를 입력받아 특정한 코드를 출력하는 프로그램이 있다고 하자. 
이때 fuzzing을 한다는 것은 이 프로그램에 이미지의 픽셀값을 조정하거나, 
크기를 늘리고 줄이는 등 데이터를 변경해 전송하여 버그를 찾아보는 것이다. 
```

## 2. Code Coverage이란?
fuzzing을 공부하게 되면 가장 먼저 배우게되는 것 중 하나가 바로 code coverage이다.

Code Coverage는 fuzzing을 할때 테스트가 프로그램의 코드를 얼마나 커버했는지 나타내는 지표이다. 
코드를 얼마나 커버했다는 뜻은 테스트를 할때 코드가 얼마나 실행되었는지를 나타낸다. 

>코드의 구조: 구문(statement),조건(condition),결정(desision)

code coverage에 대한 예시코드를 통해 정확한 개념을 이해해보자. 
코드의 구조에 따라서 어떤 식으로 쓰이는지 정리하였다. 

**Statement/Line**

```c
void test(int x)
{
  printf("Test Start!\n"); //case 1
  if (x>0) //case 2
    printf("x>0 \n"); //case 3
  printf("Test End \n"); //case 4
}
```
이러한 코드의 경우에 만약 input을 0을 준 경우에는 case 1, case2, case4만 실행되고 case 3은 실행되지 않는다. 
총 4줄의 코드중에 3줄이 실행되었기 때문에 code coverage는 75%라고 할 수 있다. 

**Condition**

```c
void test(int x, int y)
{
  printf("Test start! \n");
  if(x>0 && y<0)
    printf("x>0 \n");
  printf("Test End \n");
}
```
이 코드에서 code coverage를 만족시키는 input은 (1,1)이 있다. (1,1)은 x>0 조건의 경우 true/false를 만족하고, y<0 조건에서도 마찬가지이다. 
하지만 조건의 결과는 무조건 false를 반환한다. 

이를 통해 알 수 있는 사실은 condition에 대한 code coverage의 경우 if(x>0 && y<0)조건식의 최종 결과가 true/false인지에 관계없이 각 조건에 대한 입력값이 true/false를 만족하기만 하면 충족된다는 것이다. 

단, 주의할 점은 이 예시는 (1,1)입력의 경우 전체 code coverage가 충족되는 것이 아니다. if(x>0 && y<0) 조건식의 code coverage가 최종 결과와 관계없이 충족된다는 의미임을 오해하지 말자. 

**Desision/Branch** 

```c
void test(int x,int y)
{
  printf("Test Start \n");
  if ((x>0)&&(y>0))
    printf("x>0 \n");
  printf("Test End \n");
}
```
이 코드에서 code coverage를 만족시키려면 모든 조건식이 true/false를 가져야한다. 이를 충족하는 값은 (0,1)과 (1,1)이 있다. 
(1,1)의 경우 x>0조건에서 true, y>0조건에서 true를 가지므로 desision coverage를 만족한다. 
(0,1)의 경우 x>0조건에서 false을 가지므로 desision coverage를 만족한다.

여기서 헷갈리면 안되는 것이 앞서 설명한 condition의 경우와 달리 desision의 coverage는 전체 결과에 대해 true/false를 만족시키는 지 확인하는 것이다.  

| Coverage           | 보는 대상     | 만족 조건                                    |
| ------------------ | --------- | ---------------------------------------- |
| Decision coverage  | 전체 조건식 결과 | `x > 0 && y < 0`이 true/false 둘 다 나와야 함   |
| Condition coverage | 개별 조건 결과  | `x > 0`, `y < 0` 각각 true/false 둘 다 나와야 함 |

## 3. Fuzzing의 상황별 분류 

### 1. White-Box Testing
White-Box Testing은 소스코드를 가지고 있는 상태에서 할 수 있는 테스팅이다. 
> NIST공식자료에 따르면 평가 객체의 내부 구조와 구현 세부 사항에 대한 명시적이고 상당한 지식을 전제로 하는 테스트 방법론이라고 정의한다. 

소스코드, 설계, 아키텍처에 대한 정보를 통해 외부의 관점에서 테스팅이 가능하다. 
white box testing은 애플리케이션의 개별요소부터 전체 시스템까지 올바르게 동작하도록 보장한다. 

E또한 소스코드를 가지고 있기때문에 원하는 부분만 퍼징을 진행하거나, 필요한 부분을 패치해서 퍼징을 진행할 수 있다는 장점이 있다. 

아래의 화살표를 클릭하면 구체적인 설명을 볼 수 있다. 

<details>
<summary>White-Box Testing</summary>

</details>

### 2. Gray-Box Testing
Gray-Box Testing은 내부테서 사용하는 데이터 구조체 혹은 알고리즘에 대한 문서를 통해 내부 프로그램의 구조를 부분적으로 알고 Testing 하는 방법이다. 

간단한 예를 들어보자. 

```text
로그인 기능을 테스트한다고 할때 

테스터가 알고 있는 정보:

비밀번호는 서버에서 해시 처리되어 DB에 저장된다
로그인 실패가 5번 누적되면 계정이 10분간 잠긴다
로그인 API는 /login 엔드포인트를 사용한다

하지만 테스터가 모르는 정보:

실제 서버 코드 전체
정확한 해시 함수 구현 방식
내부 클래스 구조
전체 DB 스키마

이 상태에서 테스트를 진행하는 것이 gray-box testing이다. 

이런경우 **올바른 아이디 + 틀린 비밀번호로 4번 로그인 시도** 를 했을때 실패메시지가 나오는지, 

잠긴 직후 올바른 비밀번호 입력 → 로그인 실패, "계정 잠김" 메시지가 나오는지 등을 테스트해볼 수 있다. 

```
아래의 화살표를 클릭하면 구체적인 설명을 볼 수 있다. 

<details>
<summary>Gray-Box testing</summary>

</details>

### Black-Box Testing
소스코드를 가지고 있지 않은 상태에서 할 수 있는 테스팅이다. 
소스코드를 가지고 있지 않기 때문에 Binaray만을 이용하여 Testing한다. 

아래의 화살표를 클릭하면 구체적인 설명을 볼 수 있다. 

<details>
<summary>Gray-Box testing</summary>

</details>

## 4. Fuzzer란?
Fuzzer란 fuzzing을 자동으로 실행하고 테스트한 뒤 이상행위가 발생할 경우 해당 테스트 케이스를 저장하고 버그를 분류하는 자동화 fuzzing 도구이다.

### Fuzzer Architecture

**1.Test Case Generator**

Targe Program에 입력할 데이터를 생성한다. 
입력할 데이터를 생성하는 방식에 따라 2가지로 나뉜다.
1. Smart Fuzzer : 프로그램의 입력 데이터 구조를 파악하여 해당 구조에 맞게 Mutation을 진행한다. 
2. Dumb Fuzzer : 랜덤한 데이터를 생성하여 Mutation을 진행한다. 

> Mutation : 데이터를 랜덤 또는 정해진 규칙에 의해서 변경 후 테스트하는 것을 의미한다. 

**2. Logger** 
fuzzing을 돌리는 중 버그 혹은 이상행위 분석에 필요한 정보를 저장한다. 
Crash와 Test Case를 저장하며, Code Coverage-Based Fuzzer의 경우 새롭게 발견한 Code Coverage도 저장한다. 
이러한 Log를 혹인하여 Crash에 대한 분석을 진행하는 것이다. 

> Crash는 프로그램에 버그가 났을 경우 그 버그의 종류 등을 저장하는 것이고, Test case는 test case generator가 생성한 input이다.

**3. Worker**
Gernerator에서 생성한 입력 데이터를 받아 실행하고 이상행위를 탐지한다. 

### 대표적인 Fuzzer 종류

## 5. Fuzzing Case

### 1. Guided Fuzzing 
Test Case의 생성을 code coverage를 넓히기 위해서 사용하는 방법이다. test case에서 변경할 데이터를 정하고 그 부분의 데이터만 변경한다. 

code coverage가 높다는 말은 그만큼 더 많은 로직에 test case 입력되었다는 뜻이다. 
이것은 버그를 찾을 가능성이 높다는 의미이다. 

### 2. 
