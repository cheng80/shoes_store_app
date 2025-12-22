//  Retail Model
/*
  Create: 13/12/2025 13:32, Creator: Chansol, Park
  Update log: 
    DUMMY 9/29/2025 09:53, 'Point X, Description', Creator: Chansol, Park
  Version: 1.0
  Dependency: SQFlite, Path, collection
  Desc: Retail Model MUST have Product Code

  DateTime MUST converted using value.toIso8601String()
  Stored DateTime in String MUST converted using DateTime.parse(value);
*/

class Retail {
  // Properties
  int? id;
  int? pid; //  Product id
  int? eid; //  Employee id
  final int rQuantity; //  Retail Quantity

  // Constructor
  Retail({this.id, required this.pid, required this.eid, required this.rQuantity});

  Retail.fromMap(Map<String, Object?> map)
    : pid = map['pid'] as int,
      eid = map['eid'] as int,
      rQuantity = map['rQuantity'] as int;

  Map<String, Object?> toMap({bool includeId = false}) {
    final map = <String, Object?>{
      'pid': pid,
      'eid': eid,
      'rQuantity': rQuantity,
    };

    if (includeId) {
      map['id'] = id;
    }

    return map;
  }

  static const List<String> keys = ['id', 'pid', 'eid', 'rQuantity'];
}
