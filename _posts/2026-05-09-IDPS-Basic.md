---
layout: post
title: "IDS/IPS란? 침입 탐지와 침입 방지 시스템의 이해"
description: "침입 탐지 및 방지 시스템(IDS/IPS)의 동작 원리, 유형, 활용 방법, 장단점, 차이점"
date: 2026-05-09
categories: [블로그]
tags: [IDPS, IPS, IDS]
---

<style>
.post-content table,
article table {
  width: 100%;
  border-collapse: collapse;
  margin: 16px 0;
  font-size: 0.95rem;
}

.post-content table th,
article table th {
  background-color: #f5f5f5;
  color: #222222;
  font-weight: 700;
}

.post-content table th,
.post-content table td,
article table th,
article table td {
  border: 1px solid #dddddd;
  padding: 10px 12px;
}

.post-content table tr:nth-child(even),
article table tr:nth-child(even) {
  background-color: #fafafa;
}

.point {
  color: #111111;
  font-weight: 700;
  text-decoration-line: underline;
  text-decoration-color: #dc2626;
  text-decoration-thickness: 2px;
  text-underline-offset: 3px;
}

.note-box {
  background: #fff8db;
  border-left: 4px solid #facc15;
  padding: 12px 16px;
  margin: 16px 0;
  border-radius: 8px;
}
.footnote-text {
  font-size: 0.9rem;
  color: #666666;
  margin-top: -4px;
  margin-bottom: 16px;
  line-height: 1.6;
}
</style>

## 침입탐지시스템(IDS, Intrusion Detection System)이란?

<span class="point">IDS</span>는 네트워크나 호스트에서 발생하는 이상 행위, 침입 시도, 보안 정책 위반 징후를 탐지하고 관리자에게 경고를 보내는 보안 시스템이다.

IDS는 일반적으로 네트워크 트래픽의 직접 경로가 아닌 <span class="point">미러링 포트</span>나 <span class="point">네트워크 TAP</span>에 배치되어 트래픽을 관찰한다.  
즉, 트래픽 흐름을 직접 차단하지 않고 관찰자 역할을 수행하기 때문에 서비스에 미치는 영향이 비교적 적다.

<p class="footnote-text">
※ 미러링 포트: 스위치의 특정 트래픽을 복사해 IDS로 보내는 포트 </p>

<p class="footnote-text">
※네트워크 TAP : 네트워크 회선 사이에서 트래픽을 복사해 모니터링 장비로 전달하는 장비
</p>

<div class="note-box">
<strong>핵심 정리</strong><br>
IDS는 침입을 직접 막기보다는 수상한 행위를 탐지하고 관리자에게 알려주는 역할을 한다.
</div>

---

## IDS의 유형

IDS는 기준에 따라 여러 유형으로 나눌 수 있다.

### 1. 탐지 위치에 따른 분류

| 유형 | 설명 |
| ---- | ---- |
| 네트워크 기반 IDS, NIDS | 네트워크 구간의 트래픽을 분석하여 침입 시도를 탐지 |
| 호스트 기반 IDS, HIDS | 서버나 PC 등 개별 호스트의 로그, 파일 변경, 프로세스 등을 분석 |
| 프로토콜 기반 IDS | 특정 프로토콜의 정상 동작 여부를 분석 |
| 애플리케이션 프로토콜 기반 IDS | HTTP, DNS, SMTP 등 애플리케이션 계층 프로토콜을 분석 |
| 하이브리드 IDS | 네트워크 기반과 호스트 기반 탐지를 함께 활용 |

### 2. 침입 판단 방식에 따른 분류

| 방식 | 설명 |
| ---- | ---- |
| 시그니처 기반 탐지 | 알려진 공격 패턴과 비교하여 침입 여부를 판단 |
| 이상 징후 기반 탐지 | 정상적인 동작 기준과 비교하여 비정상 행위를 탐지 |

---

## 침입방지시스템(IPS, Intrusion Prevention System)이란?

<span class="point">IPS</span>는 악성 트래픽을 탐지하는 것뿐만 아니라, 탐지된 위협을 실시간으로 차단하는 보안 시스템이다.

IPS는 일반적으로 네트워크 트래픽이 실제로 통과하는 <span class="point">인라인 경로</span>에 배치된다.  
따라서 트래픽을 실시간으로 검사하고, 악성으로 판단된 패킷을 차단하거나 세션을 종료할 수 있다.

즉, <span class="point">IDS</span>가 주로 “탐지와 경고”에 초점을 둔다면, <span class="point">IPS</span>는 “탐지와 차단”까지 수행한다.

