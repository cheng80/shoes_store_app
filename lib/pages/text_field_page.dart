import 'package:flutter/material.dart';

import '../custom/widgets.dart';
import '../theme/app_colors.dart';

/// TextField 사용 예제 페이지
class TextFieldPage extends StatefulWidget {
  const TextFieldPage({super.key});

  @override
  State<TextFieldPage> createState() => _TextFieldPageState();
}

class _TextFieldPageState extends State<TextFieldPage> {
  final _formKey = GlobalKey<FormState>();
  late TextEditingController _idController;
  late TextEditingController _pwController;
  late TextEditingController _nameController;
  late TextEditingController _emailController;
  late TextEditingController _phoneController;
  late TextEditingController _numberController;

  @override
  void initState() {
    super.initState();
    _idController = TextEditingController();
    _pwController = TextEditingController();
    _nameController = TextEditingController();
    _emailController = TextEditingController();
    _phoneController = TextEditingController();
    _numberController = TextEditingController();
  }

  @override
  void dispose() {
    _idController.dispose();
    _pwController.dispose();
    _nameController.dispose();
    _emailController.dispose();
    _phoneController.dispose();
    _numberController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () {
        // TextField 항목은 키보드 자동으로 내리기 위해 이걸 해주는게 좋다.
        FocusScope.of(context).unfocus(); // 버튼이나 키보드, 인풋 박스 이외에 터치 하면 언포커스
      },
      behavior: HitTestBehavior.opaque, // 자식 위젯이 터치를 소비해도 onTap이 호출되도록 설정
      child: Scaffold(
        backgroundColor: context.palette.background,
        appBar: CustomAppBar(
          title: "TextField 예시",
          backgroundColor: Colors.green, // 예제용 색상 유지
        ),
        body: SingleChildScrollView(
          child: CustomPadding.all(
            16.0,
            child: CustomColumn(
              spacing: 20,
              children: [
                CustomText(
                  "입력 필드 종합 예시",
                  fontSize: 24,
                  fontWeight: FontWeight.bold,
                  color: Colors.green, // 예제용 색상 유지
                ),

                // 기본 텍스트 입력
                CustomColumn(
                  spacing: 12,
                  children: [
                    CustomText(
                      "기본 텍스트 입력",
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                    ),
                    CustomTextField(
                      controller: _idController,
                      labelText: "아이디를 입력하세요",
                      keyboardType: TextInputType.text,
                    ),
                  ],
                ),

                // 필수 입력 필드
                CustomColumn(
                  spacing: 12,
                  children: [
                    CustomText(
                      "필수 입력 필드 (required: true)",
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                    ),
                    CustomTextField(
                      controller: _nameController,
                      labelText: "이름 (필수)",
                      keyboardType: TextInputType.name,
                      required: true,
                      requiredMessage: "이름을 입력해주세요",
                    ),
                  ],
                ),

                // 비밀번호 입력
                CustomColumn(
                  spacing: 12,
                  children: [
                    CustomText(
                      "비밀번호 입력",
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                    ),
                    CustomTextField(
                      controller: _pwController,
                      labelText: "비밀번호를 입력하세요",
                      obscureText: true,
                    ),
                  ],
                ),

                // 이메일 필수 입력
                CustomColumn(
                  spacing: 12,
                  children: [
                    CustomText(
                      "이메일 입력 (필수)",
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                    ),
                    CustomTextField(
                      controller: _emailController,
                      labelText: "이메일 (필수)",
                      keyboardType: TextInputType.emailAddress,
                      required: true,
                      requiredMessage: "이메일을 입력해주세요",
                    ),
                  ],
                ),

                // 이메일 입력
                CustomColumn(
                  spacing: 12,
                  children: [
                    CustomText(
                      "이메일 입력",
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                    ),
                    CustomTextField(
                      controller: _emailController,
                      labelText: "이메일",
                      keyboardType: TextInputType.emailAddress,
                    ),
                  ],
                ),

                // 전화번호 입력 (textCheck 예시)
                CustomColumn(
                  spacing: 12,
                  children: [
                    CustomText(
                      "전화번호 입력 (textCheck 사용 예시)",
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                    ),
                    CustomTextField(
                      controller: _phoneController,
                      labelText: "전화번호",
                      keyboardType: TextInputType.phone,
                    ),
                    CustomButton(
                      btnText: "textCheck 검증",
                      backgroundColor: Colors.orange, // 예제용 색상 유지
                      minimumSize: const Size(double.infinity, 50),
                      onCallBack: () {
                        // textCheck를 사용한 검증 예시
                        // 전화번호 필드가 비어있는지 체크
                        if (!CustomTextField.textCheck(context, _phoneController)) {
                          CustomSnackBar.showError(
                            context,
                            message: "전화번호를 입력해주세요",
                          );
                          return;
                        }
                        
                        // 여러 필드를 체크하는 예시
                        if (!CustomTextField.textCheck(context, _nameController)) {
                          CustomSnackBar.showError(
                            context,
                            message: "이름을 입력해주세요",
                          );
                          return;
                        }
                        
                        // 모든 검증 통과
                        CustomDialog.show(
                          context,
                          title: "검증 성공",
                          message: "전화번호와 이름이 모두 입력되었습니다.",
                          type: DialogType.single,
                        );
                      },
                    ),
                  ],
                ),

                // 숫자 입력
                CustomColumn(
                  spacing: 12,
                  children: [
                    CustomText(
                      "숫자 입력",
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                    ),
                    CustomTextField(
                      controller: _numberController,
                      labelText: "숫자를 입력하세요",
                      keyboardType: TextInputType.number,
                    ),
                  ],
                ),

                const SizedBox(height: 20),

                // Form을 사용한 검증 예시
                CustomColumn(
                  spacing: 12,
                  children: [
                    CustomText(
                      "Form 검증 예시",
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                    ),
                    Form(
                      key: _formKey,
                      child: CustomColumn(
                        spacing: 12,
                        children: [
                          CustomTextField(
                            controller: _idController,
                            labelText: "아이디 (필수)",
                            required: true,
                            requiredMessage: "아이디를 입력해주세요",
                          ),
                          CustomTextField(
                            controller: _pwController,
                            labelText: "비밀번호 (필수)",
                            obscureText: true,
                            required: true,
                            requiredMessage: "비밀번호를 입력해주세요",
                          ),
                        ],
                      ),
                    ),
                  ],
                ),

                const SizedBox(height: 20),

                // 제출 버튼
                CustomRow(
                  spacing: 12,
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    CustomButton(
                      btnText: "입력값 확인",
                      backgroundColor: Colors.green, // 예제용 색상 유지
                      minimumSize: const Size(150, 50),
                      onCallBack: () {
                        // 버튼 클릭 시 키보드 내리기
                        FocusScope.of(context).unfocus();
                        CustomDialog.show(
                          context,
                          title: "입력값 확인",
                          message:
                              "아이디: ${_idController.text}\n"
                              "이름: ${_nameController.text}\n"
                              "이메일: ${_emailController.text}\n"
                              "전화번호: ${_phoneController.text}\n"
                              "숫자: ${_numberController.text}",
                          type: DialogType.single,
                        );
                      },
                    ),
                    CustomButton(
                      btnText: "Form 검증",
                      // backgroundColor를 지정하지 않으면 테마 primary 색상 자동 적용
                      minimumSize: const Size(150, 50),
                      onCallBack: () {
                        // 버튼 클릭 시 키보드 내리기
                        FocusScope.of(context).unfocus();
                        if (_formKey.currentState!.validate()) {
                          CustomDialog.show(
                            context,
                            title: "검증 성공",
                            message: "모든 필수 항목이 입력되었습니다.",
                            type: DialogType.single,
                          );
                        }
                      },
                    ),
                  ],
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
