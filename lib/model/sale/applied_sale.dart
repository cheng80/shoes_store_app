//  AppliedSale Model


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