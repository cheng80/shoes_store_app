import 'package:flutter/material.dart';

import 'package:shoes_store_app/custom/custom.dart';
import 'package:shoes_store_app/custom/custom_dialog.dart';
import 'package:shoes_store_app/custom/util/navigation/custom_navigation_util.dart';
import 'package:shoes_store_app/theme/app_colors.dart';
import 'package:shoes_store_app/view/cheng/storage/admin_storage.dart';
import 'package:shoes_store_app/view/cheng/test_navigation_page.dart';
import 'package:shoes_store_app/view/cheng/screens/auth/admin_login_view.dart';

/// 관리자 메뉴 타입 열거형
enum AdminMenuType {
  orderManagement,
  returnManagement,
}

/// 관리자 드로워 메뉴 아이템 클래스
class AdminDrawerMenuItem {
  final String label;
  final IconData icon;
  final AdminMenuType menuType;
  final VoidCallback onTap;

  const AdminDrawerMenuItem({
    required this.label,
    required this.icon,
    required this.menuType,
    required this.onTap,
  });
}

/// 관리자 드로워 위젯
class AdminDrawer extends StatelessWidget {
  final AdminMenuType currentMenu;
  final String? userName;
  final String? userRole;
  final List<AdminDrawerMenuItem>? menuItems;
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
    final String displayName = userName ?? '관리자';
    final String displayRole = userRole ?? '관리자';
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
      items: items.map((item) {
        return DrawerItem(
          label: item.label,
          icon: item.icon,
          selected: item.menuType == currentMenu,
          onTap: () {
            CustomNavigationUtil.back(context);
            if (item.menuType != currentMenu) {
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
                CustomNavigationUtil.back(context);
                onProfileEditTap?.call();
              },
              minimumSize: const Size(double.infinity, 48),
            ),
            CustomButton(
              btnText: '테스트 페이지로 이동',
              buttonType: ButtonType.outlined,
              onCallBack: () {
                CustomNavigationUtil.back(context);
                CustomNavigationUtil.to(context, const TestNavigationPage());
              },
              minimumSize: const Size(double.infinity, 48),
            ),
            CustomButton(
              btnText: '로그아웃',
              buttonType: ButtonType.outlined,
              onCallBack: () {
                CustomNavigationUtil.back(context);
                CustomDialog.show(
                  context,
                  title: '로그아웃',
                  message: '정말 로그아웃하시겠습니까?',
                  type: DialogType.dual,
                  confirmText: '로그아웃',
                  cancelText: '취소',
                  onConfirm: () {
                    AdminStorage.clearAdmin();
                    CustomNavigationUtil.offAll(context, const AdminLoginView());
                  },
                );
              },
              minimumSize: const Size(double.infinity, 48),
            ),
          ],
        ),
      ),
    );
  }

  List<AdminDrawerMenuItem> _getDefaultMenuItems(BuildContext context) {
    return [
      AdminDrawerMenuItem(
        label: '주문 관리',
        icon: Icons.shopping_cart,
        menuType: AdminMenuType.orderManagement,
        onTap: () {},
      ),
      AdminDrawerMenuItem(
        label: '반품 관리',
        icon: Icons.assignment_return,
        menuType: AdminMenuType.returnManagement,
        onTap: () {},
      ),
    ];
  }
}

