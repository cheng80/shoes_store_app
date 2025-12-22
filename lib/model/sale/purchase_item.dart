//  PurchaseItem Model
/*
  Create: 10/12/2025 12:42, Creator: Chansol, Park
  Update log: 
    DUMMY 9/29/2025 09:53, 'Point X, Description', Creator: Chansol, Park
    12/12/2025 14:27, 'Point 1, Removed quantity', Creator: Chansol, Park
    12/12/2025 14:27, 'Point 2, Purchase item Quantity, rebuild attributes, toMap', Creator: Chansol, Park
    12/12/2025 15:26, 'Point 3, Purchase item Status', Creator: Chansol, Park
    12/12/2025 16:40, 'Point 4, Purchase item uid', Creator: Chansol, Park
    12/12/2025 20:17, 'Point 5, uid -> pcid', Creator: Chansol, Park
  Version: 1.0
  Dependency: SQFlite, Path, collection
  Desc: PurchaseItem Model

  DateTime MUST converted using value.toIso8601String()
  Stored DateTime in String MUST converted using DateTime.parse(value);
*/

class PurchaseItem {
  //  Properties
  //  Point 1
  int? id;
  int pid; //  Product id
  //  Point 4 Point 5
  int pcid; //  Purchase id
  //  Point 2
  int pcQuantity; //  Purchase Item Quantity
  String pcStatus;  //  config.pickupStatus의 value(한글 문자열)만 사용: '제품 준비 중', '제품 준비 완료', '제품 수령 완료', '반품 신청', '반품 처리 중', '반품 완료'



  // Constructor
  PurchaseItem({
    this.id,
    required this.pid,
    required this.pcid,
    required this.pcQuantity,
    required this.pcStatus  //  
  });

  PurchaseItem.fromMap(Map<String, Object?> map)
    : id = map['id'] as int?,
      pid = map['pid'] as int,
      pcid = map['pcid'] as int,
      pcQuantity = map['pcQuantity'] as int,
      pcStatus = map['pcStatus'] as String;

  //  Point 2
  Map<String, Object?> toMap({bool includeId = false}) {
    final map = <String, Object?>{
      'pid': pid,
      'pcid': pcid,
      'pcQuantity': pcQuantity,
      'pcStatus': pcStatus
    };

    if (includeId) {
      map['id'] = id;
    }

    return map;
  }

  static const List<String> keys = ['id', 'pid', 'pcid', 'pcQuantity', 'pcStatus'];
}