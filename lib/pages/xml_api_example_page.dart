import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

import '../custom/util/json/custom_json_util.dart';
import '../custom/util/xml/custom_xml_util.dart';
import '../custom/widgets.dart';
import '../theme/app_colors.dart';

/// 서울시 지하철 실시간 도착 정보 API 파싱 예제 페이지
class XmlApiExamplePage extends StatefulWidget {
  const XmlApiExamplePage({super.key});

  @override
  State<XmlApiExamplePage> createState() => _XmlApiExamplePageState();
}

class _XmlApiExamplePageState extends State<XmlApiExamplePage> {
  String _result = '';
  bool _isLoading = false;
  Map<String, dynamic>? _parsedData;
  final TextEditingController _searchController = TextEditingController();
  List<MapEntry<String, dynamic>> _searchResults = [];

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final p = context.palette;
    return Scaffold(
      backgroundColor: p.background,
      appBar: CustomAppBar(
        title: 'XML API 파싱 예제',
        backgroundColor: Colors.deepOrange,
        foregroundColor: Colors.white,
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
                    '서울시 지하철 실시간 도착 정보',
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                    color: p.textPrimary,
                  ),
                  CustomText(
                    'XML API를 파싱하여 Map으로 변환하고 순환 출력하는 예제',
                    fontSize: 14,
                    color: p.textSecondary,
                  ),
                ],
              ),
              const SizedBox(height: 8),

              // API 정보 카드
              CustomCard(
                padding: const EdgeInsets.all(16),
                child: CustomColumn(
                  spacing: 12,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    CustomText(
                      '📡 API 정보',
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                    ),
                    CustomText(
                      'URL: http://swopenapi.seoul.go.kr/api/subway/6f73517352636865353159466c7045/xml/realtimeStationArrival/ALL/',
                      fontSize: 12,
                      color: p.textSecondary,
                    ),
                    CustomText(
                      '형식: XML',
                      fontSize: 12,
                      color: p.textSecondary,
                    ),
                  ],
                ),
              ),

              // 버튼
              SizedBox(
                width: double.infinity,
                child: CustomButton(
                  btnText: _isLoading ? '로딩 중...' : 'API 데이터 가져오기',
                  backgroundColor: Colors.deepOrange,
                  onCallBack: _isLoading
                      ? () {}
                      : () {
                          _fetchAndParseXml();
                        },
                ),
              ),

              // 결과 표시
              if (_result.isNotEmpty)
                CustomCard(
                  padding: const EdgeInsets.all(16),
                  child: CustomColumn(
                    spacing: 12,
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      CustomText(
                        '📊 파싱 결과',
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                      ),
                      Container(
                        padding: const EdgeInsets.all(12),
                        decoration: BoxDecoration(
                          color: Colors.grey[100],
                          borderRadius: BorderRadius.circular(8),
                        ),
                        child: SelectableText(
                          _result,
                          style: const TextStyle(
                            fontFamily: 'monospace',
                            fontSize: 12,
                          ),
                        ),
                      ),
                    ],
                  ),
                ),

              // 키 검색 섹션
              if (_parsedData != null)
                CustomCard(
                  padding: const EdgeInsets.all(16),
                  child: CustomColumn(
                    spacing: 12,
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      CustomText(
                        '🔍 키 검색',
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                      ),
                      CustomRow(
                        spacing: 8,
                        children: [
                          Expanded(
                            child: CustomTextField(
                              controller: _searchController,
                              hintText: '검색할 키 입력 (예: statnNm, subwayId)',
                              onSubmitted: (value) {
                                _searchKey(value);
                              },
                            ),
                          ),
                          CustomButton(
                            btnText: '검색',
                            backgroundColor: Colors.blue,
                            minimumSize: const Size(80, 48),
                            onCallBack: () {
                              _searchKey(_searchController.text);
                            },
                          ),
                        ],
                      ),
                      if (_searchResults.isNotEmpty) ...[
                        const SizedBox(height: 8),
                        CustomText(
                          '검색 결과: ${_searchResults.length}개',
                          fontSize: 14,
                          fontWeight: FontWeight.bold,
                          color: Colors.blue,
                        ),
                        const SizedBox(height: 8),
                        Container(
                          constraints: const BoxConstraints(maxHeight: 300),
                          decoration: BoxDecoration(
                            color: Colors.blue.shade50,
                            borderRadius: BorderRadius.circular(8),
                            border: Border.all(color: Colors.blue.shade200),
                          ),
                          child: ListView.builder(
                            shrinkWrap: true,
                            itemCount: _searchResults.length,
                            itemBuilder: (context, index) {
                              final entry = _searchResults[index];
                              return Padding(
                                padding: const EdgeInsets.all(8.0),
                                child: CustomColumn(
                                  spacing: 4,
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    CustomText(
                                      '키: ${entry.key}',
                                      fontSize: 12,
                                      fontWeight: FontWeight.bold,
                                      color: Colors.blue.shade900,
                                    ),
                                    CustomText(
                                      '값: ${_formatValue(entry.value)}',
                                      fontSize: 12,
                                      color: Colors.blue.shade800,
                                    ),
                                    const Divider(height: 8),
                                  ],
                                ),
                              );
                            },
                          ),
                        ),
                      ] else if (_searchController.text.isNotEmpty &&
                          _parsedData != null) ...[
                        const SizedBox(height: 8),
                        CustomText(
                          '검색 결과가 없습니다.',
                          fontSize: 12,
                          color: Colors.grey.shade600,
                        ),
                      ],
                    ],
                  ),
                ),

              // Map 데이터 상세 표시
              if (_parsedData != null)
                CustomCard(
                  padding: const EdgeInsets.all(16),
                  child: CustomColumn(
                    spacing: 12,
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      CustomText(
                        '🗺️ Map 데이터 구조',
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                      ),
                      _buildMapWidget(_parsedData!),
                    ],
                  ),
                ),
            ],
          ),
        ),
      ),
    );
  }

  /// XML API를 가져와서 파싱하는 함수
  Future<void> _fetchAndParseXml() async {
    setState(() {
      _isLoading = true;
      _result = '요청 중...\n';
      _parsedData = null;
    });

    try {
      // API 요청
      final url = Uri.parse(
        'http://swopenapi.seoul.go.kr/api/subway/sample/xml/realtimeStationArrival/ALL/',
      );
      final response = await http.get(url);

      if (response.statusCode == 200) {
        // 한글 깨짐 방지를 위해 UTF-8로 명시적으로 디코딩
        String xmlString;
        try {
          // Content-Type 헤더에서 charset 확인
          final contentType = response.headers['content-type'] ?? '';
          if (contentType.contains('charset=')) {
            final charset = contentType
                .split('charset=')[1]
                .split(';')[0]
                .trim()
                .toLowerCase();
            if (charset == 'euc-kr' || charset == 'ks_c_5601-1987') {
              // EUC-KR 인코딩인 경우
              xmlString = _decodeEucKr(response.bodyBytes);
            } else {
              // 기본적으로 UTF-8로 디코딩
              xmlString = utf8.decode(response.bodyBytes);
            }
          } else {
            // charset 정보가 없으면 UTF-8로 디코딩 시도
            xmlString = utf8.decode(response.bodyBytes);
          }
        } catch (e) {
          // 디코딩 실패 시 기본 body 사용
          xmlString = response.body;
        }

        setState(() {
          _result = '=== API 응답 성공 ===\n\n';
          _result += '상태 코드: ${response.statusCode}\n';
          _result += '응답 길이: ${xmlString.length} bytes\n';
          _result += 'Content-Type: ${response.headers['content-type'] ?? 'N/A'}\n\n';

          // XML 검증
          if (CustomXmlUtil.isValid(xmlString)) {
            _result += '✅ 유효한 XML입니다\n\n';

            // XML을 Map으로 변환
            final map = CustomXmlUtil.toMap(xmlString);
            if (map != null) {
              _parsedData = map;
              _result += '✅ Map 변환 성공!\n\n';
              _result += '=== Map 구조 ===\n';
              _result += CustomJsonUtil.formatMap(map);
              _result += '\n\n=== 순환 출력 ===\n';
              _result += _iterateMap(map);
            } else {
              _result += '❌ Map 변환 실패\n';
            }
          } else {
            _result += '❌ 유효하지 않은 XML입니다\n';
            _result += '원본 XML (처음 500자):\n';
            _result += xmlString.length > 500
                ? '${xmlString.substring(0, 500)}...'
                : xmlString;
          }
        });
      } else {
        // 에러 응답도 UTF-8로 디코딩
        String errorBody;
        try {
          errorBody = utf8.decode(response.bodyBytes);
        } catch (e) {
          errorBody = response.body;
        }
        
        setState(() {
          _result = '❌ API 요청 실패\n';
          _result += '상태 코드: ${response.statusCode}\n';
          _result += '응답: $errorBody';
        });
      }
    } catch (e) {
      setState(() {
        _result = '❌ 에러 발생\n';
        _result += '에러 메시지: $e\n';
        _result += '\n인터넷 연결을 확인해주세요.';
      });
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  /// Map을 순환하며 출력
  String _iterateMap(Map<String, dynamic> map) {
    final buffer = StringBuffer();
    int itemCount = 0;

    void iterate(dynamic data, String prefix) {
      if (data is Map<String, dynamic>) {
        for (final entry in data.entries) {
          final key = entry.key;
          final value = entry.value;

          if (key == 'row' && value is List) {
            // 'row' 키의 리스트를 순환
            buffer.writeln('\n--- 지하철 도착 정보 (${value.length}개) ---\n');
            for (int i = 0; i < value.length; i++) {
              itemCount++;
              final item = value[i];
              if (item is Map<String, dynamic>) {
                buffer.writeln('[$itemCount] 역 정보:');
                _printMapItem(item, buffer, prefix: '  ');
                buffer.writeln('');
              }
            }
          } else if (value is Map<String, dynamic>) {
            buffer.writeln('$prefix$key:');
            iterate(value, '$prefix  ');
          } else if (value is List) {
            buffer.writeln('$prefix$key: [리스트 ${value.length}개]');
            for (int i = 0; i < value.length; i++) {
              iterate(value[i], '$prefix  [$i] ');
            }
          } else {
            buffer.writeln('$prefix$key: $value');
          }
        }
      } else if (data is List) {
        for (int i = 0; i < data.length; i++) {
          iterate(data[i], '$prefix[$i] ');
        }
      }
    }

    iterate(map, '');
    buffer.writeln('\n총 $itemCount개의 도착 정보를 찾았습니다.');
    return buffer.toString();
  }

  /// Map 항목을 출력하는 헬퍼 함수
  void _printMapItem(Map<String, dynamic> item, StringBuffer buffer,
      {String prefix = ''}) {
    for (final entry in item.entries) {
      final key = entry.key;
      final value = entry.value;
      buffer.writeln('$prefix$key: $value');
    }
  }

  /// Map 위젯을 재귀적으로 생성
  Widget _buildMapWidget(Map<String, dynamic> map) {
    return CustomColumn(
      spacing: 8,
      crossAxisAlignment: CrossAxisAlignment.start,
      children: map.entries.map((entry) {
        final key = entry.key;
        final value = entry.value;

        if (value is Map<String, dynamic>) {
          return ExpansionTile(
            title: CustomText(
              key,
              fontSize: 14,
              fontWeight: FontWeight.bold,
            ),
            children: [
              Padding(
                padding: const EdgeInsets.only(left: 16),
                child: _buildMapWidget(value),
              ),
            ],
          );
        } else if (value is List) {
          return ExpansionTile(
            title: CustomText(
              '$key (${value.length}개)',
              fontSize: 14,
              fontWeight: FontWeight.bold,
            ),
            children: value.asMap().entries.map((listEntry) {
              final index = listEntry.key;
              final item = listEntry.value;
              if (item is Map<String, dynamic>) {
                return Padding(
                  padding: const EdgeInsets.only(left: 16),
                  child: ExpansionTile(
                    title: CustomText(
                      '[$index] 항목',
                      fontSize: 12,
                    ),
                    children: [
                      Padding(
                        padding: const EdgeInsets.only(left: 16),
                        child: _buildMapWidget(item),
                      ),
                    ],
                  ),
                );
              } else {
                return Padding(
                  padding: const EdgeInsets.only(left: 32),
                  child: CustomText(
                    '[$index]: $item',
                    fontSize: 12,
                  ),
                );
              }
            }).toList(),
          );
        } else {
          return Padding(
            padding: const EdgeInsets.only(left: 16),
            child: CustomRow(
              spacing: 8,
              children: [
                CustomText(
                  '$key:',
                  fontSize: 12,
                  fontWeight: FontWeight.bold,
                ),
                Expanded(
                  child: CustomText(
                    value.toString(),
                    fontSize: 12,
                  ),
                ),
              ],
            ),
          );
        }
      }).toList(),
    );
  }

  /// 키 검색 함수
  void _searchKey(String searchKey) {
    if (searchKey.trim().isEmpty || _parsedData == null) {
      setState(() {
        _searchResults = [];
      });
      return;
    }

    final results = <MapEntry<String, dynamic>>[];
    final key = searchKey.trim();

    // Map을 재귀적으로 순회하며 키 검색
    void searchInMap(dynamic data, String path) {
      if (data is Map<String, dynamic>) {
        for (final entry in data.entries) {
          final currentPath = path.isEmpty ? entry.key : '$path.${entry.key}';
          
          // 키가 일치하는지 확인 (대소문자 구분 없이)
          if (entry.key.toLowerCase().contains(key.toLowerCase())) {
            results.add(MapEntry(currentPath, entry.value));
          }
          
          // 값이 Map이나 List인 경우 재귀적으로 검색
          if (entry.value is Map<String, dynamic>) {
            searchInMap(entry.value, currentPath);
          } else if (entry.value is List) {
            for (int i = 0; i < (entry.value as List).length; i++) {
              searchInMap(
                (entry.value as List)[i],
                '$currentPath[$i]',
              );
            }
          }
        }
      } else if (data is List) {
        for (int i = 0; i < data.length; i++) {
          searchInMap(data[i], '$path[$i]');
        }
      }
    }

    searchInMap(_parsedData!, '');
    
    setState(() {
      _searchResults = results;
    });
  }

  /// 값을 포맷팅하는 헬퍼 함수
  String _formatValue(dynamic value) {
    if (value == null) {
      return 'null';
    } else if (value is Map) {
      return '{Map with ${value.length} keys}';
    } else if (value is List) {
      return '[List with ${value.length} items]';
    } else {
      return value.toString();
    }
  }

  /// EUC-KR 인코딩을 UTF-8로 변환하는 헬퍼 함수
  /// 주의: Dart는 기본적으로 EUC-KR을 지원하지 않으므로,
  /// 대부분의 경우 UTF-8로 디코딩하면 됩니다.
  /// 만약 정말 EUC-KR이 필요하다면 `charset` 패키지를 사용해야 합니다.
  String _decodeEucKr(List<int> bytes) {
    // 대부분의 경우 UTF-8로 디코딩하면 됩니다
    // 실제로 서울시 API는 UTF-8을 사용합니다
    try {
      return utf8.decode(bytes);
    } catch (e) {
      // UTF-8 디코딩 실패 시 Latin1로 시도 (임시 방안)
      return latin1.decode(bytes);
    }
  }
}

