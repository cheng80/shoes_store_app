import 'package:shoes_store_app/core/global_storage.dart';
import 'package:shoes_store_app/model/employee.dart';

/// 관리자 정보 저장소 클래스
/// GlobalStorage를 사용하여 관리자(Employee) 정보를 저장하고 불러오는 기능을 제공합니다.
/// 로그인 성공 시 관리자 정보를 저장하고, 관리자 페이지에서 사용합니다.
/// 메모리 기반 휘발성 저장소이므로 앱을 종료하면 데이터가 사라집니다.

class AdminStorage {
  /// GlobalStorage 인스턴스
  static GlobalStorage get _storage => GlobalStorage.instance;

  /// 저장 키 상수들
  static const String _keyEmployeeId = 'admin_employee_id';
  static const String _keyEmployeeEmail = 'admin_employee_email';
  static const String _keyEmployeePhone = 'admin_employee_phone';
  static const String _keyEmployeeName = 'admin_employee_name';

  /// 관리자 정보 저장
  /// 로그인 성공 시 Employee 정보를 저장합니다.
  /// [employee] 저장할 직원 정보
  static void saveAdmin(Employee employee) {
    if (employee.id != null) {
      _storage.save(_keyEmployeeId, employee.id);
    }
    _storage.save(_keyEmployeeEmail, employee.eEmail);
    _storage.save(_keyEmployeePhone, employee.ePhoneNumber);
    _storage.save(_keyEmployeeName, employee.eName);
    _storage.save('admin_role', employee.eRole);
    // 비밀번호는 보안상 저장하지 않음
  }

  /// 저장된 관리자 정보 가져오기
  /// 저장된 관리자 정보를 Employee 객체로 반환합니다.
  /// 반환값: 저장된 Employee 객체, 없으면 null
  static Employee? getAdmin() {
    final email = _storage.get<String>(_keyEmployeeEmail);
    final phone = _storage.get<String>(_keyEmployeePhone);
    final name = _storage.get<String>(_keyEmployeeName);
    final id = _storage.get<int>(_keyEmployeeId);

    if (email == null || phone == null || name == null) {
      return null;
    }

    return Employee(
      id: id,
      eEmail: email,
      ePhoneNumber: phone,
      eName: name,
      ePassword: '', // 비밀번호는 저장하지 않음
      eRole: getAdminRole(),
    );
  }

  /// 관리자 이름 가져오기
  /// 저장된 관리자 이름을 반환합니다.
  /// 반환값: 관리자 이름, 없으면 null
  static String? getAdminName() {
    return _storage.get<String>(_keyEmployeeName);
  }

  /// 관리자 이메일 가져오기
  /// 저장된 관리자 이메일을 반환합니다.
  /// 반환값: 관리자 이메일, 없으면 null
  static String? getAdminEmail() {
    return _storage.get<String>(_keyEmployeeEmail);
  }

  /// 관리자 역할 가져오기
  /// 저장된 관리자 역할을 반환합니다. (기본값: '관리자')
  /// 반환값: 관리자 역할
  static String getAdminRole() {
    return _storage.get<String>('admin_role') ?? '관리자';
  }

  /// 관리자 역할 저장
  /// 관리자 역할을 저장합니다.
  /// [role] 저장할 역할 (예: '관리자', '대리점장' 등)
  static void saveAdminRole(String role) {
    _storage.save('admin_role', role);
  }

  /// 관리자 정보 삭제
  /// 로그아웃 시 저장된 관리자 정보를 삭제합니다.
  static void clearAdmin() {
    _storage.remove(_keyEmployeeId);
    _storage.remove(_keyEmployeeEmail);
    _storage.remove(_keyEmployeePhone);
    _storage.remove(_keyEmployeeName);
    _storage.remove('admin_role');
  }

  /// 관리자 로그인 여부 확인
  /// 저장된 관리자 정보가 있는지 확인합니다.
  /// 반환값: 관리자 정보가 있으면 true, 없으면 false
  static bool isAdminLoggedIn() {
    return _storage.containsKey(_keyEmployeeEmail);
  }
}

