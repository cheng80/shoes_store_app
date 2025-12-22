import 'package:flutter/material.dart';
import 'custom_json_util.dart';

// JsonUtil 사용 예제 페이지
class JsonUtilExamplePage extends StatefulWidget {
  const JsonUtilExamplePage({super.key});

  @override
  State<JsonUtilExamplePage> createState() => _JsonUtilExamplePageState();
}

class _JsonUtilExamplePageState extends State<JsonUtilExamplePage> {
  String _result = '';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('JsonUtil 예제')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            ElevatedButton(
              onPressed: _basicExample,
              child: const Text('기본 JSON 변환'),
            ),
            const SizedBox(height: 8),
            ElevatedButton(
              onPressed: _objectExample,
              child: const Text('객체 ↔ JSON 변환'),
            ),
            const SizedBox(height: 8),
            ElevatedButton(
              onPressed: _validationExample,
              child: const Text('JSON 검증'),
            ),
            const SizedBox(height: 8),
            ElevatedButton(
              onPressed: _formattingExample,
              child: const Text('JSON 포맷팅'),
            ),
            const SizedBox(height: 8),
            ElevatedButton(
              onPressed: _mergeExample,
              child: const Text('JSON 병합'),
            ),
            const SizedBox(height: 8),
            ElevatedButton(
              onPressed: _pathExample,
              child: const Text('경로로 값 가져오기/설정'),
            ),
            const SizedBox(height: 16),
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: Colors.grey[200],
                borderRadius: BorderRadius.circular(8),
              ),
              child: Text(
                _result.isEmpty ? '위 버튼을 눌러 예제를 실행하세요' : _result,
                style: const TextStyle(fontFamily: 'monospace'),
              ),
            ),
          ],
        ),
      ),
    );
  }

  // 기본 JSON 변환 예제
  void _basicExample() {
    setState(() {
      _result = '=== 기본 JSON 변환 ===\n\n';

      // JSON 디코딩
      final jsonString = '{"name": "홍길동", "age": 25}';
      final decoded = CustomJsonUtil.decode(jsonString);
      _result += '원본: $jsonString\n';
      _result += '디코딩: $decoded\n';
      _result += 'name: ${decoded?['name']}\n';
      _result += 'age: ${decoded?['age']}\n\n';

      // JSON 인코딩
      final map = {'name': '김철수', 'age': 30};
      final encoded = CustomJsonUtil.encode(map);
      _result += '원본 Map: $map\n';
      _result += '인코딩: $encoded\n';
    });
  }

  // 객체 ↔ JSON 변환 예제
  void _objectExample() {
    setState(() {
      _result = '=== 객체 ↔ JSON 변환 ===\n\n';

      // User 클래스 예제
      final userJson = {'name': '홍길동', 'age': 25, 'email': 'hong@example.com'};

      // JSON → 객체
      final jsonString = CustomJsonUtil.encode(userJson);
      _result += 'JSON 문자열: $jsonString\n\n';

      // 객체 → JSON (실제로는 fromJson 메서드가 필요하지만 예제용)
      _result += '객체 변환 예제:\n';
      _result += 'User(name: ${userJson['name']}, age: ${userJson['age']})\n\n';

      // 리스트 변환
      final usersJson = [
        userJson,
        {'name': '김철수', 'age': 30},
      ];
      final usersJsonString = CustomJsonUtil.encode(usersJson);
      _result += '리스트 JSON: $usersJsonString\n';
    });
  }

  // JSON 검증 예제
  void _validationExample() {
    setState(() {
      _result = '=== JSON 검증 ===\n\n';

      final validJson = '{"name": "홍길동"}';
      final invalidJson = '{name: 홍길동}'; // 따옴표 없음

      _result += '유효한 JSON: $validJson\n';
      _result += '검증 결과: ${CustomJsonUtil.isValid(validJson)}\n\n';

      _result += '유효하지 않은 JSON: $invalidJson\n';
      _result += '검증 결과: ${CustomJsonUtil.isValid(invalidJson)}\n';
    });
  }

  // JSON 포맷팅 예제
  void _formattingExample() {
    setState(() {
      _result = '=== JSON 포맷팅 ===\n\n';

      final jsonString = '{"name":"홍길동","age":25,"email":"hong@example.com"}';
      _result += '원본 (압축):\n$jsonString\n\n';

      final formatted = CustomJsonUtil.format(jsonString);
      _result += '포맷팅 (들여쓰기):\n$formatted\n\n';

      final compressed = CustomJsonUtil.compress(formatted ?? '');
      _result += '압축 (공백 제거):\n$compressed\n';
    });
  }

  // JSON 병합 예제
  void _mergeExample() {
    setState(() {
      _result = '=== JSON 병합 ===\n\n';

      final json1 = {'name': '홍길동', 'age': 25};
      final json2 = {'email': 'hong@example.com', 'city': '서울'};

      _result += 'JSON 1: $json1\n';
      _result += 'JSON 2: $json2\n\n';

      final merged = CustomJsonUtil.merge(json1, json2);
      _result += '병합 결과: $merged\n';
    });
  }

  // 경로로 값 가져오기/설정 예제
  void _pathExample() {
    setState(() {
      _result = '=== 경로로 값 가져오기/설정 ===\n\n';

      final json = {
        'user': {
          'name': '홍길동',
          'age': 25,
          'address': {'city': '서울', 'street': '강남구'},
        },
      };

      _result +=
          '원본 JSON:\n${CustomJsonUtil.format(CustomJsonUtil.encode(json) ?? '')}\n\n';

      // 값 가져오기
      final name = CustomJsonUtil.getValue(json, 'user.name');
      final city = CustomJsonUtil.getValue(json, 'user.address.city');
      _result += 'user.name: $name\n';
      _result += 'user.address.city: $city\n\n';

      // 값 설정하기
      CustomJsonUtil.setValue(json, 'user.email', 'hong@example.com');
      CustomJsonUtil.setValue(json, 'user.address.zipcode', '12345');
      _result +=
          '값 설정 후:\n${CustomJsonUtil.format(CustomJsonUtil.encode(json) ?? '')}\n\n';

      // 값 삭제하기
      CustomJsonUtil.removeValue(json, 'user.age');
      _result +=
          'user.age 삭제 후:\n${CustomJsonUtil.format(CustomJsonUtil.encode(json) ?? '')}\n';
    });
  }
}
