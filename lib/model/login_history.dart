//  LoginHistory Model
/*
  Create: 10/12/2025 12:26, Creator: Chansol, Park
  Update log: 
    DUMMY 9/29/2025 09:53, 'Point X, Description', Creator: Chansol, Park
    12/12/2025 14:46, 'Point 1, lPaymentMethod, lAddress, total refactored attributes', Creator: Chansol, Park
  Version: 1.0
  Dependency: SQFlite, Path, collection
  Desc: LoginHistory Model
*/

class LoginHistory {
  // Properties
  int? id;
  int? cid; //  Customer ID
  final String loginTime;
  final String lStatus;
  final double lVersion;
  //  Point 1
  final String lAddress;
  final String lPaymentMethod;

  // Constructor
  LoginHistory({
    this.id,
    this.cid,
    required this.loginTime,
    required this.lStatus,
    required this.lVersion,
    required this.lAddress,
    required this.lPaymentMethod,
  });

  LoginHistory.fromMap(Map<String, Object?> map)
    : id = map['id'] as int?,
      cid = map['cid'] as int?,
      loginTime = map['loginTime'] as String,
      lStatus = map['lStatus'] as String,
      lVersion = (map['lVersion'] as num).toDouble(),
      lAddress = map['lAddress'] as String,
      lPaymentMethod = map['lPaymentMethod'] as String;

  Map<String, Object?> toMap({bool includeId = false}) {
    final map = <String, Object?>{
      'cid': cid,
      'loginTime': loginTime,
      'lStatus': lStatus,
      'lVersion': lVersion,
      'lAddress': lAddress,
      'lPaymentMethod': lPaymentMethod,
    };

    if (includeId) {
      map['id'] = id;
    }

    return map;
  }

  static const List<String> keys = [
    'id',
    'cid',
    'loginTime',
    'lStatus',
    'lVersion',
    'lAddress',
    'lPaymentMethod',
  ];
}
