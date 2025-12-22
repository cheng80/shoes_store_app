//  Product Model
/*
  Create: 10/12/2025 13:57, Creator: Chansol, Park
  Update log: 
    DUMMY 00/00/0000 00:00, 'Point X, Description', Creator: Chansol, Park
    12/12/2025 14:31, 'Point 1, Description', Creator: Chansol, Park
  Version: 1.0
  Dependency: SQFlite, Path, collection
  Desc: Product Model

  DateTime MUST converted using value.toIso8601String()
  Stored DateTime in String MUST converted using DateTime.parse(value);
*/

class Product {
  // Properties
  int? id;
  int? pbid; //  ProductBase id
  int? mfid; //  Manufacturer id
  final int size;
  final int basePrice;
  final int pQuantity;  //  Quantity of a product for Stock 

  // Constructor
  Product({
    this.id,
    required this.pbid,
    required this.mfid,
    required this.size,
    required this.basePrice,
    required this.pQuantity
  });

  Product.fromMap(Map<String, Object?> map)
    : id = map['id'] as int?,
      pbid = map['pbid'] as int?, //  ProductBase id
      mfid = map['mfid'] as int?,
      size = map['size'] as int,
      basePrice = map['basePrice'] as int,
      pQuantity = map['pQuantity'] as int;

  Map<String, Object?> toMap({bool includeId = false}) {
    final map = <String, Object?>{
      'pbid': pbid,
      'mfid': mfid,
      'size': size,
      'basePrice': basePrice,
      'pQuantity': pQuantity
    };

    if (includeId) {
      map['id'] = id;
    }

    return map;
  }

  static const List<String> keys = [
    'id',
    'pbid',
    'mfid',
    'size',
    'basePrice',
    'pQuantity'
  ];
}
