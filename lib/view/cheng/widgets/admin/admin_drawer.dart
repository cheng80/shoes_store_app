import 'package:flutter/material.dart';
import 'package:get/get.dart';

import 'package:shoes_store_app/view/cheng/custom/custom.dart';
import 'package:shoes_store_app/view/cheng/theme/app_colors.dart';
import 'package:shoes_store_app/view/cheng/storage/admin_storage.dart';
import 'package:shoes_store_app/view/cheng/test_navigation_page.dart';
import 'package:shoes_store_app/view/cheng/screens/auth/admin_login_view.dart';

/// 관리자 메뉴 타입 열거형
/// 관리자 화면에서 사용 가능한 메뉴 종류를 정의합니다.
enum AdminMenuType {
  /// 주문 관리 메뉴
  orderManagement, // 주문 관리
  /// 반품 관리 메뉴
  returnManagement, // 반품 관리
  // TODO: 다른 메뉴 타입 추가 가능
}

/// 관리자 드로워 메뉴 아이템 클래스
/// 드로워 메뉴에 표시될 각 메뉴 항목의 정보를 담는 클래스입니다.
class AdminDrawerMenuItem {
  /// 메뉴 항목의 라벨 텍스트
  final String label;
  /// 메뉴 항목의 아이콘
  final IconData icon;
  /// 메뉴 항목의 타입 (어떤 메뉴인지 식별)
  final AdminMenuType menuType;
  /// 메뉴 항목 클릭 시 실행될 콜백 함수
  final VoidCallback onTap;

  const AdminDrawerMenuItem({
    required this.label,
    required this.icon,
    required this.menuType,
    required this.onTap,
  });
}

/// 관리자 드로워 위젯
/// 
/// 사용 예시:
/// ```dart
/// drawer: AdminDrawer(
///   currentMenu: AdminMenuType.orderManagement,
///   userName: '홍길동',
///   onMenuTap: (menuType) {
///     switch (menuType) {
///       case AdminMenuType.orderManagement:
///         // 주문 관리 페이지로 이동
///         break;
///       case AdminMenuType.returnManagement:
///         Get.off(() => AdminReturnOrderView());
///         break;
///     }
///   },
///   onProfileEditTap: () {
///     // 개인정보 수정 페이지로 이동
///   },
/// ),
/// ```
class AdminDrawer extends StatelessWidget {
  /// 현재 선택된 메뉴 타입 (필수)
  final AdminMenuType currentMenu;

  /// 사용자 이름 (선택사항, null이면 기본값 사용)
  final String? userName;

  /// 사용자 역할 (선택사항, 기본값: '관리자')
  final String? userRole;

  /// 메뉴 아이템 리스트 (선택사항, 기본 메뉴 사용)
  final List<AdminDrawerMenuItem>? menuItems;

  /// 개인정보 수정 버튼 클릭 콜백 (선택사항)
  final VoidCallback? onProfileEditTap;

  const AdminDrawer({
    super.key,
    required this.currentMenu,
    this.userName,
    this.userRole,
    this.menuItems,
    this.onProfileEditTap,
  });

