//  Manufacturer Model
/*
  Create: 11/12/2025 12:42, Creator: Chansol, Park
  Update log: 
    DUMMY 00/00/0000 00:00, 'Point X, Description', Creator: Chansol, Park
  Version: 1.0
  Dependency: SQFlite, Path, collection
  Desc: Manufacturer Model

  DateTime MUST converted using value.toIso8601String()
  Stored DateTime in String MUST converted using DateTime.parse(value);
*/

class Manufacturer {
  // Properties
  int? id;
  final String mName;

  // Constructor
  Manufacturer({this.id, required this.mName});

  Manufacturer.fromMap(Map<String, Object?> map)
    : id = map['id'] as int?,
      mName = map['mName'] as String;

  Map<String, Object?> toMap({bool includeId = false}) {
    final map = <String, Object?>{'mName': mName};

    if (includeId) {
      map['id'] = id;
    }

    return map;
  }

  static const List<String> keys = ['id', 'mName'];
}
