import 'package:shoes_store_app/core/global_storage.dart';
import 'package:shoes_store_app/model/customer.dart';

/// 사용자 정보 저장소 클래스
/// GlobalStorage를 사용하여 사용자(Customer) 정보를 저장하고 불러오는 기능을 제공합니다.
/// 로그인 성공 시 사용자 정보를 저장하고, 사용자 페이지에서 사용합니다.
/// 메모리 기반 휘발성 저장소이므로 앱을 종료하면 데이터가 사라집니다.

class UserStorage {
  /// GlobalStorage 인스턴스
  static GlobalStorage get _storage => GlobalStorage.instance;

  /// 저장 키 상수들
  static const String _keyCustomerId = 'user_customer_id';
  static const String _keyCustomerEmail = 'user_customer_email';
  static const String _keyCustomerPhoneNumber = 'user_customer_phone_number';
  static const String _keyCustomerName = 'user_customer_name';

  /// 사용자 정보 저장
  /// 로그인 성공 시 Customer 정보를 저장합니다.
  /// [customer] 저장할 고객 정보
  static void saveUser(Customer customer) {
    if (customer.id != null) {
      _storage.save(_keyCustomerId, customer.id);
    }
    _storage.save(_keyCustomerEmail, customer.cEmail);
    _storage.save(_keyCustomerPhoneNumber, customer.cPhoneNumber);
    _storage.save(_keyCustomerName, customer.cName);
    // 비밀번호는 보안상 저장하지 않음
  }

  /// 저장된 사용자 정보 가져오기
  /// 저장된 사용자 정보를 Customer 객체로 반환합니다.
  /// 반환값: 저장된 Customer 객체, 없으면 null
  static Customer? getUser() {
    final email = _storage.get<String>(_keyCustomerEmail);
    final phoneNumber = _storage.get<String>(_keyCustomerPhoneNumber);
    final name = _storage.get<String>(_keyCustomerName);
    final id = _storage.get<int>(_keyCustomerId);

    if (email == null || phoneNumber == null || name == null) {
      return null;
    }

    return Customer(
      id: id,
      cEmail: email,
      cPhoneNumber: phoneNumber,
      cName: name,
      cPassword: '', // 비밀번호는 저장하지 않음
    );
  }

  /// 사용자 이름 가져오기
  /// 저장된 사용자 이름을 반환합니다.
  /// 반환값: 사용자 이름, 없으면 null
  static String? getUserName() {
    return _storage.get<String>(_keyCustomerName);
  }

  /// 사용자 이메일 가져오기
  /// 저장된 사용자 이메일을 반환합니다.
  /// 반환값: 사용자 이메일, 없으면 null
  static String? getUserEmail() {
    return _storage.get<String>(_keyCustomerEmail);
  }

  /// 사용자 전화번호 가져오기
  /// 저장된 사용자 전화번호를 반환합니다.
  /// 반환값: 사용자 전화번호, 없으면 null
  static String? getUserPhoneNumber() {
    return _storage.get<String>(_keyCustomerPhoneNumber);
  }

  /// 사용자 ID 가져오기
  /// 저장된 사용자 ID를 반환합니다.
  /// 반환값: 사용자 ID, 없으면 null
  static int? getUserId() {
    return _storage.get<int>(_keyCustomerId);
  }

  /// 사용자 정보 삭제
  /// 로그아웃 시 저장된 사용자 정보를 삭제합니다.
  static void clearUser() {
    _storage.remove(_keyCustomerId);
    _storage.remove(_keyCustomerEmail);
    _storage.remove(_keyCustomerPhoneNumber);
    _storage.remove(_keyCustomerName);
  }

  /// 사용자 로그인 여부 확인
  /// 저장된 사용자 정보가 있는지 확인합니다.
  /// 반환값: 사용자 정보가 있으면 true, 없으면 false
  static bool isUserLoggedIn() {
    return _storage.containsKey(_keyCustomerEmail);
  }
}

