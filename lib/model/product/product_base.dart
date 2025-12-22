//  ProductBase Model
/*
  Create: 10/12/2025 14:05, Creator: Chansol, Park
  Update log: 
    11/12/2025 10:53, 'Point 1, Redesign entire Model', Creator: Chansol, Park
    11/12/2025 13:53, 'Point 2, Remove piid', Creator: Chansol, Park
  Version: 1.0
  Dependency: SQFlite, Path, collection
  Desc: ProductBase Model

  DateTime MUST converted using value.toIso8601String()
  Stored DateTime in String MUST converted using DateTime.parse(value);
*/

class ProductBase {
  // Properties
  int? id;
  final String pName;
  final String pDescription;
  final String pColor;
  final String pGender;
  final String pStatus; //  active, coming soon, inactive etc
  final String pCategory; //  sneakers, sandals, boots
  final String pModelNumber;

  // Constructor
  ProductBase({
    this.id,
    required this.pName,
    required this.pDescription,
    required this.pColor,
    required this.pGender,
    required this.pStatus,
    required this.pCategory,
    required this.pModelNumber,
  });

  ProductBase.fromMap(Map<String, Object?> map)
    : id = map['id'] as int?,
      pName = map['pName'] as String,
      pDescription = map['pDescription'] as String,
      pColor = map['pColor'] as String,
      pGender = map['pGender'] as String,
      pStatus = map['pStatus'] as String,
      pCategory = map['pCategory'] as String,
      pModelNumber = map['pModelNumber'] as String;

  Map<String, Object?> toMap({bool includeId = false}) {
    final map = <String, Object?>{
      'pName': pName,
      'pDescription': pDescription,
      'pColor': pColor,
      'pGender': pGender,
      'pStatus': pStatus,
      'pCategory': pCategory,
      'pModelNumber': pModelNumber,
    };

    if (includeId) {
      map['id'] = id;
    }

    return map;
  }

  static const List<String> keys = [
    'id',
    'pName',
    'pDescription',
    'pColor',
    'pGender',
    'pStatus',
    'pCategory',
    'pModelNumber',
  ];
}
