import 'package:flutter/material.dart';

import '../custom/widgets.dart';
import '../theme/app_colors.dart';

/// Dialog 사용 예제 페이지
class DialogPage extends StatefulWidget {
  const DialogPage({super.key});

  @override
  State<DialogPage> createState() => _DialogPageState();
}

class _DialogPageState extends State<DialogPage> {
  int _counter = 0;

  @override
  Widget build(BuildContext context) {
    final p = context.palette;
    return Scaffold(
      backgroundColor: p.background,
      appBar: CustomAppBar(title: "Dialog 예시", backgroundColor: Colors.orange), // 예제용 색상 유지
      body: SingleChildScrollView(
        child: CustomPadding.all(
          16.0,
          child: CustomColumn(
            spacing: 24,
            children: [
              CustomText(
                "다이얼로그 종합 예시",
                fontSize: 24,
                fontWeight: FontWeight.bold,
                color: Colors.orange, // 예제용 색상 유지
              ),

              // 단일 버튼 다이얼로그
              CustomColumn(
                spacing: 12,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  CustomText(
                    "단일 버튼 다이얼로그",
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                  ),
                  SizedBox(
                    width: double.infinity,
                    child: CustomButton(
                      btnText: "알림 다이얼로그",
                      // backgroundColor를 지정하지 않으면 테마 primary 색상 자동 적용
                      onCallBack: () {
                        CustomDialog.show(
                          context,
                          title: "알림",
                          message: "단일 버튼 다이얼로그입니다.",
                          type: DialogType.single,
                        );
                      },
                    ),
                  ),
                  SizedBox(
                    width: double.infinity,
                    child: CustomButton(
                      btnText: "성공 메시지",
                      backgroundColor: Colors.green, // 예제용 색상 유지
                      onCallBack: () {
                        CustomDialog.show(
                          context,
                          title: "성공",
                          message: "작업이 성공적으로 완료되었습니다.",
                          type: DialogType.single,
                          confirmText: "확인",
                        );
                      },
                    ),
                  ),
                  SizedBox(
                    width: double.infinity,
                    child: CustomButton(
                      btnText: "경고 메시지",
                      backgroundColor: Colors.orange, // 예제용 색상 유지
                      onCallBack: () {
                        CustomDialog.show(
                          context,
                          title: "경고",
                          message: "주의가 필요한 상황입니다.",
                          type: DialogType.single,
                          confirmText: "알겠습니다",
                        );
                      },
                    ),
                  ),
                ],
              ),

              // 이중 버튼 다이얼로그
              CustomColumn(
                spacing: 12,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  CustomText(
                    "이중 버튼 다이얼로그",
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                  ),
                  SizedBox(
                    width: double.infinity,
                    child: CustomButton(
                      btnText: "확인 다이얼로그",
                      backgroundColor: Colors.teal, // 예제용 색상 유지
                      onCallBack: () {
                        CustomDialog.show(
                          context,
                          title: "확인",
                          message: "진행하시겠습니까?",
                          type: DialogType.dual,
                          onConfirm: () {
                            setState(() {
                              _counter++;
                            });
                          },
                          onCancel: () {
                            print("취소됨");
                          },
                        );
                      },
                    ),
                  ),
                  SizedBox(
                    width: double.infinity,
                    child: CustomButton(
                      btnText: "삭제 확인",
                      backgroundColor: Colors.red, // 예제용 색상 유지
                      onCallBack: () {
                        CustomDialog.show(
                          context,
                          title: "삭제 확인",
                          message: "정말로 삭제하시겠습니까?\n이 작업은 되돌릴 수 없습니다.",
                          type: DialogType.dual,
                          confirmText: "삭제",
                          cancelText: "취소",
                          onConfirm: () {
                            CustomDialog.show(
                              context,
                              title: "완료",
                              message: "삭제되었습니다.",
                              type: DialogType.single,
                            );
                          },
                        );
                      },
                    ),
                  ),
                ],
              ),

              // 버튼 정렬 예시
              CustomColumn(
                spacing: 12,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  CustomText(
                    "버튼 정렬 예시",
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                  ),
                  SizedBox(
                    width: double.infinity,
                    child: CustomButton(
                      btnText: "가운데 정렬 (기본값)",
                      backgroundColor: Colors.purple, // 예제용 색상 유지
                      onCallBack: () {
                        CustomDialog.show(
                          context,
                          title: "정렬 예시",
                          message: "버튼이 가운데 정렬됩니다.",
                          type: DialogType.dual,
                          actionsAlignment: MainAxisAlignment.center,
                        );
                      },
                    ),
                  ),
                  SizedBox(
                    width: double.infinity,
                    child: CustomButton(
                      btnText: "왼쪽 정렬",
                      backgroundColor: Colors.indigo, // 예제용 색상 유지
                      onCallBack: () {
                        CustomDialog.show(
                          context,
                          title: "정렬 예시",
                          message: "버튼이 왼쪽 정렬됩니다.",
                          type: DialogType.dual,
                          actionsAlignment: MainAxisAlignment.start,
                        );
                      },
                    ),
                  ),
                  SizedBox(
                    width: double.infinity,
                    child: CustomButton(
                      btnText: "오른쪽 정렬",
                      backgroundColor: Colors.deepPurple, // 예제용 색상 유지
                      onCallBack: () {
                        CustomDialog.show(
                          context,
                          title: "정렬 예시",
                          message: "버튼이 오른쪽 정렬됩니다.",
                          type: DialogType.dual,
                          actionsAlignment: MainAxisAlignment.end,
                        );
                      },
                    ),
                  ),
                  SizedBox(
                    width: double.infinity,
                    child: CustomButton(
                      btnText: "양쪽 정렬",
                      backgroundColor: Colors.purple.shade700, // 예제용 색상 유지
                      onCallBack: () {
                        CustomDialog.show(
                          context,
                          title: "정렬 예시",
                          message: "버튼이 양쪽에 정렬됩니다.",
                          type: DialogType.dual,
                          actionsAlignment: MainAxisAlignment.spaceBetween,
                        );
                      },
                    ),
                  ),
                ],
              ),

              // Widget 사용 예시
              CustomColumn(
                spacing: 12,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  CustomText(
                    "Widget 사용 예시",
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                  ),
                  SizedBox(
                    width: double.infinity,
                    child: CustomButton(
                      btnText: "Widget 다이얼로그",
                      backgroundColor: Colors.deepPurple, // 예제용 색상 유지
                      onCallBack: () {
                        final p = context.palette;
                        CustomDialog.show(
                          context,
                          title: Row(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              Icon(Icons.info, color: p.primary),
                              const SizedBox(width: 8),
                              CustomText(
                                "정보",
                                fontSize: 18,
                                fontWeight: FontWeight.bold,
                              ),
                            ],
                          ),
                          message: Column(
                            mainAxisSize: MainAxisSize.min,
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              CustomText(
                                "이것은 Widget을 사용한 다이얼로그입니다.",
                                fontSize: 16,
                              ),
                              const SizedBox(height: 8),
                              CustomText(
                                "제목과 메시지 모두 Widget으로 지정할 수 있습니다.",
                                fontSize: 14,
                                color: p.textSecondary,
                              ),
                            ],
                          ),
                          type: DialogType.single,
                        );
                      },
                    ),
                  ),
                ],
              ),

