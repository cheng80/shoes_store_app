//  Customer Model
/*
  Create: 12/11/2025 15:38, Creator: taekkwon, kim
  Update log: 
    12/11/2025 15:38, 'create Employee Model', Creator: taekkwon, kim
    12/11/2025 15:38, 'add Function toMap', Creator: taekkwon, kim
    12/12/2025 14:41, 'Point 1, eRole', Creator: Chansol Park
  Version: 1.0
  Dependency: SQFlite, Path, collection
  Desc: Employee Model
*/

class Employee {
  // Properties
  int? id;
  final String eEmail;
  final String ePhoneNumber;
  final String eName;
  final String ePassword;
  final String eRole;

  // Constructor
  Employee({
    this.id,
    required this.eEmail,
    required this.ePhoneNumber,
    required this.eName,
    required this.ePassword,
    //  Point 1
    required this.eRole
  });

  Employee.fromMap(Map<String, Object?> map)
    : id = map['id'] as int?,
      eEmail = map['eEmail'] as String,
      ePhoneNumber = map['ePhoneNumber'] as String,
      eName = map['eName'] as String,
      ePassword = map['ePassword'] as String,
      eRole = map['eRole'] as String;

  Map<String, Object?> toMap({bool includeId = false}) {
    final map = <String, Object?>{
      'eEmail': eEmail,
      'ePhoneNumber': ePhoneNumber,
      'eName': eName,
      'ePassword': ePassword,
      'eRole': eRole,
    };

    if (includeId) {
      map['id'] = id;
    }

    return map;
  }

  static const List<String> keys = [
    'id',
    'eEmail',
    'ePhoneNumber',
    'eName',
    'ePassword',
    'eRole'
  ];
}
