/// 전역 저장소 클래스
/// 
/// 메모리 기반 휘발성 저장소입니다.
/// 앱을 종료하면 데이터가 사라지며, Map, List뿐만 아니라 String, int, bool, double 등 모든 타입을 키-값 형태로 저장하고 관리합니다.
/// 앱 사용 중에만 데이터가 유지되는 임시 저장소로 사용합니다.
/// 
/// 사용 예시:
/// ```dart
/// // Map/List 저장
/// GlobalStorage.instance.save('userData', {'name': '홍길동', 'age': 25});
/// GlobalStorage.instance.save('items', [1, 2, 3, 4, 5]);
/// 
/// // 단일 변수 저장
/// GlobalStorage.instance.save('userName', '홍길동');
/// GlobalStorage.instance.save('userAge', 25);
/// GlobalStorage.instance.save('isActive', true);
/// GlobalStorage.instance.save('userScore', 95.5);
/// 
/// // 가져오기 (제네릭)
/// final userData = GlobalStorage.instance.get<Map>('userData');
/// final items = GlobalStorage.instance.get<List>('items');
/// 
/// // 타입별 안전하게 가져오기
/// final name = GlobalStorage.instance.getString('userName');
/// final age = GlobalStorage.instance.getInt('userAge');
/// final isActive = GlobalStorage.instance.getBool('isActive');
/// final score = GlobalStorage.instance.getDouble('userScore');
/// 
/// // 타입 확인
/// final type = GlobalStorage.instance.getType('userName'); // 'String'
/// 
/// // 키 중복 검사
/// if (GlobalStorage.instance.isKeyAvailable('newKey')) {
///   GlobalStorage.instance.save('newKey', value);
/// }
/// ```
class GlobalStorage {
  /// 싱글톤 인스턴스
  static final GlobalStorage instance = GlobalStorage._();
  
  GlobalStorage._();

  /// 내부 저장소 (키-값 쌍) - 메모리 기반 휘발성 저장소
  final Map<String, dynamic> _storage = {};

  /// 값을 저장합니다.
  /// 
  /// [key] 저장할 키 (String 타입, 중복 불가)
  /// [value] 저장할 값 (Map, List, String, int, bool, double 등 모든 타입 가능)
  /// 
  /// 키가 이미 존재하는 경우 기존 값을 덮어씁니다.
  /// 메모리 기반 저장소이므로 앱을 종료하면 데이터가 사라집니다.
  /// 
  /// 사용 예시:
  /// ```dart
  /// // Map/List 저장
  /// GlobalStorage.instance.save('userData', {'name': '홍길동'});
  /// GlobalStorage.instance.save('items', [1, 2, 3]);
  /// 
  /// // 단일 변수 저장
  /// GlobalStorage.instance.save('userName', '홍길동');
  /// GlobalStorage.instance.save('userAge', 25);
  /// GlobalStorage.instance.save('isActive', true);
  /// ```
  void save(String key, dynamic value) {
    _storage[key] = value;
  }

  /// 키에 해당하는 값을 가져옵니다.
  /// 
  /// [key] 가져올 키
  /// 
  /// 반환값: 저장된 값 (타입은 제네릭으로 지정)
  /// 키가 존재하지 않으면 null을 반환합니다.
  /// 
  /// 사용 예시:
  /// ```dart
  /// final userData = GlobalStorage.instance.get<Map>('userData');
  /// final items = GlobalStorage.instance.get<List<int>>('items');
  /// ```
  T? get<T>(String key) {
    final value = _storage[key];
    if (value == null) return null;
    
    // 타입 안전성을 위한 검사
    try {
      return value as T;
    } catch (e) {
      return null;
    }
  }

  /// 키가 존재하는지 확인합니다.
  /// 
  /// [key] 확인할 키
  /// 
  /// 반환값: 키가 존재하면 true, 없으면 false
  /// 
  /// 사용 예시:
  /// ```dart
  /// if (GlobalStorage.instance.containsKey('userData')) {
  ///   final data = GlobalStorage.instance.get<Map>('userData');
  /// }
  /// ```
  bool containsKey(String key) {
    return _storage.containsKey(key);
  }

  /// 키가 사용 가능한지 확인합니다 (중복 검사).
  /// 
  /// [key] 확인할 키
  /// 
  /// 반환값: 키가 사용 가능하면 true (중복 없음), 이미 존재하면 false (중복)
  /// 
  /// 사용 예시:
  /// ```dart
  /// if (GlobalStorage.instance.isKeyAvailable('newKey')) {
  ///   GlobalStorage.instance.save('newKey', value);
  /// } else {
  ///   print('키가 이미 존재합니다');
  /// }
  /// ```
  bool isKeyAvailable(String key) {
    return !_storage.containsKey(key);
  }

  /// 저장된 키-값 쌍을 삭제합니다.
  /// 
  /// [key] 삭제할 키
  /// 
  /// 반환값: 삭제된 값 (키가 없으면 null)
  /// 
  /// 사용 예시:
  /// ```dart
  /// final removed = GlobalStorage.instance.remove('userData');
  /// ```
  dynamic remove(String key) {
    return _storage.remove(key);
  }

  /// 모든 저장된 데이터를 삭제합니다.
  /// 
  /// 사용 예시:
  /// ```dart
  /// GlobalStorage.instance.clear();
  /// ```
  void clear() {
    _storage.clear();
  }