<div class="note-box">
<strong>핵심 정리</strong><br>
IPS는 트래픽 경로에 직접 위치하여 악성 트래픽을 탐지하고, 필요하면 즉시 차단한다.
</div>

---

## IPS의 유형

IPS는 차단 판단 기준에 따라 다음과 같이 분류할 수 있다.

| 방식 | 설명 |
| ---- | ---- |
| 시그니처 기반 탐지 | 알려진 익스플로잇 패턴이나 공격 시그니처를 기준으로 차단 |
| 이상 징후 기반 탐지 | 네트워크 활동을 정상 기준선과 비교하여 비정상 행위를 탐지 |
| 정책 기반 탐지 | 관리자가 설정한 보안 정책과 규칙을 기준으로 차단 여부를 판단 |

---

## IDS와 IPS의 차이점

| 구분 | IDS | IPS |
| ---- | ---- | ---- |
| 주 역할 | 탐지 | 탐지 + 차단 |
| 동작 방식 | 수상한 행위를 발견하고 알림 | 수상한 행위를 발견하고 자동 대응 |
| 트래픽 처리 위치 | 보통 미러링 또는 모니터링 방식 | 보통 인라인 방식 |
| 대응 방식 | 경고, 로그 기록 | 차단, 세션 종료, 패킷 드롭 |
| 서비스 영향 | 직접 차단하지 않아 영향이 적음 | 오탐 시 정상 트래픽도 차단될 수 있음 |

<span class="point">IDS</span>와 <span class="point">IPS</span>는 역할에서 차이가 있지만, 실제 보안 제품에서는 두 기능이 함께 제공되는 경우가 많다.  
NIST SP 800-94에서도 IDS와 IPS를 <span class="point">IDPS(Intrusion Detection and Prevention System)</span>라는 하나의 큰 범주로 묶어 설명한다.

따라서 이 글의 이후 내용에서는 IDS와 IPS를 포괄하는 개념인 <span class="point">IDPS</span>를 기준으로 동작 원리와 활용 방법을 정리한다.

<div class="note-box">
<strong>정리하면</strong><br>
IDS는 탐지 중심, IPS는 탐지와 차단 중심이다. 두 기능을 통합한 개념을 IDPS라고 볼 수 있다.
</div>

---

## IDS/IPS의 공통점

IDS와 IPS는 모두 네트워크나 시스템에서 발생하는 이벤트를 분석하여 보안 위협을 탐지한다는 공통점이 있다.

| 공통 기술 | 설명 |
| -------- | ---- |
| 시그니처 기반 탐지 | 알려진 공격 패턴과 비교 |
| 이상 징후 기반 탐지 | 정상 상태와 비교하여 비정상 행위 탐지 |
| 상태 기반 프로토콜 분석 | 프로토콜의 정상 동작 절차와 비교 |
| 로그 분석 | 시스템 및 네트워크 기록 확인 |
| 알림 생성 | 관리자에게 보안 경고 전달 |

---

## 동작 원리 
![IPS-IDS 동작원리](./img/IPS-IDS.png)
이 그림은 IPS와 IDS의 동작원리를 쉽게 이해하기 위해 AI를 사용하여 그린 그림이다. 
IPS와 IDS의 동작원리의 차이점을 잘 보여준다. 

---

## 탐지 방법
IDS와 IPS는 기본적으로 네트워크나 시스템의 이벤트를 모니터링하고, 보안 정책 위반 징후를 분석한다는 점에서 유사한 탐지 방법론을 사용한다.

### 1. 서명 기반 탐지

<span class="point">서명 기반 탐지(Signature-Based Detection)</span>는 알려진 공격 패턴이나 악성 행위의 특징을 미리 정의해두고, 실제 이벤트와 비교하여 침입 여부를 판단하는 방식이다.

예를 들어 특정 악성코드의 패킷 패턴, 익스플로잇 코드, 공격 문자열 등이 시그니처로 등록되어 있다면, IDS/IPS는 이를 탐지하여 경고하거나 차단할 수 있다.

이 방식은 알려진 공격을 탐지하는 데 효과적이지만, 아직 시그니처가 등록되지 않은 새로운 공격이나 제로데이 공격에는 취약할 수 있다.

### 2. 이상 기반 탐지

<span class="point">이상 기반 탐지(Anomaly-Based Detection)</span>는 정상적인 사용자 행위나 네트워크 트래픽의 기준선을 설정한 뒤, 이 기준에서 크게 벗어나는 활동을 탐지하는 방식이다.

예를 들어 평소보다 비정상적으로 많은 로그인 시도, 갑작스러운 트래픽 증가, 일반적이지 않은 포트 접근 등이 이상 행위로 판단될 수 있다.

