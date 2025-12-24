import 'package:flutter/material.dart';

import '../custom/util/address/custom_address_util.dart';
import '../custom/widgets.dart';
import '../theme/app_colors.dart';

/// AddressUtil 사용 예제 페이지
class AddressPage extends StatefulWidget {
  const AddressPage({super.key});

  @override
  State<AddressPage> createState() => _AddressPageState();
}

class _AddressPageState extends State<AddressPage> {
  // 각 예제별 결과와 로딩 상태
  String _result1 = ''; // 위도/경도로 주소 가져오기
  String _result2 = ''; // 간단한 주소 가져오기
  String _result3 = ''; // 상세 주소 정보 가져오기
  String _result4 = ''; // JSON 파싱 예제
  String _result5 = ''; // 예외 처리 예제

  bool _isLoading1 = false;
  bool _isLoading2 = false;
  bool _isLoading3 = false;

  @override
  Widget build(BuildContext context) {
    final p = context.palette;
    return Scaffold(
      backgroundColor: p.background,
      appBar: CustomAppBar(
        title: 'AddressUtil 예제',
        // backgroundColor와 foregroundColor를 지정하지 않으면 테마 색상 자동 적용
      ),
      body: SingleChildScrollView(
        child: CustomPadding.all(
          16.0,
          child: CustomColumn(
            spacing: 16,
            children: [
              // 제목 섹션
              CustomColumn(
                spacing: 8,
                children: [
                  CustomText(
                    'AddressUtil 예제',
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                    color: p.textPrimary,
                  ),
                  CustomText(
                    '위도/경도로 주소를 가져오는 예제입니다.',
                    fontSize: 14,
                    color: p.textSecondary,
                  ),
                ],
              ),

              // 위도/경도로 주소 가져오기
              CustomCard(
                padding: const EdgeInsets.all(16),
                child: CustomColumn(
                  spacing: 12,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    CustomText(
                      '위도/경도로 주소 가져오기',
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                    ),
                    CustomText(
                      '서울 가락동 좌표 (37.497429, 127.127782)',
                      fontSize: 14,
                      color: p.textSecondary,
                    ),
                    SizedBox(
                      width: double.infinity,
                      child: CustomButton(
                        btnText: _isLoading1 ? '로딩 중...' : '주소 가져오기',
                        // backgroundColor를 지정하지 않으면 테마 primary 색상 자동 적용
                        onCallBack: _isLoading1
                            ? () {}
                            : () {
                                _getAddressFromCoordinates();
                              },
                      ),
                    ),
                    // 결과 영역
                    if (_result1.isNotEmpty)
                      Container(
                        width: double.infinity,
                        margin: const EdgeInsets.only(top: 12),
                        padding: const EdgeInsets.all(12),
                        decoration: BoxDecoration(
                          color: Colors.blue[50],
                          borderRadius: BorderRadius.circular(8),
                          border: Border.all(color: Colors.blue[200]!),
                        ),
                        child: SelectableText(
                          _result1,
                          style: const TextStyle(
                            fontFamily: 'monospace',
                            fontSize: 12,
                          ),
                        ),
                      ),
                  ],
                ),
              ),

              // 간단한 주소 가져오기
              CustomCard(
                padding: const EdgeInsets.all(16),
                child: CustomColumn(
                  spacing: 12,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    CustomText(
                      '간단한 주소 가져오기 (국가 제외)',
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                    ),
                    CustomText(
                      '서울 가락동 좌표 (37.497429, 127.127782)',
                      fontSize: 14,
                      color: p.textSecondary,
                    ),
                    SizedBox(
                      width: double.infinity,
                      child: CustomButton(
                        btnText: _isLoading2 ? '로딩 중...' : '간단한 주소 가져오기',
                        backgroundColor: Colors.green, // 예제용 색상 유지
                        onCallBack: _isLoading2
                            ? () {}
                            : () {
                                _getSimpleAddressFromCoordinates();
                              },
                      ),
                    ),
                    // 결과 영역
                    if (_result2.isNotEmpty)
                      Container(
                        width: double.infinity,
                        margin: const EdgeInsets.only(top: 12),
                        padding: const EdgeInsets.all(12),
                        decoration: BoxDecoration(
                          color: Colors.green[50],
                          borderRadius: BorderRadius.circular(8),
                          border: Border.all(color: Colors.green[200]!),
                        ),
                        child: SelectableText(
                          _result2,
                          style: const TextStyle(
                            fontFamily: 'monospace',
                            fontSize: 12,
                          ),
                        ),
                      ),
                  ],
                ),
              ),

              // 상세 주소 정보 가져오기
              CustomCard(
                padding: const EdgeInsets.all(16),
                child: CustomColumn(
                  spacing: 12,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    CustomText(
                      '상세 주소 정보 가져오기',
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                    ),
                    CustomText(
                      '서울 가락동 좌표 (37.497429, 127.127782)',
                      fontSize: 14,
                      color: p.textSecondary,
                    ),
                    SizedBox(
                      width: double.infinity,
                      child: CustomButton(
                        btnText: _isLoading3 ? '로딩 중...' : '상세 정보 가져오기',
                        backgroundColor: Colors.purple, // 예제용 색상 유지
                        onCallBack: _isLoading3
                            ? () {}
                            : () {
                                _getAddressInfoFromCoordinates();
                              },
                      ),
                    ),
                    // 결과 영역
                    if (_result3.isNotEmpty)
                      Container(
                        width: double.infinity,
                        margin: const EdgeInsets.only(top: 12),
                        padding: const EdgeInsets.all(12),
                        decoration: BoxDecoration(
                          color: Colors.purple[50],
                          borderRadius: BorderRadius.circular(8),
                          border: Border.all(color: Colors.purple[200]!),
                        ),
                        child: SelectableText(
                          _result3,
                          style: const TextStyle(
                            fontFamily: 'monospace',
                            fontSize: 12,
                          ),
                        ),
                      ),
                  ],
                ),
              ),

              // JSON 파싱 예제
              CustomCard(
                padding: const EdgeInsets.all(16),
                child: CustomColumn(
                  spacing: 12,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    CustomText(
                      'JSON 문자열 파싱',
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                    ),
                    CustomText(
                      'JSON 문자열에서 주소 추출',
                      fontSize: 14,
                      color: Colors.grey[700],
                    ),
                    SizedBox(
                      width: double.infinity,
                      child: CustomButton(
                        btnText: 'JSON 파싱 예제',
                        backgroundColor: Colors.orange, // 예제용 색상 유지
                        onCallBack: _parseJsonExample,
                      ),
                    ),
                    // 결과 영역
                    if (_result4.isNotEmpty)
                      Container(
                        width: double.infinity,
                        margin: const EdgeInsets.only(top: 12),
                        padding: const EdgeInsets.all(12),
                        decoration: BoxDecoration(
                          color: Colors.orange[50],
                          borderRadius: BorderRadius.circular(8),
                          border: Border.all(color: Colors.orange[200]!),
                        ),
                        child: SelectableText(
                          _result4,
                          style: const TextStyle(
                            fontFamily: 'monospace',
                            fontSize: 12,
                          ),
                        ),
                      ),
                  ],
                ),
              ),

              // 예외 처리 예제
              CustomCard(
                padding: const EdgeInsets.all(16),
                child: CustomColumn(
                  spacing: 12,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    CustomText(
                      '예외 처리 예제',
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                    ),
                    CustomText(
                      '유효하지 않은 좌표로 예외 처리 테스트',
                      fontSize: 14,
                      color: Colors.grey[700],
                    ),
                    SizedBox(
                      width: double.infinity,
                      child: CustomButton(
                        btnText: '예외 처리 테스트',
                        backgroundColor: Colors.red, // 예제용 색상 유지
                        onCallBack: () => _exceptionExample(),
                      ),
                    ),
                    // 결과 영역
                    if (_result5.isNotEmpty)
                      Container(
                        width: double.infinity,
                        margin: const EdgeInsets.only(top: 12),
                        padding: const EdgeInsets.all(12),
                        decoration: BoxDecoration(
                          color: Colors.red[50],
                          borderRadius: BorderRadius.circular(8),
                          border: Border.all(color: Colors.red[200]!),
                        ),
                        child: SelectableText(
                          _result5,
                          style: const TextStyle(
                            fontFamily: 'monospace',
                            fontSize: 12,
                          ),
                        ),
                      ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  /// 위도/경도로 주소 가져오기
  Future<void> _getAddressFromCoordinates() async {
    setState(() {
      _isLoading1 = true;
      _result1 = '주소를 가져오는 중...\n';
    });

    try {
      final address = await CustomAddressUtil.getAddressFromCoordinates(
        37.497429,
        127.127782,
      );

      setState(() {
        _isLoading1 = false;
        _result1 = '=== 위도/경도로 주소 가져오기 ===\n\n';
        _result1 += '위도: 37.497429\n';
        _result1 += '경도: 127.127782\n\n';
        _result1 += '주소: $address\n';
      });
    } on AddressException catch (e) {
      setState(() {
        _isLoading1 = false;
        _result1 = '❌ 오류 발생\n\n';
        _result1 += '메시지: ${e.message}\n';
        _result1 += '코드: ${e.code}\n';
      });
    } catch (e) {
      setState(() {
        _isLoading1 = false;
        _result1 = '❌ 알 수 없는 오류: $e';
      });
    }
  }

  /// 간단한 주소 가져오기
  Future<void> _getSimpleAddressFromCoordinates() async {
    setState(() {
      _isLoading2 = true;
      _result2 = '간단한 주소를 가져오는 중...\n';
    });

    try {
      final address = await CustomAddressUtil.getSimpleAddressFromCoordinates(
        37.497429,
        127.127782,
      );

      setState(() {
        _isLoading2 = false;
        _result2 = '=== 간단한 주소 가져오기 (국가 제외) ===\n\n';
        _result2 += '위도: 37.497429\n';
        _result2 += '경도: 127.127782\n\n';
        _result2 += '주소: $address\n';
      });
    } on AddressException catch (e) {
      setState(() {
        _isLoading2 = false;
        _result2 = '❌ 오류 발생\n\n';
        _result2 += '메시지: ${e.message}\n';
        _result2 += '코드: ${e.code}\n';
      });
    } catch (e) {
      setState(() {
        _isLoading2 = false;
        _result2 = '❌ 알 수 없는 오류: $e';
      });
    }
  }

  /// 상세 주소 정보 가져오기
  Future<void> _getAddressInfoFromCoordinates() async {
    setState(() {
      _isLoading3 = true;
      _result3 = '상세 주소 정보를 가져오는 중...\n';
    });

    try {
      final addressInfo = await CustomAddressUtil.getAddressInfoFromCoordinates(
        37.497429,
        127.127782,
      );

      setState(() {
        _isLoading3 = false;
        _result3 = '=== 상세 주소 정보 ===\n\n';
        _result3 += '위도: 37.497429\n';
        _result3 += '경도: 127.127782\n\n';
        if (addressInfo != null) {
          _result3 += '국가: ${addressInfo['countryName']}\n';
          _result3 += '시/도: ${addressInfo['province']}\n';
          _result3 += '시: ${addressInfo['city']}\n';
          _result3 += '구: ${addressInfo['district']}\n';
          _result3 += '동: ${addressInfo['locality']}\n';
          _result3 += '전체 주소: ${addressInfo['fullAddress']}\n';
        } else {
          _result3 += '주소 정보를 가져올 수 없습니다.\n';
        }
      });
    } on AddressException catch (e) {
      setState(() {
        _isLoading3 = false;
        _result3 = '❌ 오류 발생\n\n';
        _result3 += '메시지: ${e.message}\n';
        _result3 += '코드: ${e.code}\n';
      });
    } catch (e) {
      setState(() {
        _isLoading3 = false;
        _result3 = '❌ 알 수 없는 오류: $e';
      });
    }
  }

  /// JSON 파싱 예제
  void _parseJsonExample() {
    const jsonString = '''
{
  "latitude": 37.497429,
  "longitude": 127.127782,
  "countryName": "대한민국",
  "countryCode": "KR",
  "principalSubdivision": "서울특별시",
  "city": "서울특별시",
  "locality": "가락2동",
  "localityInfo": {
    "administrative": [
      {
        "name": "대한민국",
        "adminLevel": 2
      },
      {
        "name": "서울특별시",
        "adminLevel": 4
      },
      {
        "name": "송파구",
        "adminLevel": 6
      },
      {
        "name": "가락2동",
        "adminLevel": 8
      }
    ]
  }
}
''';

    try {
      final address = CustomAddressUtil.parseAddress(jsonString);
      final simpleAddress = CustomAddressUtil.parseSimpleAddress(jsonString);
      final addressInfo = CustomAddressUtil.getAddressInfo(jsonString);

      setState(() {
        _result4 = '=== JSON 문자열 파싱 ===\n\n';
        _result4 += '전체 주소: $address\n';
        _result4 += '간단한 주소: $simpleAddress\n\n';
        if (addressInfo != null) {
          _result4 += '상세 정보:\n';
          _result4 += '- 국가: ${addressInfo['countryName']}\n';
          _result4 += '- 시/도: ${addressInfo['province']}\n';
          _result4 += '- 구: ${addressInfo['district']}\n';
          _result4 += '- 동: ${addressInfo['locality']}\n';
        }
      });
    } on AddressException catch (e) {
      setState(() {
        _result4 = '❌ JSON 파싱 오류\n\n';
        _result4 += '메시지: ${e.message}\n';
        _result4 += '코드: ${e.code}\n';
      });
    } catch (e) {
      setState(() {
        _result4 = '❌ 알 수 없는 오류: $e';
      });
    }
  }

  /// 예외 처리 예제
  Future<void> _exceptionExample() async {
    setState(() {
      _result5 = '예외 처리 테스트 중...\n';
    });

    try {
      // 유효하지 않은 좌표로 테스트
      await CustomAddressUtil.getAddressFromCoordinates(999, 999);
    } on AddressException catch (e) {
      setState(() {
        _result5 = '=== 예외 처리 예제 ===\n\n';
        _result5 += '✅ 예외가 정상적으로 처리되었습니다.\n\n';
        _result5 += '예외 타입: AddressException\n';
        _result5 += '메시지: ${e.message}\n';
        _result5 += '코드: ${e.code}\n';
      });
    } catch (e) {
      setState(() {
        _result5 = '❌ 예상치 못한 오류: $e';
      });
    }
  }
}

