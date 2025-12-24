import 'package:flutter/material.dart';

import 'address_page.dart';
import 'json_api_example_page.dart';
import 'network_page.dart';
import 'storage_page.dart';
import 'xml_api_example_page.dart';
import '../custom/util/collection/example.dart';
import '../custom/util/json/example.dart';
import '../custom/util/xml/example.dart';
import '../custom/util/timer/example.dart';
import '../custom/util/log/example.dart';
import '../custom/widgets.dart';
import '../theme/app_colors.dart';

/// 유틸리티 예제 페이지 목록
class UtilPage extends StatelessWidget {
  const UtilPage({super.key});

  @override
  Widget build(BuildContext context) {
    final p = context.palette;
    return Scaffold(
      backgroundColor: p.background,
      appBar: CustomAppBar(
        title: '유틸리티 예제',
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
                    '유틸리티 클래스 예제',
                    fontSize: 28,
                    fontWeight: FontWeight.bold,
                    color: p.textPrimary,
                  ),
                  CustomText(
                    '구현된 유틸리티 클래스들의 사용 예제를 확인할 수 있습니다.',
                    fontSize: 16,
                    color: p.textSecondary,
                  ),
                ],
              ),
              const SizedBox(height: 8),

              // StorageUtil 예제
              CustomCard(
                padding: const EdgeInsets.all(16),
                child: CustomColumn(
                  spacing: 12,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    CustomText(
                      'StorageUtil',
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                    CustomText(
                      '로컬 데이터 저장 유틸리티 (SharedPreferences 래핑)',
                      fontSize: 14,
                      color: p.textSecondary,
                    ),
                    CustomText(
                      '⚠️ 별도 페이지로 이동: StorageUtil 예제 페이지',
                      fontSize: 12,
                      color: Colors.orange[700]!, // 경고 색상은 유지
                    ),
                    SizedBox(
                      width: double.infinity,
                      child: CustomButton(
                        btnText: '예제 보기',
                        onCallBack: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (context) => const StoragePage(),
                            ),
                          );
                        },
                      ),
                    ),
                  ],
                ),
              ),

              // CollectionUtil 예제
              CustomCard(
                padding: const EdgeInsets.all(16),
                child: CustomColumn(
                  spacing: 12,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    CustomText(
                      'CollectionUtil',
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                    CustomText(
                      '컬렉션(리스트, 맵) 조작 유틸리티',
                      fontSize: 14,
                      color: p.textSecondary,
                    ),
                    SizedBox(
                      width: double.infinity,
                      child: CustomButton(
                        btnText: '예제 보기',
                        onCallBack: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (context) =>
                                  const CollectionExamplePage(),
                            ),
                          );
                        },
                      ),
                    ),
                  ],
                ),
              ),

              // TimerUtil 예제
              CustomCard(
                padding: const EdgeInsets.all(16),
                child: CustomColumn(
                  spacing: 12,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    CustomText(
                      'TimerUtil',
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                    CustomText(
                      '타이머 관리 유틸리티 (Unity Coroutine 유사 기능)',
                      fontSize: 14,
                      color: Colors.grey[700]!,
                    ),
                    SizedBox(
                      width: double.infinity,
                      child: CustomButton(
                        btnText: '예제 보기',
                        onCallBack: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (context) => const TimerExamplePage(),
                            ),
                          );
                        },
                      ),
                    ),
                  ],
                ),
              ),

              // JsonUtil 예제
              CustomCard(
                padding: const EdgeInsets.all(16),
                child: CustomColumn(
                  spacing: 12,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    CustomText(
                      'JsonUtil',
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                    CustomText(
                      'JSON 변환 유틸리티 (저장소와 무관한 순수 JSON 변환)',
                      fontSize: 14,
                      color: Colors.grey[700]!,
                    ),
                    SizedBox(
                      width: double.infinity,
                      child: CustomButton(
                        btnText: '예제 보기',
                        onCallBack: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (context) => const JsonUtilExamplePage(),
                            ),
                          );
                        },
                      ),
                    ),
                    const SizedBox(height: 8),
                    SizedBox(
                      width: double.infinity,
                      child: CustomButton(
                        btnText: 'JSON API 파싱 예제',
                        backgroundColor: Colors.blue,
                        onCallBack: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (context) => const JsonApiExamplePage(),
                            ),
                          );
                        },
                      ),
                    ),
                  ],
                ),
              ),

              // XmlUtil 예제
              CustomCard(
                padding: const EdgeInsets.all(16),
                child: CustomColumn(
                  spacing: 12,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    CustomText(
                      'XmlUtil',
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                    CustomText(
                      'XML 변환 유틸리티 (저장소와 무관한 순수 XML 변환)',
                      fontSize: 14,
                      color: Colors.grey[700]!,
                    ),
                    SizedBox(
                      width: double.infinity,
                      child: CustomButton(
                        btnText: '예제 보기',
                        onCallBack: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (context) => const XmlUtilExamplePage(),
                            ),
                          );
                        },
                      ),
                    ),
                    const SizedBox(height: 8),
                    SizedBox(
                      width: double.infinity,
                      child: CustomButton(
                        btnText: 'XML API 파싱 예제',
                        backgroundColor: Colors.deepOrange,
                        onCallBack: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (context) => const XmlApiExamplePage(),
                            ),
                          );
                        },
                      ),
                    ),
                  ],
                ),
              ),

              // AddressUtil 예제
              CustomCard(
                padding: const EdgeInsets.all(16),
                child: CustomColumn(
                  spacing: 12,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    CustomText(
                      'AddressUtil',
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                    CustomText(
                      '위도/경도로 주소 가져오기 유틸리티 (BigDataCloud API)',
                      fontSize: 14,
                      color: Colors.grey[700]!,
                    ),
                    SizedBox(
                      width: double.infinity,
                      child: CustomButton(
                        btnText: '예제 보기',
                        onCallBack: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (context) => const AddressPage(),
                            ),
                          );
                        },
                      ),
                    ),
                  ],
                ),
              ),

              // NetworkUtil 예제
              CustomCard(
                padding: const EdgeInsets.all(16),
                child: CustomColumn(
                  spacing: 12,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    CustomText(
                      'NetworkUtil',
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                    CustomText(
                      'HTTP 통신 유틸리티 (GET, POST, PUT, DELETE, PATCH)',
                      fontSize: 14,
                      color: Colors.grey[700]!,
                    ),
                    CustomText(
                      '⚠️ 별도 페이지로 이동: NetworkUtil 예제 페이지',
                      fontSize: 12,
                      color: Colors.orange[700]!, // 경고 색상은 유지
                    ),
                    SizedBox(
                      width: double.infinity,
                      child: CustomButton(
                        btnText: '예제 보기',
                        onCallBack: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (context) => const NetworkPage(),
                            ),
                          );
                        },
                      ),
                    ),
                  ],
                ),
              ),

              // AppLogger 예제
              CustomCard(
                padding: const EdgeInsets.all(16),
                child: CustomColumn(
                  spacing: 12,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    CustomText(
                      'AppLogger',
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                    CustomText(
                      '앱 전역 로깅 유틸리티 (디버그/정보/경고/에러/성공 로그)',
                      fontSize: 14,
                      color: Colors.grey[700]!,
                    ),
                    SizedBox(
                      width: double.infinity,
                      child: CustomButton(
                        btnText: '예제 보기',
                        onCallBack: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (context) => const LogExamplePage(),
                            ),
                          );
                        },
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
}