              // 카운터 표시
              CustomCard(
                padding: const EdgeInsets.all(20),
                child: CustomColumn(
                  spacing: 8,
                  children: [
                    CustomText(
                      "확인 버튼 클릭 횟수",
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                    ),
                    CustomText(
                      '$_counter',
                      fontSize: 32,
                      fontWeight: FontWeight.bold,
                      color: Colors.orange, // 예제용 색상 유지
                    ),
                  ],
                ),
              ),

              // 자동 닫힘 제어 예시
              CustomColumn(
                spacing: 12,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  CustomText(
                    "자동 닫힘 제어 예시",
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                  ),
                  SizedBox(
                    width: double.infinity,
                    child: CustomButton(
                      btnText: "닫히지 않는 다이얼로그",
                      backgroundColor: Colors.amber, // 예제용 색상 유지
                      onCallBack: () {
                        showDialog(
                          context: context,
                          builder: (dialogContext) {
                            return AlertDialog(
                              title: CustomText(
                                "처리 중",
                                fontSize: 18,
                                fontWeight: FontWeight.bold,
                              ),
                              content: Column(
                                mainAxisSize: MainAxisSize.min,
                                children: [
                                  CustomText(
                                    "확인 버튼을 눌러도 닫히지 않습니다.\n내부 버튼으로 수동으로 닫아주세요.",
                                    fontSize: 16,
                                  ),
                                  const SizedBox(height: 16),
                                  SizedBox(
                                    width: double.infinity,
                                    child: CustomButton(
                                      btnText: "다이얼로그 닫기",
                                      // backgroundColor를 지정하지 않으면 테마 primary 색상 자동 적용
                                      onCallBack: () {
                                        Navigator.pop(dialogContext);
                                      },
                                    ),
                                  ),
                                ],
                              ),
                              actions: [
                                CustomButton(
                                  btnText: "확인",
                                  // backgroundColor를 지정하지 않으면 테마 primary 색상 자동 적용
                                  minimumSize: const Size(100, 40),
                                  onCallBack: () {
                                    // 다이얼로그가 자동으로 닫히지 않음
                                    print("확인 버튼 클릭됨 - 다이얼로그는 열려있음");
                                  },
                                ),
                              ],
                            );
                          },
                        );
                      },
                    ),
                  ),
                  SizedBox(
                    width: double.infinity,
                    child: CustomButton(
                      btnText: "비동기 작업 후 닫기",
                      backgroundColor: Colors.cyan, // 예제용 색상 유지
                      onCallBack: () {
                        CustomDialog.show(
                          context,
                          title: "처리 중",
                          message: "작업을 수행한 후 자동으로 닫힙니다...",
                          type: DialogType.single,
                          autoDismissOnConfirm: false,
                          confirmText: "처리 시작",
                          onConfirm: () async {
                            // 비동기 작업 시뮬레이션
                            await Future.delayed(const Duration(seconds: 2));
                            if (context.mounted) {
                              Navigator.pop(context);
                              // 완료 다이얼로그 표시
                              CustomDialog.show(
                                context,
                                title: "완료",
                                message: "작업이 완료되었습니다!",
                                type: DialogType.single,
                              );
                            }
                          },
                        );
                      },
                    ),
                  ),
                  SizedBox(
                    width: double.infinity,
                    child: CustomButton(
                      btnText: "확인은 닫지 않고 취소만 닫기",
                      backgroundColor: Colors.pink, // 예제용 색상 유지
                      onCallBack: () {
                        CustomDialog.show(
                          context,
                          title: "확인",
                          message: "확인 버튼은 닫히지 않고,\n취소 버튼만 다이얼로그를 닫습니다.",
                          type: DialogType.dual,
                          autoDismissOnConfirm: false,
                          autoDismissOnCancel: true,
                          onConfirm: () {
                            print("확인 클릭 - 다이얼로그는 열려있음");
                          },
                          onCancel: () {
                            print("취소 클릭 - 다이얼로그가 닫힘");
                          },
                        );
                      },
                    ),
                  ),
                ],
              ),

              // Dialog와 SnackBar 함께 사용 테스트
              CustomColumn(
                spacing: 12,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  CustomText(
                    "Dialog와 SnackBar 함께 사용 테스트",
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                  ),
                  SizedBox(
                    width: double.infinity,
                    child: CustomButton(
                      btnText: "Dialog 내부에서 SnackBar 표시 (fixed)",
                      backgroundColor: Colors.deepPurple.shade300, // 예제용 색상 유지
                      onCallBack: () {
                        CustomDialog.show(
                          context,
                          title: "SnackBar 테스트",
                          message:
                              "확인 버튼을 누르면 Dialog가 닫히지 않고 SnackBar가 표시됩니다.\nDialog는 수동으로 닫아야 합니다.",
                          type: DialogType.dual,
                          autoDismissOnConfirm: false,
                          onConfirmWithContexts: (dialogContext, dialogScaffoldCtx) {
                            // Dialog 내부 Scaffold의 context를 사용하여 SnackBar 표시
                            // Dialog 위에 SnackBar가 표시됨 (자동으로 처리됨)
                            // behavior: SnackBarBehavior.fixed (하단 고정, margin 사용 불가)
                            CustomSnackBar.showSuccess(
                              dialogScaffoldCtx,
                              message:
                                  "Dialog 내부에서 표시된 SnackBar (fixed - 하단 고정)",
                              behavior: SnackBarBehavior.fixed,
                            );
                          },
                        );
                      },
                    ),
                  ),
                  SizedBox(
                    width: double.infinity,
                    child: CustomButton(
                      btnText: "Dialog 내부에서 SnackBar 표시 (floating)",
                      backgroundColor: Colors.deepPurple.shade400, // 예제용 색상 유지
                      onCallBack: () {
                        CustomDialog.show(
                          context,
                          title: "SnackBar 테스트",
                          message:
                              "확인 버튼을 누르면 Dialog가 닫히지 않고 SnackBar가 표시됩니다.\nDialog는 수동으로 닫아야 합니다.",
                          type: DialogType.dual,
                          autoDismissOnConfirm: false,
                          onConfirmWithContexts: (dialogContext, dialogScaffoldCtx) {
                            // Dialog 내부 Scaffold의 context를 사용하여 SnackBar 표시
                            // Dialog 위에 SnackBar가 표시됨 (자동으로 처리됨)
                            // behavior: SnackBarBehavior.floating (공중에 떠있는 형태, margin 사용 가능)
                            CustomSnackBar.showSuccess(
                              dialogScaffoldCtx,
                              message:
                                  "Dialog 내부에서 표시된 SnackBar (floating - 공중에 떠있음)",
                              behavior: SnackBarBehavior.floating,
                              margin: const EdgeInsets.all(
                                16,
                              ), // floating에서만 사용 가능
                            );
                          },
                        );
                      },
                    ),
                  ),
                  SizedBox(
                    width: double.infinity,
                    child: CustomButton(
                      btnText: "Dialog 닫은 후 SnackBar 표시 (기본 사용법)",
                      backgroundColor: Colors.deepPurple.shade400, // 예제용 색상 유지
                      onCallBack: () async {
                        // Dialog가 닫힌 후에 SnackBar 표시
                        await CustomDialog.show(
                          context,
                          title: "SnackBar 테스트",
                          message: "확인 버튼을 누르면 Dialog가 닫힌 후 SnackBar가 표시됩니다.",
                          type: DialogType.dual,
                          onConfirm: () {
                            // Dialog는 자동으로 닫힘 (autoDismissOnConfirm: true)
                          },
                        );
                        // Dialog가 닫힌 후에 SnackBar 표시 (기본 사용법)
                        if (context.mounted) {
                          CustomSnackBar.showSuccess(
                            context,
                            message: "Dialog 닫은 후 표시된 SnackBar (정상적으로 표시됨)",
                          );
                        }
                      },
                    ),
                  ),
                ],
              ),

              // 커스텀 버튼 예시
              CustomColumn(
                spacing: 12,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  CustomText(
                    "커스텀 버튼 예시",
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                  ),
                  SizedBox(
                    width: double.infinity,
                    child: CustomButton(
                      btnText: "3개 버튼 다이얼로그 (세로 배치)",
                      backgroundColor: Colors.teal, // 예제용 색상 유지
                      onCallBack: () {
                        CustomDialog.show(
                          context,
                          title: "작업 선택",
                          message: "원하는 작업을 선택해주세요.",
                          customActions: [
                            DialogActionItem(
                              label: "저장",
                              backgroundColor: Colors.green,
                              onTap: () {
                                print("저장 선택");
                              },
                              autoDismiss: true,
                            ),
                            DialogActionItem(
                              label: "수정",
                              backgroundColor: Colors.blue,
                              onTap: () {
                                print("수정 선택");
                              },
                              autoDismiss: true,
                            ),
                            DialogActionItem(
                              label: "취소",
                              buttonType: ButtonType.outlined,
                              backgroundColor: Colors.grey,
                              onTap: () {
                                print("취소 선택");
                              },
                            ),
                          ],
                        );
                      },
                    ),
                  ),
                  SizedBox(
                    width: double.infinity,
                    child: CustomButton(
                      btnText: "3개 버튼 다이얼로그 (가로 배치 - DialogActionGroup)",
                      backgroundColor: Colors.teal.shade700, // 예제용 색상 유지
                      onCallBack: () {
                        CustomDialog.show(
                          context,
                          title: "작업 선택",
                          message: "원하는 작업을 선택해주세요.",
                          customActionGroups: [
                            DialogActionGroup(
                              actions: [
                                DialogActionItem(
                                  label: "저장",
                                  backgroundColor: Colors.green,
                                  onTap: () {
                                    print("저장 선택");
                                  },
                                  autoDismiss: true,
                                ),
                                DialogActionItem(
                                  label: "수정",
                                  backgroundColor: Colors.blue,
                                  onTap: () {
                                    print("수정 선택");
                                  },
                                  autoDismiss: true,
                                ),
                                DialogActionItem(
                                  label: "취소",
                                  buttonType: ButtonType.outlined,
                                  backgroundColor: Colors.grey,
                                  onTap: () {
                                    print("취소 선택");
                                  },
                                  autoDismiss: true,
                                ),
                              ],
                              direction: Axis.horizontal,
                              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                              spacing: 8,
                            ),
                          ],
                        );
                      },
                    ),
                  ),
                  SizedBox(
                    width: double.infinity,
                    child: CustomButton(
                      btnText: "그리드 배치 (Row + Column 혼합)",
                      backgroundColor: Colors.teal.shade900, // 예제용 색상 유지
                      onCallBack: () {
                        CustomDialog.show(
                          context,
                          title: "작업 선택",
                          message: "원하는 작업을 선택해주세요.",
                          customActionGroups: [
                            // 첫 번째 행: 가로 배치
                            DialogActionGroup(
                              actions: [
                                DialogActionItem(
                                  label: "저장",
                                  backgroundColor: Colors.green,
                                  onTap: () {
                                    print("저장 선택");
                                  },
                                  autoDismiss: true,
                                ),
                                DialogActionItem(
                                  label: "수정",
                                  backgroundColor: Colors.blue,
                                  onTap: () {
                                    print("수정 선택");
                                  },
                                  autoDismiss: true,
                                ),
                              ],
                              direction: Axis.horizontal,
                              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                              spacing: 8,
                            ),
                            // 두 번째 행: 가로 배치
                            DialogActionGroup(
                              actions: [
                                DialogActionItem(
                                  label: "삭제",
                                  backgroundColor: Colors.red,
                                  onTap: () {
                                    print("삭제 선택");
                                  },
                                  autoDismiss: true,
                                ),
                                DialogActionItem(
                                  label: "취소",
                                  buttonType: ButtonType.outlined,
                                  backgroundColor: Colors.grey,
                                  onTap: () {
                                    print("취소 선택");
                                  },
                                  autoDismiss: true,
                                ),
                              ],
                              direction: Axis.horizontal,
                              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                              spacing: 8,
                            ),
                          ],
                        );
                      },
                    ),
                  ),
                  SizedBox(
                    width: double.infinity,
                    child: CustomButton(
                      btnText: "직접 위젯 전달 (actions 파라미터)",
                      backgroundColor: Colors.indigo, // 예제용 색상 유지
                      onCallBack: () {
                        CustomDialog.show(
                          context,
                          title: "작업 선택",
                          message: "원하는 작업을 선택해주세요.",
                          actions: [
                            Row(
                              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                              children: [
                                Expanded(
                                  child: CustomButton(
                                    btnText: "저장",
                                    backgroundColor: Colors.green, // 예제용 색상 유지
                                    minimumSize: const Size(0, 40),
                                    onCallBack: () {
                                      print("저장 선택");
                                      Navigator.pop(context);
                                    },
                                  ),
                                ),
                                const SizedBox(width: 8),
                                Expanded(
                                  child: CustomButton(
                                    btnText: "수정",
                                    // backgroundColor를 지정하지 않으면 테마 primary 색상 자동 적용
                                    minimumSize: const Size(0, 40),
                                    onCallBack: () {
                                      print("수정 선택");
                                      Navigator.pop(context);
                                    },
                                  ),
                                ),
                                const SizedBox(width: 8),
                                Expanded(
                                  child: CustomButton(
                                    btnText: "취소",
                                    buttonType: ButtonType.outlined,
                                    backgroundColor: Colors.grey, // 예제용 색상 유지
                                    minimumSize: const Size(0, 40),
                                    onCallBack: () {
                                      print("취소 선택");
                                      Navigator.pop(context);
                                    },
                                  ),
                                ),
                              ],
                            ),
                          ],
                        );
                      },
                    ),
                  ),
                  SizedBox(
                    width: double.infinity,
                    child: CustomButton(
                      btnText: "4개 버튼 (저장/수정/삭제/취소)",
                      backgroundColor: Colors.indigo, // 예제용 색상 유지
                      onCallBack: () {
                        CustomDialog.show(
                          context,
                          title: "파일 관리",
                          message: "이 파일에 대해 어떤 작업을 하시겠습니까?",
                          customActions: [
                            DialogActionItem(
                              label: "저장",
                              backgroundColor: Colors.green,
                              minimumSize: const Size(70, 40),
                              onTap: () {
                                print("저장");
                                if (context.mounted) {
                                  Navigator.pop(context);
                                  CustomDialog.show(
                                    context,
                                    title: "저장 완료",
                                    message: "파일이 저장되었습니다.",
                                    type: DialogType.single,
                                  );
                                }
                              },
                            ),
                            DialogActionItem(
                              label: "수정",
                              backgroundColor: Colors.blue,
                              minimumSize: const Size(70, 40),
                              onTap: () {
                                print("수정");
                              },
                            ),
                            DialogActionItem(
                              label: "삭제",
                              backgroundColor: Colors.red,
                              buttonType: ButtonType.outlined,
                              minimumSize: const Size(70, 40),
                              onTap: () {
                                print("삭제");
                              },
                            ),
                            DialogActionItem(
                              label: "취소",
                              buttonType: ButtonType.outlined,
                              backgroundColor: Colors.grey,
                              minimumSize: const Size(70, 40),
                              onTap: () {},
                            ),
                          ],
                        );
                      },
                    ),
                  ),
                  SizedBox(
                    width: double.infinity,
                    child: CustomButton(
                      btnText: "닫히지 않는 커스텀 버튼",
                      backgroundColor: Colors.deepOrange, // 예제용 색상 유지
                      onCallBack: () {
                        showDialog(
                          context: context,
                          builder: (dialogContext) {
                            return AlertDialog(
                              title: CustomText(
                                "선택",
                                fontSize: 18,
                                fontWeight: FontWeight.bold,
                              ),
                              content: Column(
                                mainAxisSize: MainAxisSize.min,
                                children: [
                                  CustomText(
                                    "저장 버튼은 다이얼로그를 닫지 않습니다.\n내부 버튼으로 수동으로 닫을 수 있습니다.",
                                    fontSize: 16,
                                  ),
                                  const SizedBox(height: 16),
                                  CustomButton(
                                    btnText: "다이얼로그 닫기",
                                    backgroundColor: Colors.red, // 예제용 색상 유지
                                    onCallBack: () {
                                      Navigator.pop(dialogContext);
                                    },
                                  ),
                                ],
                              ),
                              actions: [
                                CustomButton(
                                  btnText: "저장",
                                  backgroundColor: Colors.green, // 예제용 색상 유지
                                  minimumSize: const Size(80, 40),
                                  onCallBack: () {
                                    print("저장 중... (다이얼로그는 열려있음)");
                                    // 다이얼로그를 열어둔 채로 다른 작업 수행 가능
                                  },
                                ),
                                CustomButton(
                                  btnText: "취소",
                                  buttonType: ButtonType.outlined,
                                  backgroundColor: Colors.grey, // 예제용 색상 유지
                                  minimumSize: const Size(80, 40),
                                  onCallBack: () {
                                    Navigator.pop(dialogContext);
                                  },
                                ),
                              ],
                            );
                          },
                        );
                      },
                    ),
                  ),
                  SizedBox(
                    width: double.infinity,
                    child: CustomButton(
                      btnText: "Widget 라벨 커스텀 버튼",
                      backgroundColor: Colors.brown, // 예제용 색상 유지
                      onCallBack: () {
                        CustomDialog.show(
                          context,
                          title: "선택",
                          message: "버튼 라벨에 아이콘을 포함할 수 있습니다.",
                          customActions: [
                            DialogActionItem(
                              label: Row(
                                mainAxisSize: MainAxisSize.min,
                                children: [
                                  Icon(
                                    Icons.save,
                                    color: Colors.white,
                                    size: 20,
                                  ),
                                  const SizedBox(width: 4),
                                  CustomText("저장", fontSize: 16),
                                ],
                              ),
                              backgroundColor: Colors.green,
                              onTap: () {
                                print("저장");
                              },
                            ),
                            DialogActionItem(
                              label: Row(
                                mainAxisSize: MainAxisSize.min,
                                children: [
                                  Icon(
                                    Icons.delete,
                                    color: Colors.white,
                                    size: 20,
                                  ),
                                  const SizedBox(width: 4),
                                  CustomText("삭제", fontSize: 16),
                                ],
                              ),
                              backgroundColor: Colors.red,
                              onTap: () {
                                print("삭제");
                              },
                            ),
                            DialogActionItem(
                              label: Row(
                                mainAxisSize: MainAxisSize.min,
                                children: [
                                  Icon(
                                    Icons.cancel,
                                    color: Colors.grey.shade700,
                                    size: 20,
                                  ),
                                  const SizedBox(width: 4),
                                  CustomText(
                                    "취소",
                                    fontSize: 16,
                                    color: Colors.grey.shade700,
                                  ),
                                ],
                              ),
                              buttonType: ButtonType.outlined,
                              backgroundColor: Colors.grey,
                              onTap: () {},
                            ),
                          ],
                        );
                      },
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}