이 방식은 알려지지 않은 공격을 탐지할 가능성이 있지만, 정상적인 활동을 공격으로 잘못 판단하는 오탐이 발생할 수 있다.

### 3. 상태 보존 프로토콜 분석

<span class="point">상태 보존 프로토콜 분석(Stateful Protocol Analysis)</span>은 프로토콜의 정상적인 동작 절차와 상태를 기준으로 트래픽을 분석하는 방식이다.

예를 들어 TCP 연결 과정이나 애플리케이션 프로토콜의 정상적인 요청·응답 흐름을 추적하고, 이 흐름에서 벗어난 비정상적인 동작을 탐지한다.

이 방식은 프로토콜 오용이나 비정상적인 통신 흐름을 탐지하는 데 유용하지만, 상태를 계속 추적해야 하므로 리소스 사용량이 증가할 수 있다.

<div class="note-box">
<strong>탐지 방법 요약</strong><br>
서명 기반 탐지는 알려진 공격에 강하고, 이상 기반 탐지는 알려지지 않은 공격을 찾는 데 유리하다. 상태 보존 프로토콜 분석은 프로토콜의 정상 흐름과 비교하여 비정상 행위를 탐지한다.
</div>

---

## IDS/IPS의 활용 방법

IDS/IPS는 단순히 침입을 탐지하는 장비가 아니라, 기업과 클라우드 환경에서 보안 사고 대응, 정책 관리, 위협 분석 자동화에 활용되는 핵심 보안 시스템이다.

### 기업 환경에서의 활용

기업 환경에서는 네트워크 경계와 내부망에 IDS/IPS를 적절히 배치하여 외부 공격과 내부 이상 행위를 함께 탐지한다.

- 네트워크 경계에 <span class="point">IPS</span>를 배치하여 악성 트래픽을 실시간으로 차단한다.
- 내부 네트워크에서는 <span class="point">IDS</span>를 활용하여 비정상적인 접근, 이상 행동, 악성 트래픽을 탐지한다.
- 보안 사고를 식별하고 기록하며, 관리자에게 <span class="point">경고(Alert)</span>를 전송해 신속한 대응이 가능하도록 한다.
- 방화벽에서 차단되지 않은 트래픽을 식별하여 <span class="point">보안 정책의 문제점</span>을 찾고 정책 준수를 유도한다.
- 공격 전 단계인 <span class="point">호스트 스캔, 포트 스캔 등 정찰 활동</span>을 탐지하여 사전에 대응한다.
- <span class="point">SIEM(Security Information and Event Management)</span>과 연동하여 보안 위협을 분석하고 대응을 자동화한다.

<p class="footnote-text">
※SIEM: 기업 내 다양한 IT 인프라에서 발생하는 로그와 보안 이벤트를 실시간으로 수집, 분석하여 위협을 탐지하고 대응하는 보안 솔루션 </p>

### 클라우드 환경에서의 적용

클라우드 환경에서도 IDS/IPS는 중요한 역할을 한다.  
온프레미스 환경과 달리 클라우드는 가상 네트워크, 보안 그룹, 로그 서비스 등과 연동하여 위협을 탐지하고 대응한다.

- AWS GuardDuty, Azure Security Center와 같은 <span class="point">클라우드 기반 IDS/IPS 솔루션</span>을 활용한다.
- 가상화된 네트워크 환경에서도 실시간 트래픽을 감시하고 위협을 탐지·차단한다.
- 클라우드 로그와 이벤트 정보를 수집하여 이상 행위를 분석하고 관리자에게 경고를 제공한다.
- 클라우드 환경의 접근 제어, 네트워크 정책, 보안 그룹 설정과 함께 사용하여 보안성을 높인다.

<p class="footnote-text">
※ AWS GuardDuty : CloudTrail, VPC Flow Logs, DNS 로그 등을 분석하여 AWS 환경의 악성 활동과 비정상 행위를 탐지하는 위협 탐지 서비스이다.</p>
<p class="footnote-text">
※ Microsoft Defender for Cloud(구 Azure Security Center)**는 Azure뿐만 아니라 AWS, GCP, 온프레미스 환경까지 보호 범위를 확장하여 보안 상태 관리와 위협 탐지를 제공한다. </p>

### 보안 강화 전략

IDS/IPS는 단독으로 사용하는 것보다 다른 보안 솔루션과 함께 사용할 때 더 효과적이다.

- 최신 위협 정보를 반영하여 IDS/IPS의 <span class="point">시그니처를 지속적으로 업데이트</span>한다.
- AI 및 머신러닝 기반 탐지 기술을 도입하여 알려지지 않은 공격이나 이상 행위를 탐지한다.
- 방화벽, VPN, SIEM 등 다른 보안 솔루션과 결합하여 <span class="point">다층 보안 체계</span>를 구축한다.
- 탐지된 위협 정보를 바탕으로 보안 정책을 개선하고 사고 대응 절차를 강화한다.
- 로그와 경고를 주기적으로 분석하여 반복적으로 발생하는 공격 패턴을 파악한다.

