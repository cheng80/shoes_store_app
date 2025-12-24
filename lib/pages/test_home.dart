import 'dart:io';
import 'dart:typed_data';

import '../custom/custom.dart';
import '../theme/app_colors.dart';
import 'bottom_sheet_page.dart';
import 'dialog_page.dart';
import 'layout_widgets_page.dart';
import 'list_view_page.dart';
import 'navigation_widgets_page.dart';
import 'picker_grid_page.dart';
import 'snackbar_action_sheet_page.dart';
import 'tab_bar_page.dart';
import 'text_field_page.dart';
import 'util_page.dart';
import '../core_global_storage_example.dart';
import 'package:flutter/material.dart';

class TestHome extends StatefulWidget {
  final VoidCallback onToggleTheme;

  const TestHome({super.key, required this.onToggleTheme});

  @override
  State<TestHome> createState() => _TestHomeState();
}

class _TestHomeState extends State<TestHome> {
  //Property
  late bool _themeBool;
  late bool _switchValue;
  late bool? _checkboxValue;
  late String? _radioValue;
  late double _sliderValue;
  late double _rating;
  late TextEditingController _ratingCommentController;
  late String? _selectedDropdownValue;

  final List<String> _dropdownItems = ['선택 1', '선택 2', '선택 3', '선택 4'];

  @override
  void initState() {
    // TODO: implement initState
    super.initState();
    _themeBool = false;
    _switchValue = false;
    _checkboxValue = false;
    _radioValue = null;
    _sliderValue = 50.0;
    _rating = 0.0;
    _ratingCommentController = TextEditingController();
    _selectedDropdownValue = _radioValue;
  }

