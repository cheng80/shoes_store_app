# 📖 개발 참고 자료

## 📁 코드 생성 위치 규칙

### 신규 코드 생성 위치

- **신규 생성하는 코드는 항상 `lib/view/cheng` 폴더 안에서 생성합니다.**
- 주로 `.dart` 파일을 생성합니다.
- 이 폴더가 프로젝트의 주요 코드 생성 위치입니다.

### ⚠️ 리팩토링 유예 사항

**리팩토링 기간 동안 유예** (2025-12-13 ~ 리팩토링 완료 시까지):
- 현재 `cheng` 폴더 리팩토링 진행 중입니다.
- 리팩토링 목적: 데이터베이스 핸들러 중심 재편, 주석 정리, RDAO 제거
- 리팩토링 기간 동안에는 `lib/database/` 폴더에 핸들러 클래스 생성이 필요할 수 있습니다.
- 리팩토링 완료 후에는 다시 `lib/view/cheng` 폴더 규칙이 적용됩니다.
- **참고**: 리팩토링 관련 문서는 `PROGRESS.md`의 "최근 완료된 작업" 섹션을 참조하세요.

## 🎨 커스텀 위젯 라이브러리

### `lib/view/cheng/custom` 폴더

- 기본 위젯들을 커스텀하게 래핑한 위젯 라이브러리입니다.
- 위젯 생성 시 **항상 기본 위젯보다 우선적으로 사용**합니다.

### 사용 규칙

- Flutter 기본 위젯 대신 `custom` 폴더의 커스텀 위젯을 우선적으로 사용합니다.
- 예: `Text` 대신 `CustomText`, `Button` 대신 `CustomButton` 사용
- 일관된 디자인과 기능을 위해 커스텀 위젯을 활용합니다.

## 🎨 디자인 위젯 코딩 규칙

### 상태 관리 변수 선언 규칙

- **상태 관리에 쓰이는 변수들은 `late final`로 선언하고 `initState`에서 초기화합니다.**
- DB 관련 객체, DAO 객체 등 상태 관리에 사용되는 변수는 즉시 초기화하지 않고 `initState`에서 초기화합니다.
- 이는 위젯 생명주기를 명확히 하고 초기화 순서를 제어하기 위함입니다.

### 함수 분리 규칙

- **디자인이 들어가는 위젯 부분에 인라인 함수는 자제합니다.**
- 단순 상태 전환 정도가 아닌 경우 모두 개별 함수로 분리합니다.
- **모든 개별 함수는 `build` 메서드 아래에 배치합니다.**
- 함수들은 `//----Function Start----`와 `//----Function End----` 주석 사이에 배치합니다.

### 상태 관리 변수 선언 예시

```dart
class _MyWidgetState extends State<MyWidget> {
  // 상태 관리 변수는 late final로 선언
  late final DbSetting dbSetting;
  late final RDAO<Employee> employeeDAO;
  
  // 일반 변수는 그대로 선언
  bool _isChecked = false;
  final TextEditingController _controller = TextEditingController();

  @override
  void initState() {
    super.initState();
    
    // 상태 관리 변수 초기화
    dbSetting = DbSetting();
    employeeDAO = RDAO<Employee>(
      dbName: dbName,
      tableName: config.tTableEmployee,
      dVersion: dVersion,
      fromMap: Employee.fromMap,
    );
  }

  @override
  void dispose() {
    // 리소스 정리
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return CustomButton(
      onCallBack: _handleButtonClick,
    );
  }

  //----Function Start----

  // 버튼 클릭 처리 함수
  void _handleButtonClick() {
    // 복잡한 로직 처리
  }

  //----Function End----
}
```

### 함수 분리 예시

```dart
class MyWidget extends StatefulWidget {
  // ...
}

class _MyWidgetState extends State<MyWidget> {
  // 변수 선언
  bool _isChecked = false;

  @override
  void dispose() {
    // 리소스 정리
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return CustomButton(
      onCallBack: _handleButtonClick, // 인라인 함수 대신 개별 함수 사용
    );
  }

  //----Function Start----

  // 버튼 클릭 처리 함수
  void _handleButtonClick() {
    // 복잡한 로직 처리
  }

  // 데이터 검증 함수
  bool _validateInput() {
    // 검증 로직
    return true;
  }

  //----Function End----
}
```

## 🔀 Git 작업 규칙

### 기본 원칙
- **Git은 기본적으로 사용자가 직접 관리합니다.**
- AI는 사용자 요청 시에만 Git 작업을 수행합니다.

### 브랜치 규칙

<!-- 
⚠️ 일단 주석 처리 하고 향후 다시 수정 예정

- **모든 작업은 `cheng` 브랜치에서만 수행합니다.**
- 다른 브랜치에는 절대 수정하지 않습니다.
- **작업 시작 시 항상 `cheng` 브랜치인지 확인합니다.**
-->

### 복원 및 Reset 규칙
- 복원 요청 시 기존 히스토리를 읽어서 수행하되 **절대 reset은 금지**합니다.
- `git reset`은 사용자가 명시적으로 요청할 때만 사용합니다.
- reset 사용 전 반드시 다시 한번 확인을 요청합니다.
- reset 복구가 필요한 상황이 되면 `git reflog`로 기록을 참조하여 복구를 시도합니다.
