//  Purchase Model
/*
  Create: 10/12/2025 12:35, Creator: Chansol, Park
  Update log: 
    DUMMY 9/29/2025 09:53, 'Point X, Description', Creator: Chansol, Park
    12/12/2025 20:22, 'Point 1, cid added', Creator: Chansol, Park
  Version: 1.0
  Dependency: SQFlite, Path, collection
  Desc: Purchase Model

  DateTime MUST converted using value.toIso8601String()
  Stored DateTime in String MUST converted using DateTime.parse(value);
*/

class Purchase {
  //  Properties
  int? id;
  //  Point 1
  int? cid; //  Customer id
  final String pickupDate;  //  Pickupdate default is Purchasedate +1 dummy for now
  final String orderCode; //  Client's request
  final String timeStamp; //  Purchased time

  // Constructor
  Purchase({
    this.id,
    required this.cid,
    required this.pickupDate,
    required this.orderCode,
    required this.timeStamp
  });

  Purchase.fromMap(Map<String, Object?> map)
    : id = map['id'] as int?,
      cid = map['cid'] as int?,
      pickupDate = map['pickupDate'] as String,
      orderCode = map['orderCode'] as String,
      timeStamp = map['timeStamp'] as String;

      Map<String, Object?> toMap({bool includeId = false}) {
    final map = <String, Object?>{
      'cid': cid,
      'pickupDate': pickupDate,
      'orderCode': orderCode,
      'timeStamp': timeStamp
    };

    if (includeId) {
      map['id'] = id;
    }

    return map;
  }
  static const List<String> keys = ['id', 'cid', 'pickupDate', 'orderCode', 'timeStamp'];
}