  /// 저장된 모든 키를 반환합니다.
  /// 
  /// 반환값: 모든 키의 리스트
  /// 
  /// 사용 예시:
  /// ```dart
  /// final keys = GlobalStorage.instance.getAllKeys();
  /// print('저장된 키: $keys');
  /// ```
  List<String> getAllKeys() {
    return _storage.keys.toList();
  }

  /// 저장된 데이터의 개수를 반환합니다.
  /// 
  /// 반환값: 저장된 키-값 쌍의 개수
  /// 
  /// 사용 예시:
  /// ```dart
  /// final count = GlobalStorage.instance.length;
  /// print('저장된 항목 수: $count');
  /// ```
  int get length => _storage.length;

  /// 저장소가 비어있는지 확인합니다.
  /// 
  /// 반환값: 비어있으면 true, 데이터가 있으면 false
  /// 
  /// 사용 예시:
  /// ```dart
  /// if (GlobalStorage.instance.isEmpty) {
  ///   print('저장소가 비어있습니다');
  /// }
  /// ```
  bool get isEmpty => _storage.isEmpty;

  /// 저장소가 비어있지 않은지 확인합니다.
  /// 
  /// 반환값: 데이터가 있으면 true, 비어있으면 false
  /// 
  /// 사용 예시:
  /// ```dart
  /// if (GlobalStorage.instance.isNotEmpty) {
  ///   print('저장소에 데이터가 있습니다');
  /// }
  /// ```
  bool get isNotEmpty => _storage.isNotEmpty;

  /// 저장된 값의 타입을 반환합니다.
  /// 
  /// [key] 확인할 키
  /// 
  /// 반환값: 저장된 값의 타입 이름 (String, int, bool, double, Map, List 등)
  /// 키가 존재하지 않으면 null을 반환합니다.
  /// 
  /// 사용 예시:
  /// ```dart
  /// final type = GlobalStorage.instance.getType('userData');
  /// print('타입: $type'); // 'Map' 또는 'String' 등
  /// ```
  String? getType(String key) {
    final value = _storage[key];
    if (value == null) return null;
    return value.runtimeType.toString();
  }

  /// String 타입으로 값을 가져옵니다.
  /// 
  /// [key] 가져올 키
  /// 
  /// 반환값: String 값 또는 null
  /// 
  /// 사용 예시:
  /// ```dart
  /// final name = GlobalStorage.instance.getString('name');
  /// ```
  String? getString(String key) {
    final value = _storage[key];
    if (value == null) return null;
    if (value is String) return value;
    return value.toString();
  }

  /// int 타입으로 값을 가져옵니다.
  /// 
  /// [key] 가져올 키
  /// 
  /// 반환값: int 값 또는 null
  /// 
  /// 사용 예시:
  /// ```dart
  /// final age = GlobalStorage.instance.getInt('age');
  /// ```
  int? getInt(String key) {
    final value = _storage[key];
    if (value == null) return null;
    if (value is int) return value;
    if (value is double) return value.toInt();
    if (value is String) return int.tryParse(value);
    return null;
  }

  /// double 타입으로 값을 가져옵니다.
  /// 
  /// [key] 가져올 키
  /// 
  /// 반환값: double 값 또는 null
  /// 
  /// 사용 예시:
  /// ```dart
  /// final price = GlobalStorage.instance.getDouble('price');
  /// ```
  double? getDouble(String key) {
    final value = _storage[key];
    if (value == null) return null;
    if (value is double) return value;
    if (value is int) return value.toDouble();
    if (value is String) return double.tryParse(value);
    return null;
  }

  /// bool 타입으로 값을 가져옵니다.
  /// 
  /// [key] 가져올 키
  /// 
  /// 반환값: bool 값 또는 null
  /// 
  /// 사용 예시:
  /// ```dart
  /// final isActive = GlobalStorage.instance.getBool('isActive');
  /// ```
  bool? getBool(String key) {
    final value = _storage[key];
    if (value == null) return null;
    if (value is bool) return value;
    if (value is String) {
      final lower = value.toLowerCase();
      if (lower == 'true') return true;
      if (lower == 'false') return false;
    }
    return null;
  }

  /// 저장된 값이 특정 타입인지 확인합니다.
  /// 
  /// [key] 확인할 키
  /// [type] 확인할 타입 (String, int, bool, double, Map, List 등)
  /// 
  /// 반환값: 타입이 일치하면 true, 아니면 false
  /// 
  /// 사용 예시:
  /// ```dart
  /// if (GlobalStorage.instance.isType('userData', 'Map')) {
  ///   final data = GlobalStorage.instance.get<Map>('userData');
  /// }
  /// ```
  bool isType(String key, String type) {
    final valueType = getType(key);
    return valueType == type;
  }

  /// 저장된 값이 기본 타입(String, int, bool, double)인지 확인합니다.
  /// 
  /// [key] 확인할 키
  /// 
  /// 반환값: 기본 타입이면 true, 아니면 false
  /// 
  /// 사용 예시:
  /// ```dart
  /// if (GlobalStorage.instance.isPrimitiveType('name')) {
  ///   final name = GlobalStorage.instance.getString('name');
  /// }
  /// ```
  bool isPrimitiveType(String key) {
    final type = getType(key);
    if (type == null) return false;
    return ['String', 'int', 'bool', 'double'].contains(type);
  }
}

