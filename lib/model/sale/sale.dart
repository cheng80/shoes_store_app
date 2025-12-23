//  Sale Model


class Sale {
  // Properties
  int? id;
  final int maxSaleQuantity;
  final int minSaleQuantity;
  final int maxSalePrice;
  final int saleTriggerPrice;
  final double saleRate;
  final double unitSale;
  final String saleStartDate;
  final String saleEndDate;

  // Constructor
  Sale({
    this.id,
    required this.maxSaleQuantity,
    required this.minSaleQuantity,
    required this.maxSalePrice,
    required this.saleTriggerPrice,
    required this.saleRate,
    required this.unitSale,
    required this.saleStartDate,
    required this.saleEndDate,
  });

  Sale.fromMap(Map<String, Object?> map)
    : id = map['id'] as int?,
      maxSaleQuantity = map['maxSaleQuantity'] as int,
      minSaleQuantity = map['minSaleQuantity'] as int,
      maxSalePrice = map['maxSalePrice'] as int,
      saleTriggerPrice = map['saleTriggerPrice'] as int,
      saleRate = (map['saleRate'] as num).toDouble(),
      unitSale = (map['unitSale'] as num).toDouble(),
      saleStartDate = map['saleStartDate'] as String,
      saleEndDate = map['saleEndDate'] as String;

  static const List<String> keys = [
    'id',
    'maxSaleQuantity',
    'minSaleQuantity',
    'maxSalePrice',
    'saleTriggerPrice',
    'saleRate',
    'unitSale',
    'saleStartDate',
    'saleEndDate'
  ];
}
