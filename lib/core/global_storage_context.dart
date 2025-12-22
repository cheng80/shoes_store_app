import 'package:flutter/material.dart';
import 'global_storage.dart';

/// BuildContext 확장 – context.globalStorage로 전역 저장소 접근
/// 
/// 사용 예시:
/// ```dart
/// // 저장
/// context.globalStorage.save('userData', {'name': '홍길동'});
/// 
/// // 가져오기
/// final userData = context.globalStorage.get<Map>('userData');
/// 
/// // 키 중복 검사
/// if (context.globalStorage.isKeyAvailable('newKey')) {
///   context.globalStorage.save('newKey', value);
/// }
/// ```
extension GlobalStorageContext on BuildContext {
  /// 전역 저장소 인스턴스 반환
  GlobalStorage get globalStorage => GlobalStorage.instance;
}

