import 'package:flutter/material.dart';
import '../custom/widgets.dart';
import '../theme/app_colors.dart';

/// 네비게이션 위젯 사용 예제 페이지
/// CustomFloatingActionButton, CustomDrawer
class NavigationWidgetsPage extends StatefulWidget {
  const NavigationWidgetsPage({super.key});

  @override
  State<NavigationWidgetsPage> createState() => _NavigationWidgetsPageState();
}

class _NavigationWidgetsPageState extends State<NavigationWidgetsPage> {
  int _counter = 0;
  int _selectedDrawerIndex = 0;
  FloatingActionButtonType _currentFABType = FloatingActionButtonType.regular;

  @override
  Widget build(BuildContext context) {
    final p = context.palette;
    return Scaffold(
      backgroundColor: p.background,
      appBar: CustomAppBar(
        title: "네비게이션 위젯 예시",
        backgroundColor: Colors.indigo, // 예제용 색상 유지
        drawerIcon: Icons.menu, // Drawer 아이콘 커스텀 (기본값: Icons.menu)
        drawerIconColor: Colors.white, // Drawer 아이콘 색상
        drawerIconSize: 28.0, // Drawer 아이콘 크기
      ),
      drawer: CustomDrawer(
        header: DrawerHeader(
          decoration: BoxDecoration(color: Colors.indigo),
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
          child: CustomColumn(
            mainAxisAlignment: MainAxisAlignment.center,
            spacing: 4,
            children: [
              CircleAvatar(
                radius: 28,
                backgroundColor: Colors.white,
                child: Icon(Icons.person, size: 28, color: Colors.indigo),
              ),
              CustomText(
                "사용자 이름",
                fontSize: 16,
                fontWeight: FontWeight.bold,
                color: Colors.white,
              ),
              CustomText(
                "user@example.com",
                fontSize: 11,
                color: Colors.white70,
              ),
            ],
          ),
        ),
        items: [
          DrawerItem(
            label: "홈",
            icon: Icons.home,
            selected: _selectedDrawerIndex == 0,
            selectedColor: Colors.indigo.shade50,
            selectedTextColor: Colors.indigo,
            onTap: () {
              Navigator.popUntil(context, (route) => route.isFirst);
            },
          ),
          DrawerItem(
            label: "프로필",
            icon: Icons.person,
            selected: _selectedDrawerIndex == 1,
            selectedColor: Colors.indigo.shade50,
            selectedTextColor: Colors.indigo,
            onTap: () {
              setState(() {
                _selectedDrawerIndex = 1;
              });
              CustomSnackBar.show(context, message: "프로필 선택됨");
            },
          ),
          DrawerItem(
            label: "설정",
            icon: Icons.settings,
            selected: _selectedDrawerIndex == 2,
            selectedColor: Colors.indigo.shade50,
            selectedTextColor: Colors.indigo,
            onTap: () {
              setState(() {
                _selectedDrawerIndex = 2;
              });
              CustomSnackBar.show(context, message: "설정 선택됨");
            },
          ),
          DrawerItem(
            label: "도움말",
            icon: Icons.help,
            selected: _selectedDrawerIndex == 3,
            selectedColor: Colors.indigo.shade50,
            selectedTextColor: Colors.indigo,
            onTap: () {
              setState(() {
                _selectedDrawerIndex = 3;
              });
              CustomSnackBar.show(context, message: "도움말 선택됨");
            },
          ),
        ],
        footer: Container(
          padding: const EdgeInsets.all(16),
          child: CustomText("버전 1.0.0", fontSize: 12, color: p.textSecondary),
        ),
      ),
      body: SingleChildScrollView(
        child: CustomPadding.all(
          16.0,
          child: CustomColumn(
            spacing: 24,
            children: [
              CustomText(
                "네비게이션 위젯 종합 예시",
                fontSize: 24,
                fontWeight: FontWeight.bold,
                color: Colors.indigo, // 예제용 색상 유지
              ),

              // CustomFloatingActionButton 예시
              CustomColumn(
                spacing: 12,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  CustomText(
                    "CustomFloatingActionButton",
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                  ),
                  CustomText(
                    "이 페이지의 우측 하단에 FloatingActionButton이 표시됩니다.",
                    fontSize: 14,
                    color: p.textSecondary,
                  ),
                  CustomCard(
                    padding: const EdgeInsets.all(16),
                    child: CustomColumn(
                      spacing: 12,
                      children: [
                        CustomText(
                          "FAB 타입별 예시",
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                        ),
                        CustomText(
                          "아래 버튼을 클릭하면 화면 하단의 FAB가 해당 타입으로 변경됩니다.",
                          fontSize: 12,
                          color: p.textSecondary,
                        ),
                        CustomRow(
                          spacing: 8,
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Expanded(
                              child: CustomButton(
                                btnText: "일반 FAB",
                                backgroundColor:
                                    _currentFABType ==
                                        FloatingActionButtonType.regular
                                    ? Colors.indigo.shade700
                                    : Colors.indigo,
                                onCallBack: () {
                                  setState(() {
                                    _currentFABType =
                                        FloatingActionButtonType.regular;
                                  });
                                  CustomSnackBar.show(
                                    context,
                                    message: "일반 FAB로 변경되었습니다",
                                  );
                                },
                              ),
                            ),
                            Expanded(
                              child: CustomButton(
                                btnText: "작은 FAB",
                                backgroundColor:
                                    _currentFABType ==
                                        FloatingActionButtonType.small
                                    ? Colors.blue.shade700
                                    : Colors.blue,
                                onCallBack: () {
                                  setState(() {
                                    _currentFABType =
                                        FloatingActionButtonType.small;
                                  });
                                  CustomSnackBar.show(
                                    context,
                                    message: "작은 FAB로 변경되었습니다",
                                  );
                                },
                              ),
                            ),
                            Expanded(
                              child: CustomButton(
                                btnText: "확장형 FAB",
                                backgroundColor:
                                    _currentFABType ==
                                        FloatingActionButtonType.extended
                                    ? Colors.purple.shade700
                                    : Colors.purple,
                                onCallBack: () {
                                  setState(() {
                                    _currentFABType =
                                        FloatingActionButtonType.extended;
                                  });
                                  CustomSnackBar.show(
                                    context,
                                    message: "확장형 FAB로 변경되었습니다",
                                  );
                                },
                              ),
                            ),
                          ],
                        ),
                        CustomText(
                          "현재 타입: ${_getFABTypeName(_currentFABType)}",
                          fontSize: 14,
                          fontWeight: FontWeight.bold,
                          color: Colors.indigo, // 예제용 색상 유지
                        ),
                      ],
                    ),
                  ),
                ],
              ),

              // CustomDrawer 예시
              CustomColumn(
                spacing: 12,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  CustomText(
                    "CustomDrawer",
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                  ),
                  CustomText(
                    "이 페이지의 좌측 상단 메뉴 아이콘을 클릭하면 Drawer가 열립니다.",
                    fontSize: 14,
                    color: Colors.grey.shade700,
                  ),
                  CustomCard(
                    padding: const EdgeInsets.all(16),
                    child: CustomColumn(
                      spacing: 12,
                      children: [
                        CustomText(
                          "Drawer 기능",
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                        ),
                        CustomText(
                          "• 헤더: 사용자 정보 표시",
                          fontSize: 14,
                          color: Colors.grey.shade700,
                        ),
                        CustomText(
                          "• 메뉴 항목: 선택 상태 표시",
                          fontSize: 14,
                          color: Colors.grey.shade700,
                        ),
                        CustomText(
                          "• 푸터: 버전 정보 표시",
                          fontSize: 14,
                          color: Colors.grey.shade700,
                        ),
                        CustomText(
                          "현재 선택된 메뉴: ${_getSelectedMenuName()}",
                          fontSize: 14,
                          fontWeight: FontWeight.bold,
                          color: Colors.indigo,
                        ),
                        CustomText(
                          "참고: leading과 drawer를 함께 사용하려면, leading에 Drawer 아이콘을 포함해야 합니다.",
                          fontSize: 12,
                          color: Colors.orange.shade700,
                          fontWeight: FontWeight.bold,
                        ),
                      ],
                    ),
                  ),
                ],
              ),

              // 카운터 예시
              CustomCard(
                padding: const EdgeInsets.all(20),
                child: CustomColumn(
                  spacing: 8,
                  children: [
                    CustomText(
                      "FAB 클릭 횟수",
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                    ),
                    CustomText(
                      '$_counter',
                      fontSize: 32,
                      fontWeight: FontWeight.bold,
                      color: Colors.indigo, // 예제용 색상 유지
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
      floatingActionButton: _buildFAB(),
    );
  }

  String _getSelectedMenuName() {
    switch (_selectedDrawerIndex) {
      case 0:
        return "홈";
      case 1:
        return "프로필";
      case 2:
        return "설정";
      case 3:
        return "도움말";
      default:
        return "없음";
    }
  }

  Widget _buildFAB() {
    switch (_currentFABType) {
      case FloatingActionButtonType.regular:
        return CustomFloatingActionButton(
          onPressed: () {
            setState(() {
              _counter++;
            });
            CustomSnackBar.show(context, message: "일반 FAB 클릭됨: $_counter");
          },
          icon: Icons.add,
          tooltip: "추가 (일반 FAB)",
          backgroundColor: Colors.indigo,
          foregroundColor: Colors.white,
        );
      case FloatingActionButtonType.small:
        return CustomFloatingActionButton.small(
          onPressed: () {
            setState(() {
              _counter++;
            });
            CustomSnackBar.show(context, message: "작은 FAB 클릭됨: $_counter");
          },
          icon: Icons.add,
          tooltip: "추가 (작은 FAB)",
          backgroundColor: Colors.blue,
          foregroundColor: Colors.white,
        );
      case FloatingActionButtonType.extended:
        return CustomFloatingActionButton.extended(
          onPressed: () {
            setState(() {
              _counter++;
            });
            CustomSnackBar.show(context, message: "확장형 FAB 클릭됨: $_counter");
          },
          label: "추가하기",
          icon: Icons.add,
          tooltip: "추가 (확장형 FAB)",
          backgroundColor: Colors.purple,
          foregroundColor: Colors.white,
        );
    }
  }

  String _getFABTypeName(FloatingActionButtonType type) {
    switch (type) {
      case FloatingActionButtonType.regular:
        return "일반 FAB";
      case FloatingActionButtonType.small:
        return "작은 FAB";
      case FloatingActionButtonType.extended:
        return "확장형 FAB";
    }
  }
}
