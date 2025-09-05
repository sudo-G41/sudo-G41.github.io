---
title: "백그라운드 내 스냅샷"
excert: "DVBA를 이용하여 백그라운드 내 스냅샷을 지워 정보를 보호하는 방법"
categories:
  - sec
tags:
  - DVBA
  - Damn Vukner Bank app
  - 금융보안
  - 백그라운드 화면
  - AOS
  - Android
last_modified_at: 2024-11-14T23:59:59+09:00

toc_label: I.N.D.E.X
toc: true
toc_sticky: true

author_profile: true
sitemap :
  changefreq : daily
  priority : 1.0
---

# 백그라운드 화면 보호

## 현 상황

<img src="/assets/images/back_snapshot/1_before_phone_screenshot.png"/>

현재 "III"버튼을 눌러 백그라운드로 들어가면 DVBA화면이 보인다.

여기서 보여주는 화면은 메인 화면이지만 프로필을 들어가도 마찬가지로 마지막에 본 화면이 노출된다.

## 취약점

이 상태가 문제인 이유는 백그라운드에 대해 간단히 설명하면 AOS(Android OS)는 앱의 마지막 장면을 스냅샷을 찍어 이를 백그라운드에서 보여주는 방식으로 백그라운드 화면을 보여준다.

이때 스냅샷은 "/data/system_ce/0/snapshots" 폴더 같이 특정 폴더에 저장되는데 이때 폰에 바이러스 등 악성 프로그램이 설치되어 공격자가 피해자의 스냅샷을 탈취 할 수 있다면 중요정보가 노출된 스냅샷도 탈취가 가능하다는 이야기이다.

그러므로 해당 화면의 스냅샷이 찍히지 않도록 다른 화면으로 대체 될 수 있도록 조치를 취해야 한다.

## 조치
<img src="/assets/images/back_snapshot/2_before_backscreen.png">

``` java
getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN, WindowManager.LayoutParams.FLAG_FULLSCREEN);
```

MainActivity.java를 보면 플래그를 삽입할 수 있는 코드가 있는데 여기서 디폴트로 "FLAG_FULLSCREEN"가 적용되어 있다. 이는 상단의 상태 바(status bar)를 지워준다.

여기서 플래그 중 FLAG_SECURE 관련 설명을 보면

<img src="/assets/images/back_snapshot/3_FLAG_SECURE.png">

보안 특히 스냅샷 같은 스크린 샷 관련 보안을 적용해주는 플래그임을 알 수 있다.
그러므로

``` java
getWindow().setFlags(
    WindowManager.LayoutParams.FLAG_FULLSCREEN | WindowManager.LayoutParams.FLAG_SECURE,
    WindowManager.LayoutParams.FLAG_FULLSCREEN | WindowManager.LayoutParams.FLAG_SECURE
);
```

같이 FLAG_SECURE를 적용해주면

<img src="/assets/images/back_snapshot/4_after_backscreen.png">

<img src="/assets/images/back_snapshot/5_after_phone_screenshot.png">

처럼 스냅샷이 찍히지 않아 빈 화면이 뜨는 것을 볼 수 있다.

## 결론

백그라운드 화면 문제는 스냅샷이 문제이므로 스냅샷을 변경시키거나 삭제 또는 스냅샷을 찍지 못하게 하는 방식으로 보안을 챙길 수 있지만 간편하게 안드로이드에서 재공하는 플러그를 사용하여 처리 할 수 있다.

:wq