  @override
  void dispose() {
    _ratingCommentController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final p = context.palette;
    return Scaffold(
      backgroundColor: p.background,
      appBar: CustomAppBar(
        title: "커스텀 위젯",
        // backgroundColor와 foregroundColor를 지정하지 않으면 테마 색상 자동 적용
        actions: [
          Switch(
            value: _themeBool,
            onChanged: (value) {
              setState(() {
                _themeBool = value;
              });
              widget.onToggleTheme();
            },
          ),
        ],
      ),
      body: SingleChildScrollView(
        child: CustomPadding.all(
          16.0,
          child: CustomColumn(
            spacing: 24,
            children: [
              // 제목 섹션
              CustomColumn(
                spacing: 8,
                children: [
                  CustomText(
                    "커스텀 위젯 종합 예시",
                    fontSize: 28,
                    fontWeight: FontWeight.bold,
                    color: p.primary,
                  ),
                  CustomText(
                    "다양한 위젯들을 조합한 사용 예시입니다",
                    fontSize: 16,
                    color: p.textSecondary,
                  ),
                ],
              ),

              const SizedBox(height: 24),

              // 메뉴 버튼들
              CustomCard(
                padding: const EdgeInsets.all(20),
                child: CustomColumn(
                  spacing: 16,
                  children: [
                    CustomText(
                      "📱 전용 예시 페이지",
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                    CustomText(
                      "각 위젯의 상세한 사용법과 다양한 예시를 확인할 수 있습니다",
                      fontSize: 14,
                      color: p.textSecondary,
                    ),
                    CustomButton(
                      btnText: "TextField 예시",
                      // backgroundColor를 지정하지 않으면 테마 primary 색상 자동 적용
                      onCallBack: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (context) => const TextFieldPage(),
                          ),
                        );
                      },
                    ),
                    CustomButton(
                      btnText: "ListView 예시",
                      backgroundColor: Colors.purple,
                      onCallBack: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (context) => const ListViewPage(),
                          ),
                        );
                      },
                    ),
                    CustomButton(
                      btnText: "Dialog 예시",
                      backgroundColor: Colors.orange,
                      onCallBack: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (context) => const DialogPage(),
                          ),
                        );
                      },
                    ),
                    CustomButton(
                      btnText: "TabBar 예시",
                      backgroundColor: Colors.indigo,
                      onCallBack: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (context) => const TabBarPage(),
                          ),
                        );
                      },
                    ),
                    CustomButton(
                      btnText: "SnackBar & ActionSheet",
                      backgroundColor: Colors.purple,
                      onCallBack: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (context) =>
                                const SnackBarActionSheetPage(),
                          ),
                        );
                      },
                    ),
                    CustomButton(
                      btnText: "Picker & Grid 예시",
                      backgroundColor: Colors.indigo,
                      onCallBack: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (context) => const PickerGridPage(),
                          ),
                        );
                      },
                    ),
                    CustomButton(
                      btnText: "레이아웃 위젯 예시",
                      backgroundColor: Colors.teal,
                      onCallBack: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (context) => const LayoutWidgetsPage(),
                          ),
                        );
                      },
                    ),
                    CustomButton(
                      btnText: "BottomSheet 예시",
                      backgroundColor: Colors.purple,
                      onCallBack: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (context) => const BottomSheetPage(),
                          ),
                        );
                      },
                    ),
                    CustomButton(
                      btnText: "네비게이션 위젯 예시",
                      backgroundColor: Colors.indigo,
                      onCallBack: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (context) => const NavigationWidgetsPage(),
                          ),
                        );
                      },
                    ),
                  ],
                ),
              ),

              const SizedBox(height: 24),

              // 유틸리티 예제 섹션
              CustomCard(
                padding: const EdgeInsets.all(20),
                child: CustomColumn(
                  spacing: 16,
                  children: [
                    CustomText(
                      "🛠️ 유틸리티 클래스 예제",
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                    CustomText(
                      "구현된 유틸리티 클래스들의 사용 예제를 확인할 수 있습니다",
                      fontSize: 14,
                      color: p.textSecondary,
                    ),
                    CustomButton(
                      btnText: "유틸리티 예제 보기",
                      backgroundColor: Colors.teal,
                      onCallBack: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (context) => const UtilPage(),
                          ),
                        );
                      },
                    ),
                    CustomButton(
                      btnText: "GlobalStorage 예제",
                      backgroundColor: Colors.blue,
                      onCallBack: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (context) =>
                                const CoreGlobalStorageExamplePage(),
                          ),
                        );
                      },
                    ),
                  ],
                ),
              ),

              const SizedBox(height: 24),

              // 기본 위젯 예시 섹션
              CustomCard(
                padding: const EdgeInsets.all(20),
                child: CustomColumn(
                  spacing: 16,
                  children: [
                    CustomText(
                      "🔘 버튼 위젯 예시",
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                    CustomText(
                      "TextButton, ElevatedButton, OutlinedButton 타입을 지원합니다",
                      fontSize: 14,
                      color: p.textSecondary,
                    ),
                    CustomRow(
                      spacing: 8,
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Expanded(
                          child: CustomButton(
                            btnText: "TextButton",
                            onCallBack: () => print("TextButton 클릭"),
                          ),
                        ),
                        Expanded(
                          child: CustomButton(
                            btnText: "Elevated",
                            buttonType: ButtonType.elevated,
                            backgroundColor: Colors.green,
                            onCallBack: () => print("ElevatedButton 클릭"),
                          ),
                        ),
                        Expanded(
                          child: CustomButton(
                            btnText: "Outlined",
                            buttonType: ButtonType.outlined,
                            backgroundColor: Colors.red,
                            onCallBack: () => print("OutlinedButton 클릭"),
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 8),
                    CustomText(
                      "Widget 사용 예시",
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                      color: p.primary,
                    ),
                    CustomButton(
                      btnText: Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Icon(
                            Icons.check_circle,
                            color: Colors.white,
                            size: 20,
                          ),
                          const SizedBox(width: 8),
                          CustomText(
                            "아이콘 + 텍스트",
                            fontSize: 16,
                            color: Colors.white,
                          ),
                        ],
                      ),
                      backgroundColor: Colors.purple,
                      onCallBack: () => print("Widget 버튼 클릭"),
                    ),
                    const SizedBox(height: 16),
                    CustomText(
                      "DropdownButton 예시",
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                      color: p.primary,
                    ),
                    CustomDropdownButton<String>(
                      value: _selectedDropdownValue,
                      items: _dropdownItems,
                      hint: "항목을 선택하세요",
                      onChanged: (String? value) {
                        setState(() {
                          _selectedDropdownValue = value;
                        });
                      },
                      backgroundColor: Colors.white,
                      borderColor: Colors.grey.shade300,
                      borderRadius: 8,
                    ),
                    if (_selectedDropdownValue != null)
                      CustomText(
                        "선택된 값: $_selectedDropdownValue",
                        fontSize: 14,
                        color: p.primary,
                      ),
                    const SizedBox(height: 12),
                    CustomText(
                      "커스텀 스타일 DropdownButton",
                      fontSize: 14,
                      fontWeight: FontWeight.bold,
                    ),
                    CustomDropdownButton<String>(
                      value: _selectedDropdownValue,
                      items: _dropdownItems,
                      hint: "선택하세요",
                      onChanged: (String? value) {
                        setState(() {
                          _selectedDropdownValue = value;
                        });
                      },
                      backgroundColor: Colors.blue.shade50,
                      borderColor: Colors.blue,
                      borderWidth: 2,
                      borderRadius: 12,
                      textStyle: const TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                        color: Colors.blue,
                      ),
                      iconColor: Colors.blue,
                    ),
                  ],
                ),
              ),

              const SizedBox(height: 16),

              // 아이콘 버튼 예시
              CustomCard(
                padding: const EdgeInsets.all(20),
                child: CustomColumn(
                  spacing: 16,
                  children: [
                    CustomText(
                      "🎯 아이콘 버튼 예시",
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                    CustomText(
                      "배경색과 둥근 모서리를 적용한 아이콘 버튼들",
                      fontSize: 14,
                      color: p.textSecondary,
                    ),
                    CustomRow(
                      spacing: 12,
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        CustomIconButton(
                          icon: Icons.favorite,
                          iconColor: Colors.red,
                          backgroundColor: Colors.red.shade50,
                          borderRadius: 8,
                          onPressed: () => print("좋아요 클릭"),
                          tooltip: "좋아요",
                        ),
                        CustomIconButton(
                          icon: Icons.share,
                          iconColor: Colors.blue,
                          backgroundColor: Colors.blue.shade50,
                          borderRadius: 8,
                          onPressed: () => print("공유 클릭"),
                          tooltip: "공유",
                        ),
                        CustomIconButton(
                          icon: Icons.bookmark,
                          iconColor: Colors.amber,
                          backgroundColor: Colors.amber.shade50,
                          borderRadius: 8,
                          onPressed: () => print("북마크 클릭"),
                          tooltip: "북마크",
                        ),
                        CustomIconButton(
                          icon: Icons.delete,
                          iconColor: Colors.grey,
                          backgroundColor: Colors.grey.shade100,
                          borderRadius: 8,
                          onPressed: () => print("삭제 클릭"),
                          tooltip: "삭제",
                        ),
                      ],
                    ),
                  ],
                ),
              ),

              const SizedBox(height: 16),

              // 입력 위젯 예시 섹션
              CustomCard(
                padding: const EdgeInsets.all(20),
                child: CustomColumn(
                  spacing: 16,
                  children: [
                    CustomText(
                      "🎛️ 입력 위젯 예시",
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                    CustomText(
                      "Switch, Checkbox, Radio, Slider 위젯 사용 예시",
                      fontSize: 14,
                      color: p.textSecondary,
                    ),
                    // Switch 예시
                    CustomColumn(
                      spacing: 12,
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        CustomText(
                          "Switch",
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                        ),
                        CustomRow(
                          spacing: 12,
                          children: [
                            CustomSwitch(
                              value: _switchValue,
                              onChanged: (value) {
                                setState(() {
                                  _switchValue = value;
                                });
                              },
                              label: "알림 받기",
                            ),
                            CustomSwitch(
                              value: !_switchValue,
                              onChanged: (value) {
                                setState(() {
                                  _switchValue = !value;
                                });
                              },
                              activeColor: Colors.green,
                              label: "다크 모드",
                            ),
                          ],
                        ),
                      ],
                    ),
                    const Divider(),
                    // Checkbox 예시
                    CustomColumn(
                      spacing: 12,
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        CustomText(
                          "Checkbox",
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                        ),
                        CustomColumn(
                          spacing: 8,
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            CustomCheckbox(
                              value: _checkboxValue,
                              onChanged: (value) {
                                setState(() {
                                  _checkboxValue = value;
                                });
                              },
                              label: "이용약관 동의",
                            ),
                            CustomCheckbox(
                              value: _checkboxValue == true,
                              onChanged: (value) {
                                setState(() {
                                  _checkboxValue = value;
                                });
                              },
                              activeColor: Colors.purple,
                              label: "개인정보 처리방침 동의",
                            ),
                          ],
                        ),
                      ],
                    ),
                    const Divider(),
                    // Radio 예시
                    CustomColumn(
                      spacing: 12,
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        CustomText(
                          "Radio",
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                        ),
                        CustomColumn(
                          spacing: 8,
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            CustomRadio<String>(
                              value: "option1",
                              groupValue: _radioValue,
                              onChanged: (value) {
                                setState(() {
                                  _radioValue = value;
                                });
                              },
                              label: "옵션 1",
                            ),
                            CustomRadio<String>(
                              value: "option2",
                              groupValue: _radioValue,
                              onChanged: (value) {
                                setState(() {
                                  _radioValue = value;
                                });
                              },
                              activeColor: Colors.orange,
                              label: "옵션 2",
                            ),
                            CustomRadio<String>(
                              value: "option3",
                              groupValue: _radioValue,
                              onChanged: (value) {
                                setState(() {
                                  _radioValue = value;
                                });
                              },
                              activeColor: Colors.teal,
                              label: "옵션 3",
                            ),
                          ],
                        ),
                      ],
                    ),
                    const Divider(),
                    // Slider 예시
                    CustomColumn(
                      spacing: 12,
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        CustomText(
                          "Slider",
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                        ),
                        CustomSlider(
                          value: _sliderValue,
                          min: 0,
                          max: 100,
                          divisions: 10,
                          title: "볼륨 조절",
                          showValue: true,
                          activeColor: Colors.blue,
                          onChanged: (value) {
                            setState(() {
                              _sliderValue = value;
                            });
                          },
                        ),
                        const SizedBox(height: 8),
                        CustomSlider(
                          value: _sliderValue / 100,
                          min: 0,
                          max: 1,
                          title: "진행률",
                          showValue: true,
                          activeColor: Colors.green,
                          onChanged: (value) {
                            setState(() {
                              _sliderValue = value * 100;
                            });
                          },
                        ),
                      ],
                    ),
                    const Divider(),
                    // Rating 예시
                    CustomColumn(
                      spacing: 12,
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        CustomText(
                          "Rating",
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                        ),
                        CustomText(
                          "별을 클릭하여 점수를 선택할 수 있습니다",
                          fontSize: 14,
                          color: p.textSecondary,
                        ),
                        CustomRating(
                          rating: _rating,
                          onRatingChanged: (rating) {
                            setState(() {
                              _rating = rating;
                            });
                          },
                        ),
                        if (_rating > 0)
                          CustomText(
                            "선택된 점수: $_rating / 5",
                            fontSize: 14,
                            fontWeight: FontWeight.bold,
                            color: Colors.amber.shade700,
                          ),
                        const SizedBox(height: 8),
                        CustomText(
                          "커스터마이징 예시",
                          fontSize: 14,
                          fontWeight: FontWeight.bold,
                        ),
                        CustomRating(
                          rating: _rating,
                          onRatingChanged: (rating) {
                            setState(() {
                              _rating = rating;
                            });
                          },
                          starSize: 32.0,
                          filledColor: Colors.orange,
                          unfilledColor: Colors.grey.shade300,
                          starSpacing: 8.0,
                        ),
                        const SizedBox(height: 8),
                        CustomText(
                          "읽기 전용 모드",
                          fontSize: 14,
                          fontWeight: FontWeight.bold,
                        ),
                        CustomRating(
                          rating: 4.0,
                          readOnly: true,
                          starSize: 28.0,
                        ),
                        const SizedBox(height: 16),
                        CustomText(
                          "입력 예제 (TextField와 함께 사용)",
                          fontSize: 14,
                          fontWeight: FontWeight.bold,
                        ),
                        CustomCard(
                          padding: const EdgeInsets.all(16),
                          child: CustomColumn(
                            spacing: 12,
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              CustomText(
                                "리뷰 작성",
                                fontSize: 16,
                                fontWeight: FontWeight.bold,
                              ),
                              CustomText(
                                "별점을 선택해주세요",
                                fontSize: 14,
                                color: p.textSecondary,
                              ),
                              CustomRating(
                                rating: _rating,
                                onRatingChanged: (rating) {
                                  setState(() {
                                    _rating = rating;
                                  });
                                },
                                starSize: 28.0,
                              ),
                              if (_rating > 0)
                                CustomText(
                                  "선택된 점수: $_rating / 5",
                                  fontSize: 14,
                                  fontWeight: FontWeight.bold,
                                  color: Colors.amber.shade700,
                                ),
                              const SizedBox(height: 8),
                              CustomTextField(
                                controller: _ratingCommentController,
                                labelText: "리뷰 내용",
                                hintText: "리뷰를 작성해주세요",
                                maxLines: 3,
                                onChanged: (value) {
                                  // 리뷰 내용 변경 시 처리
                                },
                              ),
                              if (_rating > 0 &&
                                  _ratingCommentController.text.isNotEmpty)
                                CustomButton(
                                  btnText: "리뷰 제출",
                                  backgroundColor: Colors.green,
                                  onCallBack: () {
                                    // 리뷰 제출 로직
                                    print(
                                      "별점: $_rating, 리뷰: ${_ratingCommentController.text}",
                                    );
                                  },
                                ),
                            ],
                          ),
                        ),
                        const SizedBox(height: 16),
                        CustomText(
                          "다양한 아이콘 버전",
                          fontSize: 14,
                          fontWeight: FontWeight.bold,
                        ),
                        CustomText(
                          "별 이외의 아이콘도 사용할 수 있습니다",
                          fontSize: 12,
                          color: p.textSecondary,
                        ),
                        const SizedBox(height: 8),
                        CustomColumn(
                          spacing: 12,
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            CustomText(
                              "하트 아이콘",
                              fontSize: 12,
                              fontWeight: FontWeight.bold,
                            ),
                            CustomRating(
                              rating: _rating,
                              onRatingChanged: (rating) {
                                setState(() {
                                  _rating = rating;
                                });
                              },
                              filledIcon: Icons.favorite,
                              unfilledIcon: Icons.favorite_border,
                              filledColor: Colors.red,
                              unfilledColor: Colors.grey.shade300,
                              starSize: 28.0,
                            ),
                            CustomText(
                              "좋아요 아이콘",
                              fontSize: 12,
                              fontWeight: FontWeight.bold,
                            ),
                            CustomRating(
                              rating: _rating,
                              onRatingChanged: (rating) {
                                setState(() {
                                  _rating = rating;
                                });
                              },
                              filledIcon: Icons.thumb_up,
                              unfilledIcon: Icons.thumb_up_outlined,
                              filledColor: Colors.blue,
                              unfilledColor: Colors.grey.shade300,
                              starSize: 28.0,
                            ),
                            CustomText(
                              "다이아몬드 아이콘",
                              fontSize: 12,
                              fontWeight: FontWeight.bold,
                            ),
                            CustomRating(
                              rating: _rating,
                              onRatingChanged: (rating) {
                                setState(() {
                                  _rating = rating;
                                });
                              },
                              filledIcon: Icons.diamond,
                              unfilledIcon: Icons.diamond_outlined,
                              filledColor: Colors.cyan,
                              unfilledColor: Colors.grey.shade300,
                              starSize: 28.0,
                            ),
                            CustomText(
                              "불꽃 아이콘 (읽기 전용)",
                              fontSize: 12,
                              fontWeight: FontWeight.bold,
                            ),
                            CustomRating(
                              rating: 4.0,
                              readOnly: true,
                              filledIcon: Icons.local_fire_department,
                              unfilledIcon:
                                  Icons.local_fire_department_outlined,
                              filledColor: Colors.orange,
                              unfilledColor: Colors.grey.shade300,
                              starSize: 28.0,
                            ),
                          ],
                        ),
                      ],
                    ),
                  ],
                ),
              ),

              const SizedBox(height: 16),

              // 이미지 갤러리 섹션
              CustomCard(
                padding: const EdgeInsets.all(20),
                child: CustomColumn(
                  spacing: 16,
                  children: [
                    CustomText(
                      "🖼️ 이미지 갤러리 예시",
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                    CustomText(
                      "CustomImage 위젯을 사용한 이미지 표시 예시",
                      fontSize: 14,
                      color: p.textSecondary,
                    ),
                    // 첫 번째 행: 3개 이미지
                    CustomRow(
                      spacing: 8,
                      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                      children: [
                        Expanded(
                          child: _buildImageCard(
                            "images/bee.png",
                            "벌",
                            context,
                          ),
                        ),
                        Expanded(
                          child: _buildImageCard(
                            "images/cat.png",
                            "고양이",
                            context,
                          ),
                        ),
                        Expanded(
                          child: _buildImageCard(
                            "images/cow.png",
                            "소",
                            context,
                          ),
                        ),
                      ],
                    ),
                    // 두 번째 행: 3개 이미지
                    CustomRow(
                      spacing: 8,
                      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                      children: [
                        Expanded(
                          child: _buildImageCard(
                            "images/dog.png",
                            "강아지",
                            context,
                          ),
                        ),
                        Expanded(
                          child: _buildImageCard(
                            "images/fox.png",
                            "여우",
                            context,
                          ),
                        ),
                        Expanded(
                          child: _buildImageCard(
                            "images/monkey.png",
                            "원숭이",
                            context,
                          ),
                        ),
                      ],
                    ),
                    // 세 번째 행: 2개 이미지
                    CustomRow(
                      spacing: 8,
                      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                      children: [
                        Expanded(
                          child: _buildImageCard(
                            "images/pig.png",
                            "돼지",
                            context,
                          ),
                        ),
                        Expanded(
                          child: _buildImageCard(
                            "images/wolf.png",
                            "늑대",
                            context,
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),

              const SizedBox(height: 16),

              // File 이미지 예시 섹션
              CustomCard(
                padding: const EdgeInsets.all(20),
                child: CustomColumn(
                  spacing: 16,
                  children: [
                    CustomText(
                      "📁 File 이미지 예시",
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                    CustomText(
                      "CustomImage.file()을 사용한 파일 이미지 표시 예시",
                      fontSize: 14,
                      color: p.textSecondary,
                    ),
                    CustomText(
                      "File 이미지는 디바이스의 파일 시스템에서 이미지를 로드합니다.",
                      fontSize: 12,
                      color: p.textSecondary,
                    ),
                    const SizedBox(height: 8),
                    // File 이미지 예시
                    CustomRow(
                      spacing: 12,
                      children: [
                        Expanded(
                          child: _buildFileImageExample(
                            "bee.png",
                            "예시 1: File 이미지",
                            "CustomImage.file() 사용",
                            context,
                          ),
                        ),
                        Expanded(
                          child: _buildFileImageExample(
                            "cat.png",
                            "예시 2: 크기 지정",
                            "width, height 지정",
                            context,
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 8),
                    CustomContainer(
                      padding: const EdgeInsets.all(12),
                      backgroundColor: Colors.blue.shade50,
                      borderRadius: 8,
                      child: CustomColumn(
                        spacing: 8,
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          CustomText(
                            "💡 사용 방법",
                            fontSize: 14,
                            fontWeight: FontWeight.bold,
                            color: Colors.blue.shade900,
                          ),
                          CustomText(
                            "// File 이미지 사용\n"
                            "final imageFile = File('images/bee.png');\n"
                            "CustomImage.file(imageFile)\n\n"
                            "// 크기 지정\n"
                            "CustomImage.file(\n"
                            "  File('images/cat.png'),\n"
                            "  width: 100,\n"
                            "  height: 100,\n"
                            "  fit: BoxFit.cover,\n"
                            ")",
                            fontSize: 12,
                            color: Colors.blue.shade800,
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),

              const SizedBox(height: 16),

              // Memory 이미지 예시 섹션
              CustomCard(
                padding: const EdgeInsets.all(20),
                child: CustomColumn(
                  spacing: 16,
                  children: [
                    CustomText(
                      "💾 Memory 이미지 예시",
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                    CustomText(
                      "CustomImage.memory()을 사용한 메모리 이미지 표시 예시",
                      fontSize: 14,
                      color: p.textSecondary,
                    ),
                    CustomText(
                      "Memory 이미지는 바이트 데이터(Uint8List)로부터 이미지를 로드합니다.",
                      fontSize: 12,
                      color: p.textSecondary,
                    ),
                    const SizedBox(height: 8),
                    // Memory 이미지 예시
                    FutureBuilder<Uint8List?>(
                      future: _loadImageAsBytes("images/cow.png"),
                      builder: (context, snapshot) {
                        if (snapshot.connectionState ==
                            ConnectionState.waiting) {
                          return const Center(
                            child: CircularProgressIndicator(),
                          );
                        }
                        if (snapshot.hasData && snapshot.data != null) {
                          return CustomRow(
                            spacing: 12,
                            children: [
                              Expanded(
                                child: _buildMemoryImageExample(
                                  snapshot.data!,
                                  "예시 1: Memory 이미지",
                                  "CustomImage.memory() 사용",
                                  context,
                                ),
                              ),
                              Expanded(
                                child: _buildMemoryImageExample(
                                  snapshot.data!,
                                  "예시 2: 크기 지정",
                                  "width, height 지정",
                                  context,
                                ),
                              ),
                            ],
                          );
                        }
                        final p = context.palette;
                        return CustomText(
                          "이미지를 로드할 수 없습니다",
                          fontSize: 12,
                          color: p.textSecondary,
                        );
                      },
                    ),
                    const SizedBox(height: 8),
                    CustomContainer(
                      padding: const EdgeInsets.all(12),
                      backgroundColor: Colors.purple.shade50,
                      borderRadius: 8,
                      child: CustomColumn(
                        spacing: 8,
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          CustomText(
                            "💡 사용 방법",
                            fontSize: 14,
                            fontWeight: FontWeight.bold,
                            color: Colors.purple.shade900,
                          ),
                          CustomText(
                            "// Memory 이미지 사용\n"
                            "CustomImage.memory(imageBytes)\n\n"
                            "// 크기 지정\n"
                            "CustomImage.memory(\n"
                            "  imageBytes,\n"
                            "  width: 100,\n"
                            "  height: 100,\n"
                            "  fit: BoxFit.cover,\n"
                            ")",
                            fontSize: 12,
                            color: Colors.purple.shade800,
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),

              const SizedBox(height: 16),

              // 복합 레이아웃 예시
              CustomCard(
                padding: const EdgeInsets.all(20),
                child: CustomColumn(
                  spacing: 16,
                  children: [
                    CustomText(
                      "🎨 복합 레이아웃 예시",
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                    CustomText(
                      "여러 위젯을 조합한 실제 사용 예시",
                      fontSize: 14,
                      color: p.textSecondary,
                    ),
                    CustomContainer(
                      padding: const EdgeInsets.all(16),
                      backgroundColor: Colors.blue.shade50,
                      borderRadius: 12,
                      borderColor: Colors.blue.shade200,
                      borderWidth: 1,
                      child: CustomColumn(
                        spacing: 12,
                        children: [
                          CustomRow(
                            spacing: 12,
                            children: [
                              ClipRRect(
                                borderRadius: BorderRadius.circular(8),
                                child: CustomImage(
                                  "images/cat.png",
                                  width: 80,
                                  height: 80,
                                  fit: BoxFit.cover,
                                ),
                              ),
                              Expanded(
                                child: CustomColumn(
                                  spacing: 4,
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    CustomText(
                                      "고양이",
                                      fontSize: 18,
                                      fontWeight: FontWeight.bold,
                                    ),
                                    CustomText(
                                      "귀여운 고양이입니다",
                                      fontSize: 14,
                                      color: p.textSecondary,
                                    ),
                                    CustomRow(
                                      spacing: 8,
                                      children: [
                                        CustomIconButton(
                                          icon: Icons.favorite_border,
                                          iconColor: Colors.red,
                                          iconSize: 20,
                                          size: 36,
                                          onPressed: () => print("좋아요"),
                                        ),
                                        CustomIconButton(
                                          icon: Icons.comment,
                                          iconColor: Colors.blue,
                                          iconSize: 20,
                                          size: 36,
                                          onPressed: () => print("댓글"),
                                        ),
                                      ],
                                    ),
                                  ],
                                ),
                              ),
                            ],
                          ),
                          CustomButton(
                            btnText: "더보기",
                            backgroundColor: Colors.blue,
                            onCallBack: () => print("더보기 클릭"),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),

              const SizedBox(height: 16),

              // 카드 형태 레이아웃
              CustomCard(
                padding: const EdgeInsets.all(20),
                child: CustomColumn(
                  spacing: 16,
                  children: [
                    CustomText(
                      "📋 카드 레이아웃 예시",
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                    CustomText(
                      "CustomCard를 사용한 정보 카드 예시",
                      fontSize: 14,
                      color: p.textSecondary,
                    ),
                    _buildAnimalCard(
                      "images/dog.png",
                      "강아지",
                      "충실한 반려동물",
                      context,
                    ),
                    const SizedBox(height: 12),
                    _buildAnimalCard("images/fox.png", "여우", "영리한 동물", context),
                  ],
                ),
              ),

              const SizedBox(height: 16),

              // CustomCard vs CustomContainer 비교 예시
              CustomCard(
                padding: const EdgeInsets.all(20),
                child: CustomColumn(
                  spacing: 16,
                  children: [
                    CustomText(
                      "⚖️ Card vs Container 비교",
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                    CustomText(
                      "두 위젯의 차이점과 사용 시나리오",
                      fontSize: 14,
                      color: p.textSecondary,
                    ),
                    CustomRow(
                      spacing: 12,
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        // CustomCard 예시 (Material Design Card 기반)
                        Expanded(
                          child: CustomCard(
                            padding: const EdgeInsets.all(16),
                            child: CustomColumn(
                              spacing: 8,
                              children: [
                                CustomText(
                                  "CustomCard",
                                  fontSize: 16,
                                  fontWeight: FontWeight.bold,
                                ),
                                CustomText(
                                  "Material Design Card 기반\n기본 elevation 적용",
                                  fontSize: 12,
                                  fontWeight: FontWeight.normal,
                                  color: Colors.grey.shade700,
                                ),
                              ],
                            ),
                          ),
                        ),
                        // CustomContainer 예시 (Container 기반)
                        Expanded(
                          child: CustomContainer(
                            padding: const EdgeInsets.all(16),
                            backgroundColor: Colors.blue.shade50,
                            borderRadius: 12,
                            borderColor: Colors.blue,
                            borderWidth: 2,
                            shadowColor: Colors.blue.withValues(alpha: 0.3),
                            blurRadius: 8,
                            child: CustomColumn(
                              spacing: 8,
                              children: [
                                CustomText(
                                  "CustomContainer",
                                  fontSize: 16,
                                  fontWeight: FontWeight.bold,
                                ),
                                CustomText(
                                  "Container 기반\n더 유연한 커스터마이징",
                                  fontSize: 12,
                                  fontWeight: FontWeight.normal,
                                  color: p.textSecondary,
                                ),
                              ],
                            ),
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),

              const SizedBox(height: 20),
            ],
          ),
        ),
      ),
    );
  }

  //--------Functions ------------

  /// 이미지 카드를 생성하는 헬퍼 메서드
  Widget _buildImageCard(String imagePath, String label, BuildContext context) {
    final p = context.palette;
    return CustomColumn(
      spacing: 8,
      children: [
        AspectRatio(
          aspectRatio: 1.0,
          child: CustomCard(
            padding: EdgeInsets.zero,
            borderRadius: 12,
            child: ClipRRect(
              borderRadius: BorderRadius.circular(12),
              child: CustomImage(imagePath, fit: BoxFit.cover),
            ),
          ),
        ),
        CustomText(
          label,
          fontSize: 14,
          fontWeight: FontWeight.w500,
          textAlign: TextAlign.center,
          color: p.textPrimary,
        ),
      ],
    );
  }

  /// 이미지를 바이트 데이터로 로드하는 헬퍼 메서드
  Future<Uint8List?> _loadImageAsBytes(String imagePath) async {
    try {
      final projectRoot = Directory.current.path;
      final imageFile = File('$projectRoot/$imagePath');
      if (await imageFile.exists()) {
        return await imageFile.readAsBytes();
      }
    } catch (e) {
      // 에러 발생 시 null 반환
    }
    return null;
  }

  /// Memory 이미지 예시를 생성하는 헬퍼 메서드
  Widget _buildMemoryImageExample(
    Uint8List imageBytes,
    String title,
    String description,
    BuildContext context,
  ) {
    final p = context.palette;
    return CustomColumn(
      spacing: 8,
      children: [
        AspectRatio(
          aspectRatio: 1.0,
          child: CustomCard(
            padding: EdgeInsets.zero,
            borderRadius: 12,
            child: ClipRRect(
              borderRadius: BorderRadius.circular(12),
              child: CustomImage.memory(
                imageBytes,
                fit: BoxFit.cover,
                errorWidget: Container(
                  color: Colors.grey.shade200,
                  child: CustomColumn(
                    mainAxisAlignment: MainAxisAlignment.center,
                    spacing: 8,
                    children: [
                      Icon(
                        Icons.broken_image,
                        size: 40,
                        color: Colors.grey.shade400,
                      ),
                      CustomText(
                        "이미지를 표시할 수 없습니다",
                        fontSize: 12,
                        color: p.textSecondary,
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ),
        ),
        CustomColumn(
          spacing: 4,
          children: [
            CustomText(
              title,
              fontSize: 12,
              fontWeight: FontWeight.w600,
              textAlign: TextAlign.center,
            ),
            CustomText(
              description,
              fontSize: 10,
              color: Colors.grey.shade600,
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ],
    );
  }

  /// File 이미지 예시를 생성하는 헬퍼 메서드
  Widget _buildFileImageExample(
    String imageFileName,
    String title,
    String description,
    BuildContext context,
  ) {
    final p = context.palette;
    // 프로젝트 루트의 images 폴더 경로 사용
    final projectRoot = Directory.current.path;
    final imageFile = File('$projectRoot/images/$imageFileName');

    return CustomColumn(
      spacing: 8,
      children: [
        AspectRatio(
          aspectRatio: 1.0,
          child: CustomCard(
            padding: EdgeInsets.zero,
            borderRadius: 12,
            child: ClipRRect(
              borderRadius: BorderRadius.circular(12),
              child: CustomImage.file(
                imageFile,
                fit: BoxFit.cover,
                errorWidget: Container(
                  color: Colors.grey.shade200,
                  child: CustomColumn(
                    mainAxisAlignment: MainAxisAlignment.center,
                    spacing: 8,
                    children: [
                      Icon(
                        Icons.broken_image,
                        size: 40,
                        color: Colors.grey.shade400,
                      ),
                      CustomText(
                        "이미지를 찾을 수 없습니다",
                        fontSize: 12,
                        color: p.textSecondary,
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ),
        ),
        CustomColumn(
          spacing: 4,
          children: [
            CustomText(
              title,
              fontSize: 12,
              fontWeight: FontWeight.w600,
              textAlign: TextAlign.center,
            ),
            CustomText(
              description,
              fontSize: 10,
              color: Colors.grey.shade600,
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ],
    );
  }

  /// 동물 카드를 생성하는 헬퍼 메서드
  Widget _buildAnimalCard(
    String imagePath,
    String title,
    String description,
    BuildContext context,
  ) {
    final p = context.palette;
    return CustomCard(
      borderRadius: 16,
      padding: const EdgeInsets.all(16),
      child: CustomColumn(
        spacing: 12,
        children: [
          CustomRow(
            spacing: 12,
            children: [
              ClipRRect(
                borderRadius: BorderRadius.circular(12),
                child: CustomImage(
                  imagePath,
                  width: 100,
                  height: 100,
                  fit: BoxFit.cover,
                ),
              ),
              CustomColumn(
                spacing: 8,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  CustomText(
                    title,
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                    color: p.textPrimary,
                  ),
                  CustomText(description, fontSize: 14, color: p.textSecondary),
                ],
              ),
            ],
          ),
          CustomRow(
            spacing: 8,
            mainAxisAlignment: MainAxisAlignment.end,
            children: [
              CustomIconButton(
                icon: Icons.favorite,
                iconColor: Colors.red,
                backgroundColor: Colors.red.shade50,
                borderRadius: 8,
                onPressed: () => print("$title 좋아요"),
              ),
              CustomIconButton(
                icon: Icons.share,
                iconColor: Colors.blue,
                backgroundColor: Colors.blue.shade50,
                borderRadius: 8,
                onPressed: () => print("$title 공유"),
              ),
              CustomButton(
                btnText: "상세보기",
                backgroundColor: Colors.blue,
                minimumSize: const Size(100, 40),
                onCallBack: () => print("$title 상세보기"),
              ),
            ],
          ),
        ],
      ),
    );
  }

  //------------------------------
}
