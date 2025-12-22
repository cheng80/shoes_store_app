//  Settings Model
/*
  Create: 10/12/2025 13:50, Creator: Chansol, Park
  Update log: 
    DUMMY 00/00/0000 00:00, 'Point X, Description', Creator: Chansol, Park
  Version: 1.0
  Dependency: SQFlite, Path, collection
  Desc: Settings Model

*/

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