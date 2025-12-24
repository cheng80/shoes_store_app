import 'package:flutter/material.dart';
import 'package:slide_to_act/slide_to_act.dart';
import 'package:shoes_store_app/config.dart' as config;
import 'package:shoes_store_app/theme/app_colors.dart';
import 'package:shoes_store_app/custom/custom_snack_bar.dart';
import 'package:shoes_store_app/custom/util/navigation/custom_navigation_util.dart';
import 'package:shoes_store_app/custom/custom_dialog.dart';
import 'package:shoes_store_app/view/cheng/storage/cart_storage.dart';

/// 결제 시트 내용 위젯
/// 
/// BottomSheet 내에서 표시되는 결제 확인 UI입니다.
/// 자치구 선택, 결제 수단, 총액 표시 및 결제 확정 기능을 제공합니다.
class PaymentSheetContent extends StatefulWidget {
  final String initialDistrict;
  final List<String> districts;
  final int totalPrice;
  final List<Map<String, dynamic>> cart;
  final Future<void> Function() onSavePurchase;
  final void Function() onClearCart;

  const PaymentSheetContent({
    super.key,
    required this.initialDistrict,
    required this.districts,
    required this.totalPrice,
    required this.cart,
    required this.onSavePurchase,
    required this.onClearCart,
  });

  @override
  State<PaymentSheetContent> createState() => _PaymentSheetContentState();
}

class _PaymentSheetContentState extends State<PaymentSheetContent> {
  late String _district;
  bool _confirmed = false;

  @override
  void initState() {
    super.initState();
    _district = widget.initialDistrict;
  }

  @override
  Widget build(BuildContext context) {
    final p = context.palette;
    
    return SafeArea(
      child: Container(
        padding: const EdgeInsets.fromLTRB(16, 14, 16, 18),
        decoration: BoxDecoration(
          color: p.cardBackground,
          borderRadius: const BorderRadius.vertical(top: Radius.circular(20)),
        ),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Container(
              width: 48,
              height: 5,
              decoration: BoxDecoration(
                color: p.divider,
                borderRadius: BorderRadius.circular(12),
              ),
            ),
            const SizedBox(height: 14),

            Row(
              children: [
                const Icon(Icons.payment),
                const SizedBox(width: 8),
                Text("결제 확인", style: config.rLabel.copyWith(color: p.textPrimary)),
                const Spacer(),
                IconButton(
                  onPressed: () => CustomNavigationUtil.back(context),
                  icon: const Icon(Icons.close),
                ),
              ],
            ),
            const SizedBox(height: 10),

            Align(
              alignment: Alignment.centerLeft,
              child: Text("수령 지점(자치구)", style: config.rLabel.copyWith(color: p.textPrimary)),
            ),
            const SizedBox(height: 8),

            Container(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
              decoration: BoxDecoration(
                border: Border.all(color: p.divider),
                borderRadius: BorderRadius.circular(14),
              ),
              child: DropdownButton<String>(
                value: _district,
                isExpanded: true,
                underline: const SizedBox.shrink(),
                style: config.rLabel.copyWith(color: p.textPrimary),
                items: widget.districts
                    .map((d) => DropdownMenuItem(
                          value: d,
                          child: Padding(
                            padding: const EdgeInsets.symmetric(vertical: 4),
                            child: Text(d, style: config.rLabel.copyWith(color: p.textPrimary)),
                          ),
                        ))
                    .toList(),
                onChanged: (v) {
                  if (v != null) {
                    setState(() {
                      _district = v;
                    });
                  }
                },
              ),
            ),

            const SizedBox(height: 14),

            Align(
              alignment: Alignment.centerLeft,
              child: Text("결제수단", style: config.rLabel.copyWith(color: p.textPrimary)),
            ),
            const SizedBox(height: 8),
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                border: Border.all(color: p.divider),
                borderRadius: BorderRadius.circular(14),
              ),
              child: Text("카드(더미)", style: config.rLabel.copyWith(color: p.textPrimary)),
            ),

            const SizedBox(height: 14),

            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                border: Border.all(color: p.divider),
                borderRadius: BorderRadius.circular(14),
              ),
              child: Row(
                children: [
                  Expanded(child: Text("총액", style: config.rLabel.copyWith(color: p.textPrimary))),
                  Text("${config.priceFormatter(widget.totalPrice)}원", style: config.rLabel.copyWith(color: p.textPrimary)),
                ],
              ),
            ),

            const SizedBox(height: 16),

            SlideAction(
              text: _confirmed ? "결제 처리중..." : "오른쪽으로 밀어서 결제 확정",
              textStyle: config.rLabel.copyWith(color: p.textPrimary),
              outerColor: p.divider,
              innerColor: p.cardBackground,
              sliderButtonIcon: Icon(
                Icons.double_arrow_rounded,
                color: p.primary,
              ),
              sliderButtonIconPadding: 12,
              borderRadius: 18,
              elevation: 0,
              onSubmit: !_confirmed ? () async {
                setState(() {
                  _confirmed = true;
                });

                try {
                  await widget.onSavePurchase();
                  widget.onClearCart();

                  if (!mounted) return;
                  CustomNavigationUtil.back(context);
                  CustomSnackBar.showSuccess(
                    context,
                    message: "수령지: $_district / 총액: ${config.priceFormatter(widget.totalPrice)}원",
                  );

                  if (!mounted) return;
                  CustomNavigationUtil.offAllNamed(context, '/searchview');
                } catch (e) {
                  if (!mounted) return;
                  setState(() {
                    _confirmed = false;
                  });

                  CustomNavigationUtil.back(context);
                  CustomDialog.show(
                    context,
                    title: '구매 실패',
                    message: e.toString().replaceFirst('Exception: ', ''),
                    type: DialogType.dual,
                    confirmText: '장바구니로 이동',
                    cancelText: '확인',
                    onConfirm: () {
                      CustomNavigationUtil.back(context);
                      for (final item in widget.cart) {
                        CartStorage.addToCart(item);
                      }
                      CustomNavigationUtil.toNamed(context, '/cart');
                    },
                  );
                }
              } : null,
              alignment: Alignment.center,
              height: 56,
            ),
          ],
        ),
      ),
    );
  }
}

