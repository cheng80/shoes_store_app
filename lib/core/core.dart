/// Core 모듈 - 전역 저장소 및 공통 기능
/// 
/// 이 파일을 import하면 전역 저장소와 관련 Extension을 사용할 수 있습니다.
/// 
/// 사용 예시:
/// ```dart
/// import 'package:custom_test_app/core/core.dart';
/// 
/// // Extension을 통해 사용
/// context.globalStorage.save('key', value);
/// final value = context.globalStorage.get<Map>('key');
/// 
/// // 또는 직접 인스턴스 접근
/// GlobalStorage.instance.save('key', value);
/// ```
library;

// 전역 저장소 클래스
export 'global_storage.dart';

// BuildContext Extension
export 'global_storage_context.dart';

