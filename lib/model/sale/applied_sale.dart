//  AppliedSale Model
/*
  Create: 10/12/2025 12:48, Creator: Chansol, Park
  Update log: 
    DUMMY 9/29/2025 09:53, 'Point X, Description', Creator: Chansol, Park
  Version: 1.0
  Dependency: SQFlite, Path, collection
  Desc: AppliedSale Model

  DateTime MUST converted using value.toIso8601String()
  Stored DateTime in String MUST converted using DateTime.parse(value);
*/

class AppliedSale {
  //  Properties
  int? id;
  int? sid;
  double totalDiscount;
  String calctype;

  // Constructor
  AppliedSale({
    this.id,
    this.sid,
    required this.totalDiscount,
    required this.calctype
  });

  AppliedSale.fromMap(Map<String, Object?> map)
    : id = map['id'] as int?,
      sid = map['sid'] as int?,
      totalDiscount = (map['totalDiscount'] as num).toDouble(),
      calctype = map['calctype'] as String;

  static const List<String> keys = ['id', 'sid', 'totalDiscount', 'calctype'];
}