---

## IDS/IPS의 장단점

### 장점

IDS/IPS를 활용하면 보안 사고를 빠르게 식별하고, 필요에 따라 자동으로 차단할 수 있다.

- 보안 사고를 빠르게 식별하고 관리자에게 경고할 수 있다.
- IPS를 활용하면 악성 트래픽 차단, 세션 종료, 패킷 드롭 등 자동 대응이 가능하다.
- 공격 시도와 보안 이벤트를 로그로 남겨 사고 분석과 포렌식에 활용할 수 있다.
- 방화벽에서 차단되지 않은 트래픽을 확인하여 보안 정책의 문제점을 찾을 수 있다.
- 보안 정책 위반 행위를 탐지하여 조직의 정책 준수를 유도할 수 있다.
- 방화벽, VPN, SIEM 등 다른 보안 솔루션과 연동하여 다층 방어 체계를 구성할 수 있다.

### 단점

IDS/IPS는 강력한 보안 장비이지만, 모든 공격을 완벽하게 탐지하거나 차단할 수 있는 것은 아니다.

- 정상 트래픽을 공격으로 잘못 판단하는 <span class="point">오탐(False Positive)</span>이 발생할 수 있다.
- 실제 공격을 탐지하지 못하는 <span class="point">미탐(False Negative)</span>이 발생할 수 있다.
- 상태 분석이나 호스트 기반 에이전트는 시스템 성능에 영향을 줄 수 있다.
- 암호화된 트래픽 내부의 위협은 탐지하기 어렵다.
- 알려지지 않은 제로데이 공격은 시그니처 기반 탐지만으로 대응하기 어렵다.
- IPS의 경우 오탐이 발생하면 정상적인 서비스 트래픽까지 차단될 수 있다.

<div class="note-box">
<strong>주의할 점</strong><br>
IPS는 자동 차단 기능이 있기 때문에 오탐이 발생하면 정상 트래픽까지 차단할 수 있다. 따라서 운영 환경에서는 탐지 정책을 신중하게 설정하고, 로그를 주기적으로 검토해야 한다.
</div>

---

## 정리

IDS와 IPS는 침입 탐지와 침입 방지를 담당하는 대표적인 보안 시스템이다.

<span class="point">IDS</span>는 주로 네트워크나 시스템에서 발생하는 이상 행위를 탐지하고 관리자에게 경고하는 역할을 한다.  
반면 <span class="point">IPS</span>는 IDS의 탐지 기능에 더해 악성 트래픽을 실시간으로 차단하는 역할까지 수행한다.

실제 보안 환경에서는 IDS와 IPS 기능이 함께 제공되는 경우가 많기 때문에, 두 시스템을 통합하여 <span class="point">IDPS</span>라고 부르기도 한다.

IDS/IPS는 시그니처 기반 탐지, 이상 기반 탐지, 상태 보존 프로토콜 분석 등의 방법을 사용하여 보안 위협을 식별한다. 또한 기업 환경과 클라우드 환경에서 보안 사고 대응, 정책 관리, 정찰 활동 탐지, SIEM 연동 등에 활용된다.

하지만 IDS/IPS만으로 모든 공격을 막을 수는 없다.  
오탐과 미탐 가능성이 존재하고, 암호화 트래픽이나 제로데이 공격 탐지에는 한계가 있기 때문이다.

따라서 IDS/IPS는 방화벽, VPN, SIEM, EDR 등 다른 보안 솔루션과 함께 사용하여 다층 보안 체계를 구성하는 것이 중요하다.

<div class="note-box">
<strong>최종 요약</strong><br>
IDS는 탐지와 경고, IPS는 탐지와 차단을 담당한다. 두 시스템은 단독으로 사용하기보다 SIEM, 방화벽, VPN, EDR 등과 함께 연동하여 다층 보안 체계를 구성할 때 더 효과적이다.
</div>

## 참고 자료

- [Palo Alto Networks, 「IPS 대 IDS 대 방화벽: 차이점은 무엇인가요?」](https://www.paloaltonetworks.co.kr/cyberpedia/firewall-vs-ids-vs-ips)
- [Aria Park, 「침입 탐지 및 방지 시스템(IDS/IPS)의 원리와 활용 방법」, *아리아 날다*, 2025.03.06.](https://creeraria.tistory.com/64)
- NIST SP 800-94, *Guide to Intrusion Detection and Prevention Systems*
