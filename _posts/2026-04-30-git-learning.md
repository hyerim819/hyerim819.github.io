---
layout: post
title: "git 배우기"
description: Learn Git Branching을 통해 기초 git 명령어 익히기
date: 2026-04-30
categories: [개발]
tags: [git,명령어,기초]
--- 

# Git 기본 명령어 정리

이번에는 Git 기본 명령어를 공부하면서 정리한 내용을 블로그 형식으로 남겨보려고 한다.
이전까지 아예 안 써봤던 명령어는 `*` 표시를 해두었다.

---

## 기본 명령어

### `commit`

`commit`은 매우 가벼운 단위이다.
커밋은 부모 커밋을 가리킨다.

---

### `branch`

브랜치를 만들 때는 다음과 같이 사용한다.

```bash
git branch [브랜치명]
```

---

### `checkout`

`checkout`은 그곳으로 이동하는 명령어이다.

HEAD는 현재 작업 중인 브랜치를 가리킨다.
단, 해시값을 checkout한 경우에는 브랜치가 아니라 커밋 자체를 가리킨다.

실제 해시값은 복잡하고 길기 때문에 Git에서는 앞부분만 써도 알아듣는다.

---

## 상대 참조

### `^` 명령어

`^`는 부모 커밋을 가리킬 때 사용한다.

예를 들어 다음과 같이 쓰면 `main`의 부모 커밋을 가리킨다.

```bash
git checkout main^
```

`^^`을 쓰면 조부모 커밋을 가리키게 된다.

---

### `~` 명령어

상대 참조는 `~`를 이용해서 한 번에 원하는 만큼 위로 이동할 수 있다.

예를 들어 다음 명령어는 HEAD에서 4칸 위로 이동한다.

```bash
git checkout HEAD~4
```

---

## `*cherry-pick`

`cherry-pick`은 `rebase`랑 비슷한 역할을 한다.

한 번에 여러 개의 커밋을 복사해서 넣을 수 있다.

```bash
git cherry-pick c2 c3 c4
```

이런 느낌으로 사용할 수 있다.

---

## `reset`


---

## `*revert`


---

## `*rebase`

`rebase`는 다른 곳에서 작업한 브랜치를 일렬로 정렬하듯이 합치는 명령어이다.

```bash
rebase -i HEAD~3
```

이런 식으로 사용하면 새로운 창이 하나 생긴다.
거기서 순서를 바꾸거나 선택해서 특정한 커밋만 복사할 수 있다.

---

## `merge`

`git merge`를 하면 커밋을 브랜치에 합칠 수 있다.

예를 들어 `main` 브랜치에 checkout한 상태에서 다음 명령어를 실행한다고 하자.

```bash
git merge c2
```

그러면 `main` 아래에 새로운 커밋이 생기면서 합쳐진다.

---

## `git branch -f 브랜치명`

```bash
git branch -f 브랜치명
```

이 명령어는 브랜치 포인터를 강제로 이동시킨다.

---

# 고난이도 문제

## 1. 무한 번의 rebase 문제

막힌 부분은 계속 `rebase`를 할 때 커밋 자체를 지정해서 브랜치가 함께 따라오지 않았다는 점이다.

---

## 2. 다수의 부모 문제

여러 개의 부모가 있을 때 `~`, `^`을 그냥 사용하면 첫 번째 부모를 가리킨다.

다른 부모를 가리키고 싶다면 다음과 같이 사용하면 된다.

```bash
git checkout HEAD^2
```

또는

```bash
git checkout 브랜치명^2
```

이렇게 쓰면 두 번째 부모를 가리키게 된다.

또한 다음처럼 한 번에 이어서 사용할 수도 있다.

```bash
git checkout HEAD~^2~2
```

---

## 3. 브랜치 스파게티

브랜치 스파게티 문제에서는 `cherry-pick`을 사용했더니 11개의 명령어를 사용하게 되었다.

---

# 원격 저장소 관련 명령어

## `*git clone`

`git clone`은 원격 저장소를 복제하는 명령어이다.

로컬 저장소에 `origin(원격저장소 이름)/브랜치명`이라는 브랜치가 생긴다.

---

## `*git fetch`

`git fetch`의 역할은 원격 저장소에는 있지만 로컬에는 없는 커밋들을 다운로드하는 것이다.

또한 우리의 원격 브랜치가 가리키는 곳을 업데이트한다.

단, 다운로드만 하는 것이지 로컬에서 직접 반영되어 바뀌거나 하지는 않는다.

한 번에 전체를 다 비교해서 로컬에 빠져 있는 브랜치나 커밋들을 복구하는 느낌인 듯하다.

---

## `*git pull`

`git pull`은 `git fetch`를 한 후에 내려받은 브랜치를 병합하는 과정을 단축한 명령어이다.

---

## `*git push`

`git push`는 로컬에서 새로 만든 커밋들을 원격에 공유하는 명령어이다.

---

## 작업 과정이 엇갈린 경우

작업 과정이 엇갈려 내가 `clone`하고 한 작업이 다른 개발자의 `clone` 후 작업에 의해 무용지물이 되었을 때, `push`의 역할이 애매해진다.

이럴 때 사용할 수 있는 흐름은 다음과 같다.

```bash
git pull --rebase
git push
```

---

## 실수로 main 브랜치에 커밋을 했다면?

실수로 `main` 브랜치에 커밋을 했다면 다음과 같은 방식으로 처리할 수 있다.

다른 브랜치를 만들고 원격 저장소에 `push`한 다음, 로컬 저장소의 `main` 브랜치를 `reset`한다.

---

## 원격 브랜치 추적 설정

```bash
git checkout -b 브랜치명 o/main
git pull
```

이 방식과 다음 명령어는 비슷한 의미로 볼 수 있다.

```bash
git branch -u o/main 브랜치명
```

지정한 브랜치가 원격 저장소를 추적하게 설정할 수 있다.
이렇게 하면 브랜치에서 바로 원격으로 `pull` / `push`할 수 있게 된다.

---

## `*git push <remote><place>`

```bash
git push <remote><place>
```

이 명령어는 내 `place`에 있는 것들을 `push`해서 `remote`로 지정되어 있는 곳에 넣으라는 의미이다.

---

## `*git push origin <source>:<destination>`

```bash
git push origin <source>:<destination>
```

`source`에 있는 내용을 `destination`으로 보내는 방식이다.

---

## `*git fetch origin C2:bar`

```bash
git fetch origin C2:bar
```

이 명령어는 `c2`를 `origin`의 place로 지정하고, 커밋을 내려받아서 `bar` 브랜치에 추가하는 방식이다.

---

## `*git push origin :foo`

```bash
git push origin :foo
```

`없음`을 보내면 원격에 있던 기존 `foo` 브랜치가 사라진다!

---

## `*git fetch origin :bar`

```bash
git fetch origin :bar
```

원격에 없는 브랜치를 `fetch`하면 로컬에 새로운 브랜치가 생긴다.

`pull`은 `fetch + merge`이므로 생략한다.

## 모드 클리어 인증사진
<img src="/img/gitlearning1.png" alt="로컬환경" width="500">
<img src="/img/gitlearning2.png" alt="원격환경" width="500">
