import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import '../custom/widgets.dart';
import '../theme/app_colors.dart';

/// Picker 및 Grid 위젯 사용 예제 페이지
class PickerGridPage extends StatefulWidget {
  const PickerGridPage({super.key});

  @override
  State<PickerGridPage> createState() => _PickerGridPageState();
}

class _PickerGridPageState extends State<PickerGridPage> {
  // DatePicker 상태
  DateTime? _selectedDate;
  DateTimeRange? _selectedDateRange;

  // CupertinoDatePicker 상태
  DateTime _cupertinoDate = DateTime.now();

  // PickerView 상태
  String? _selectedPickerItem;
  final List<String> _pickerItems = ['옵션 1', '옵션 2', '옵션 3', '옵션 4', '옵션 5'];
  List<String> _selectedMultiItems = [];

  // GridView 상태
  final List<Map<String, dynamic>> _gridItems = List.generate(
    20,
    (index) => {
      'id': index,
      'title': '아이템 ${index + 1}',
      'color': Colors.primaries[index % Colors.primaries.length],
    },
  );

  @override
  Widget build(BuildContext context) {
    final p = context.palette;
    return Scaffold(
      backgroundColor: p.background,
      appBar: CustomAppBar(
        title: "Picker & Grid 예시",
        backgroundColor: Colors.indigo, // 예제용 색상 유지
      ),
      body: SingleChildScrollView(
        child: CustomPadding.all(
          16.0,
          child: CustomColumn(
            spacing: 24,
            children: [
              // 제목
              CustomText(
                "Picker 및 Grid 위젯 종합 예시",
                fontSize: 24,
                fontWeight: FontWeight.bold,
                color: Colors.indigo, // 예제용 색상 유지
              ),

              // DatePicker 섹션
              CustomCard(
                padding: const EdgeInsets.all(20),
                child: CustomColumn(
                  spacing: 16,
                  children: [
                    CustomText(
                      "📅 DatePicker 예시",
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                    CustomText(
                      "Material Design 날짜 선택 다이얼로그",
                      fontSize: 14,
                      color: p.textSecondary,
                    ),
                    CustomRow(
                      spacing: 12,
                      children: [
                        Expanded(
                          child: CustomButton(
                            btnText: "날짜 선택",
                            // backgroundColor를 지정하지 않으면 테마 primary 색상 자동 적용
                            onCallBack: () async {
                              final date = await CustomDatePicker.show(
                                context: context,
                                initialDate: _selectedDate ?? DateTime.now(),
                                firstDate: DateTime(2000),
                                lastDate: DateTime(2100),
                                helpText: "날짜를 선택하세요",
                              );
                              if (date != null) {
                                setState(() {
                                  _selectedDate = date;
                                });
                              }
                            },
                          ),
                        ),
                        Expanded(
                          child: CustomButton(
                            btnText: "날짜 범위 선택",
                            backgroundColor: Colors.green, // 예제용 색상 유지
                            onCallBack: () async {
                              final range = await CustomDatePicker.showRange(
                                context: context,
                                firstDate: DateTime(2000),
                                lastDate: DateTime(2100),
                                helpText: "날짜 범위를 선택하세요",
                              );
                              if (range != null) {
                                setState(() {
                                  _selectedDateRange = range;
                                });
                              }
                            },
                          ),
                        ),
                      ],
                    ),
                    if (_selectedDate != null)
                      CustomText(
                        "선택된 날짜: ${_selectedDate!.toString().split(' ')[0]}",
                        fontSize: 16,
                        color: p.primary,
                      ),
                    if (_selectedDateRange != null)
                      CustomText(
                        "선택된 범위: ${_selectedDateRange!.start.toString().split(' ')[0]} ~ ${_selectedDateRange!.end.toString().split(' ')[0]}",
                        fontSize: 16,
                        color: Colors.green, // 예제용 색상 유지
                      ),
                  ],
                ),
              ),

              // CupertinoDatePicker 섹션
              CustomCard(
                padding: const EdgeInsets.all(20),
                child: CustomColumn(
                  spacing: 16,
                  children: [
                    CustomText(
                      "🍎 CupertinoDatePicker 예시",
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                    CustomText(
                      "iOS 스타일 날짜 선택기",
                      fontSize: 14,
                      color: Colors.grey.shade600,
                    ),
                    CustomCupertinoDatePicker(
                      mode: CupertinoDatePickerMode.dateAndTime,
                      initialDateTime: _cupertinoDate,
                      minimumDate: DateTime(2000),
                      maximumDate: DateTime(2100),
                      use24HourFormat: false,
                      onDateTimeChanged: (DateTime dateTime) {
                        setState(() {
                          _cupertinoDate = dateTime;
                        });
                      },
                    ),
                    CustomText(
                      "선택된 날짜/시간: ${_cupertinoDate.toString().split('.')[0]}",
                      fontSize: 16,
                      color: p.primary,
                    ),
                    CustomRow(
                      spacing: 12,
                      children: [
                        Expanded(
                          child: CustomButton(
                            btnText: "날짜만",
                            backgroundColor: Colors.purple, // 예제용 색상 유지
                            onCallBack: () {
                              setState(() {
                                // 모드 변경은 위젯 재생성 필요
                              });
                            },
                          ),
                        ),
                        Expanded(
                          child: CustomButton(
                            btnText: "시간만",
                            backgroundColor: Colors.orange, // 예제용 색상 유지
                            onCallBack: () {
                              setState(() {
                                // 모드 변경은 위젯 재생성 필요
                              });
                            },
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),

              // PickerView 섹션
              CustomCard(
                padding: const EdgeInsets.all(20),
                child: CustomColumn(
                  spacing: 16,
                  children: [
                    CustomText(
                      "📋 PickerView 예시",
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                    CustomText(
                      "리스트에서 항목 선택",
                      fontSize: 14,
                      color: Colors.grey.shade600,
                    ),
                    // 단일 선택
                    CustomColumn(
                      spacing: 12,
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        CustomText(
                          "단일 선택",
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                        ),
                        Container(
                          height: 200,
                          decoration: BoxDecoration(
                            border: Border.all(color: Colors.grey.shade300),
                            borderRadius: BorderRadius.circular(8),
                          ),
                          child: CustomPickerView<String>(
                            items: _pickerItems,
                            selectedItem: _selectedPickerItem,
                            onItemSelected: (String item) {
                              setState(() {
                                _selectedPickerItem = item;
                              });
                            },
                            selectedItemColor: p.primary.withOpacity(0.1),
                            selectedItemStyle: TextStyle(
                              fontSize: 16,
                              fontWeight: FontWeight.bold,
                              color: p.primary,
                            ),
                          ),
                        ),
                        if (_selectedPickerItem != null)
                          CustomText(
                            "선택된 항목: $_selectedPickerItem",
                            fontSize: 16,
                            color: p.primary,
                          ),
                      ],
                    ),
                    const Divider(),
                    // 다중 선택
                    CustomColumn(
                      spacing: 12,
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        CustomText(
                          "다중 선택",
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                        ),
                        Container(
                          height: 200,
                          decoration: BoxDecoration(
                            border: Border.all(color: Colors.grey.shade300),
                            borderRadius: BorderRadius.circular(8),
                          ),
                          child: CustomPickerView<String>(
                            items: _pickerItems,
                            multiSelect: true,
                            selectedItems: _selectedMultiItems,
                            onItemSelected:
                                (_) {}, // 다중 선택 모드에서는 사용되지 않지만 필수 파라미터
                            onItemsSelected: (List<String> items) {
                              setState(() {
                                _selectedMultiItems = items;
                              });
                            },
                            selectedItemColor: Colors.green.withOpacity(0.1), // 예제용 색상 유지
                            selectedItemStyle: const TextStyle(
                              fontSize: 16,
                              fontWeight: FontWeight.bold,
                              color: Colors.green, // 예제용 색상 유지
                            ),
                          ),
                        ),
                        if (_selectedMultiItems.isNotEmpty)
                          CustomText(
                            "선택된 항목: ${_selectedMultiItems.join(', ')}",
                            fontSize: 16,
                            color: Colors.green, // 예제용 색상 유지
                          ),
                      ],
                    ),
                  ],
                ),
              ),

              // GridView 섹션
              CustomCard(
                padding: const EdgeInsets.all(20),
                child: CustomColumn(
                  spacing: 16,
                  children: [
                    CustomText(
                      "📊 GridView 예시",
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                    CustomText(
                      "그리드 레이아웃으로 아이템 표시",
                      fontSize: 14,
                      color: p.textSecondary,
                    ),
                    SizedBox(
                      height: 400,
                      child: CustomGridView(
                        itemCount: _gridItems.length,
                        crossAxisCount: 2,
                        spacing: 12,
                        padding: const EdgeInsets.all(8),
                        itemBuilder: (context, index) {
                          final item = _gridItems[index];
                          return CustomCard(
                            padding: const EdgeInsets.all(16),
                            borderRadius: 12,
                            child: CustomColumn(
                              spacing: 8,
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                Container(
                                  width: 60,
                                  height: 60,
                                  decoration: BoxDecoration(
                                    color: item['color'],
                                    shape: BoxShape.circle,
                                  ),
                                  child: Center(
                                    child: CustomText(
                                      '${item['id'] + 1}',
                                      fontSize: 24,
                                      fontWeight: FontWeight.bold,
                                      color: Colors.white,
                                    ),
                                  ),
                                ),
                                CustomText(
                                  item['title'],
                                  fontSize: 16,
                                  fontWeight: FontWeight.bold,
                                ),
                              ],
                            ),
                          );
                        },
                      ),
                    ),
                    const SizedBox(height: 12),
                    CustomText(
                      "3열 GridView 예시",
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                    ),
                    SizedBox(
                      height: 300,
                      child: CustomGridView(
                        itemCount: 12,
                        crossAxisCount: 3,
                        spacing: 8,
                        padding: const EdgeInsets.all(8),
                        itemBuilder: (context, index) {
                          return CustomCard(
                            padding: const EdgeInsets.all(12),
                            borderRadius: 8,
                            child: Center(
                              child: CustomText(
                                '${index + 1}',
                                fontSize: 20,
                                fontWeight: FontWeight.bold,
                              ),
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
