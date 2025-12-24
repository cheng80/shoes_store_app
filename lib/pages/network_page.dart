import 'package:flutter/material.dart';

import '../custom/external_util/network/custom_network_util.dart';
import '../custom/widgets.dart';
import '../theme/app_colors.dart';

/// NetworkUtil 사용 예제 페이지
///
/// 주의: 이 페이지를 사용하려면 pubspec.yaml에 http 패키지가 필요합니다.
class NetworkPage extends StatefulWidget {
  const NetworkPage({super.key});

  @override
  State<NetworkPage> createState() => _NetworkPageState();
}

class _NetworkPageState extends State<NetworkPage> {
  String _result = '';

  @override
  void initState() {
    super.initState();
    // 예제용 기본 URL 설정 (실제 API는 사용 불가)
    // CustomNetworkUtil.setBaseUrl('https://api.example.com');
  }

  @override
  Widget build(BuildContext context) {
    final p = context.palette;
    return Scaffold(
      backgroundColor: p.background,
      appBar: CustomAppBar(
        title: 'NetworkUtil 예제',
        backgroundColor: Colors.indigo, // 예제용 색상 유지
        foregroundColor: Colors.white,
      ),
      body: SingleChildScrollView(
        child: CustomPadding.all(
          16.0,
          child: CustomColumn(
            spacing: 16,
            children: [
              CustomText(
                'HTTP 통신 예제',
                fontSize: 24,
                fontWeight: FontWeight.bold,
                color: Colors.indigo, // 예제용 색상 유지
              ),
              CustomText(
                '주의: 실제 API 서버가 필요합니다',
                fontSize: 14,
                color: p.textSecondary,
              ),
              const SizedBox(height: 8),

              SizedBox(
                width: double.infinity,
                child: CustomButton(
                  btnText: 'GET 요청 예제',
                  // backgroundColor를 지정하지 않으면 테마 primary 색상 자동 적용
                  onCallBack: _getExample,
                ),
              ),

              SizedBox(
                width: double.infinity,
                child: CustomButton(
                  btnText: 'POST 요청 예제',
                  backgroundColor: Colors.green, // 예제용 색상 유지
                  onCallBack: _postExample,
                ),
              ),

              SizedBox(
                width: double.infinity,
                child: CustomButton(
                  btnText: 'PUT 요청 예제',
                  backgroundColor: Colors.orange, // 예제용 색상 유지
                  onCallBack: _putExample,
                ),
              ),

              SizedBox(
                width: double.infinity,
                child: CustomButton(
                  btnText: 'DELETE 요청 예제',
                  backgroundColor: Colors.red, // 예제용 색상 유지
                  onCallBack: _deleteExample,
                ),
              ),

              SizedBox(
                width: double.infinity,
                child: CustomButton(
                  btnText: '쿼리 파라미터 예제',
                  backgroundColor: Colors.purple, // 예제용 색상 유지
                  onCallBack: _queryParamsExample,
                ),
              ),

              SizedBox(
                width: double.infinity,
                child: CustomButton(
                  btnText: '에러 처리 예제',
                  backgroundColor: Colors.grey, // 예제용 색상 유지
                  onCallBack: _errorHandlingExample,
                ),
              ),

              const SizedBox(height: 16),

              // 결과 표시
              CustomCard(
                padding: const EdgeInsets.all(16),
                child: CustomText(
                  _result.isEmpty
                      ? '위 버튼을 눌러 예제를 실행하세요\n\n주의: 실제 API 서버가 필요합니다'
                      : _result,
                  fontSize: 12,
                  fontWeight: FontWeight.normal,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  /// GET 요청 예제
  void _getExample() async {
    setState(() {
      _result = '=== GET 요청 예제 ===\n\n';
      _result += '요청 중...\n';
    });

    // 실제 API 예제 (JSONPlaceholder 사용)
    final response = await CustomNetworkUtil.get<Map<String, dynamic>>(
      'https://jsonplaceholder.typicode.com/posts/1',
    );

    setState(() {
      if (response.success) {
        _result += '✅ 성공!\n';
        _result += '상태 코드: ${response.statusCode}\n';
        _result += '데이터: ${response.data}\n';
      } else {
        _result += '❌ 실패!\n';
        _result += '에러: ${response.error}\n';
        _result += '상태 코드: ${response.statusCode}\n';
      }
    });
  }

  /// POST 요청 예제
  void _postExample() async {
    setState(() {
      _result = '=== POST 요청 예제 ===\n\n';
      _result += '요청 중...\n';
    });

    // 실제 API 예제 (JSONPlaceholder 사용)
    final response = await CustomNetworkUtil.post<Map<String, dynamic>>(
      'https://jsonplaceholder.typicode.com/posts',
      body: {'title': '테스트 제목', 'body': '테스트 내용', 'userId': 1},
    );

    setState(() {
      if (response.success) {
        _result += '✅ 성공!\n';
        _result += '상태 코드: ${response.statusCode}\n';
        _result += '생성된 데이터:\n';
        _result += 'ID: ${response.data?['id']}\n';
        _result += '제목: ${response.data?['title']}\n';
        _result += '내용: ${response.data?['body']}\n';
      } else {
        _result += '❌ 실패!\n';
        _result += '에러: ${response.error}\n';
      }
    });
  }

  /// PUT 요청 예제
  void _putExample() async {
    setState(() {
      _result = '=== PUT 요청 예제 ===\n\n';
      _result += '요청 중...\n';
    });

    // 실제 API 예제 (JSONPlaceholder 사용)
    final response = await CustomNetworkUtil.put<Map<String, dynamic>>(
      'https://jsonplaceholder.typicode.com/posts/1',
      body: {'id': 1, 'title': '수정된 제목', 'body': '수정된 내용', 'userId': 1},
    );

    setState(() {
      if (response.success) {
        _result += '✅ 성공!\n';
        _result += '상태 코드: ${response.statusCode}\n';
        _result += '수정된 데이터:\n';
        _result += '제목: ${response.data?['title']}\n';
        _result += '내용: ${response.data?['body']}\n';
      } else {
        _result += '❌ 실패!\n';
        _result += '에러: ${response.error}\n';
      }
    });
  }

  /// DELETE 요청 예제
  void _deleteExample() async {
    setState(() {
      _result = '=== DELETE 요청 예제 ===\n\n';
      _result += '요청 중...\n';
    });

    // 실제 API 예제 (JSONPlaceholder 사용)
    final response = await CustomNetworkUtil.delete(
      'https://jsonplaceholder.typicode.com/posts/1',
    );

    setState(() {
      if (response.success) {
        _result += '✅ 성공!\n';
        _result += '상태 코드: ${response.statusCode}\n';
        _result += '데이터가 삭제되었습니다.\n';
      } else {
        _result += '❌ 실패!\n';
        _result += '에러: ${response.error}\n';
      }
    });
  }

  /// 쿼리 파라미터 예제
  void _queryParamsExample() async {
    setState(() {
      _result = '=== 쿼리 파라미터 예제 ===\n\n';
      _result += '요청 중...\n';
    });

    // 실제 API 예제 (JSONPlaceholder 사용)
    final response = await CustomNetworkUtil.get<List<dynamic>>(
      'https://jsonplaceholder.typicode.com/posts',
      queryParams: {'userId': '1', '_limit': '5'},
    );

    setState(() {
      if (response.success) {
        _result += '✅ 성공!\n';
        _result += '상태 코드: ${response.statusCode}\n';
        final dataList = response.data;
        _result += '받은 데이터 개수: ${dataList is List ? dataList.length : 0}\n';
        if (dataList is List && dataList.isNotEmpty) {
          _result += '\n첫 번째 항목:\n';
          _result += 'ID: ${dataList[0]['id']}\n';
          _result += '제목: ${dataList[0]['title']}\n';
        }
      } else {
        _result += '❌ 실패!\n';
        _result += '에러: ${response.error}\n';
      }
    });
  }

  /// 에러 처리 예제
  void _errorHandlingExample() async {
    setState(() {
      _result = '=== 에러 처리 예제 ===\n\n';
      _result += '잘못된 URL로 요청 중...\n';
    });

    // 존재하지 않는 URL로 요청 (에러 발생)
    final response = await CustomNetworkUtil.get<Map<String, dynamic>>(
      'https://invalid-url-that-does-not-exist.com/api',
    );

    setState(() {
      if (response.success) {
        _result += '✅ 성공!\n';
        _result += '데이터: ${response.data}\n';
      } else {
        _result += '❌ 실패 (예상된 동작)\n';
        _result += '에러: ${response.error}\n';
        _result += '상태 코드: ${response.statusCode}\n';
        _result += '\n에러 처리가 정상적으로 작동합니다!\n';
      }
    });
  }
}