  @override
  Widget build(BuildContext context) {
    // 사용자 정보 설정 (파라미터로 전달된 값 우선, 없으면 기본값 사용)
    final String displayName = userName ?? '관리자';
    final String displayRole = userRole ?? '관리자';

    // 메뉴 아이템 생성 (파라미터로 전달된 메뉴 아이템이 있으면 사용, 없으면 기본 메뉴 사용)
    final List<AdminDrawerMenuItem> items = menuItems ?? _getDefaultMenuItems(context);

    return CustomDrawer(
      header: Container(
        width: double.infinity,
        decoration: BoxDecoration(color: context.palette.primary),
        padding: const EdgeInsets.all(16),
        child: CustomColumn(
          crossAxisAlignment: CrossAxisAlignment.start,
          mainAxisAlignment: MainAxisAlignment.end,
          spacing: 8,
          children: [
            CustomText(
              displayRole,
              fontSize: 16,
              fontWeight: FontWeight.normal,
              color: context.palette.textOnPrimary,
            ),
            CustomText(
              displayName,
              fontSize: 24,
              fontWeight: FontWeight.bold,
              color: context.palette.textOnPrimary,
            ),
          ],
        ),
      ),
      middleChildren: [const Divider(height: 1)],
      // 메뉴 아이템들을 DrawerItem으로 변환하여 표시
      items: items.map((item) {
        return DrawerItem(
          label: item.label,
          icon: item.icon,
          // 현재 선택된 메뉴인지 확인하여 선택 상태 표시
          selected: item.menuType == currentMenu,
          onTap: () {
            if (item.menuType == currentMenu) {
              // 현재 선택된 메뉴는 클릭해도 아무 동작 없이 드로워만 닫음
              Get.back();
            } else {
              // 다른 메뉴를 클릭하면 드로워를 닫고 해당 메뉴의 콜백 실행
              Get.back();
              item.onTap();
            }
          },
        );
      }).toList(),
      bottomChildren: [const Divider(height: 1)],
      footer: Padding(
        padding: const EdgeInsets.all(16),
        child: CustomColumn(
          spacing: 12,
          children: [
            CustomButton(
              btnText: '개인정보 수정',
              buttonType: ButtonType.outlined,
              onCallBack: () {
                Get.back();
                onProfileEditTap?.call();
              },
              minimumSize: const Size(double.infinity, 48),
            ),
            // 테스트 페이지로 이동 버튼
            CustomButton(
              btnText: '테스트 페이지로 이동',
              buttonType: ButtonType.outlined,
              onCallBack: () {
                Get.back();
                Get.to(() => const TestNavigationPage());
              },
              minimumSize: const Size(double.infinity, 48),
            ),
            // 로그아웃 버튼
            CustomButton(
              btnText: '로그아웃',
              buttonType: ButtonType.outlined,
              onCallBack: () {
                Get.back();
                // 로그아웃 확인 다이얼로그
                Get.dialog(
                  AlertDialog(
                    title: const Text('로그아웃'),
                    content: const Text('정말 로그아웃하시겠습니까?'),
                    actions: [
                      TextButton(
                        onPressed: () => Get.back(),
                        child: const Text('취소'),
                      ),
                      TextButton(
                        onPressed: () {
                          // 관리자 정보 삭제
                          AdminStorage.clearAdmin();
                          // 관리자 로그인 화면으로 이동 (모든 페이지 제거)
                          Get.offAll(() => const AdminLoginView());
                        },
                        child: const Text('로그아웃'),
                      ),
                    ],
                  ),
                );
              },
              minimumSize: const Size(double.infinity, 48),
            ),
          ],
        ),
      ),
    );
  }

  /// 기본 메뉴 아이템 생성 메서드
  /// 파라미터로 메뉴 아이템이 전달되지 않았을 때 사용되는 기본 메뉴를 생성합니다.
  /// 각 페이지에서 menuItems 파라미터로 커스텀 메뉴 아이템을 전달하는 것을 권장합니다.
  List<AdminDrawerMenuItem> _getDefaultMenuItems(BuildContext context) {
    return [
      AdminDrawerMenuItem(
        label: '주문 관리',
        icon: Icons.shopping_cart,
        menuType: AdminMenuType.orderManagement,
        onTap: () {
          // 기본 동작 없음 - 각 페이지에서 menuItems로 커스텀 정의 필요
        },
      ),
      AdminDrawerMenuItem(
        label: '반품 관리',
        icon: Icons.assignment_return,
        menuType: AdminMenuType.returnManagement,
        onTap: () {
          // 기본 동작 없음 - 각 페이지에서 menuItems로 커스텀 정의 필요
        },
      ),
      // TODO: 다른 메뉴 항목들 추가 가능
    ];
  }
}

