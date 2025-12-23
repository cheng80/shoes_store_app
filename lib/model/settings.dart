//  Settings Model

class Settings {
  // Properties
  int? id;
  final String seedColor;
  final double brightness;

  // Constructor
  Settings({this.id, required this.seedColor, required this.brightness});

  Settings.fromMap(Map<String, Object?> map)
    : id = map['id'] as int?,
      seedColor = map['seedColor'].toString(),
      brightness = (map['brightness'] as num).toDouble();
  
  static const List<String> keys = ['id', 'seedColor', 'brightness'];
}