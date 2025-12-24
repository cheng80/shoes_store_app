import 'package:flutter/material.dart';

import '../custom/external_util/storage/custom_storage_util.dart';
import '../custom/widgets.dart';
import '../theme/app_colors.dart';

/// StorageUtil 사용 예제 페이지
///
/// 주의: 이 페이지를 사용하려면 pubspec.yaml에 shared_preferences 패키지가 필요합니다.
class StoragePage extends StatefulWidget {
  const StoragePage({super.key});

  @override
  State<StoragePage> createState() => _StoragePageState();
}

class _StoragePageState extends State<StoragePage> {
  String? _username;
  int? _age;
  bool? _isDarkMode;
  List<String>? _tags;

  @override
  void initState() {
    super.initState();
    _loadData();
  }

  /// 저장된 데이터 불러오기
  Future<void> _loadData() async {
    final username = await CustomStorageUtil.getString('username');
    final age = await CustomStorageUtil.getInt('age');
    final isDarkMode = await CustomStorageUtil.getBool('isDarkMode');
    final tags = await CustomStorageUtil.getStringList('tags');

    setState(() {
      _username = username;
      _age = age;
      _isDarkMode = isDarkMode;
      _tags = tags;
    });
  }

  /// 기본 타입 저장 예제
  Future<void> _saveBasicTypes() async {
    await CustomStorageUtil.setString('username', '홍길동');
    await CustomStorageUtil.setInt('age', 25);
    await CustomStorageUtil.setBool('isDarkMode', true);
    await CustomStorageUtil.setDouble('price', 99.99);
    await CustomStorageUtil.setStringList('tags', [
      'flutter',
      'dart',
      'mobile',
    ]);

    await _loadData();
  }

  /// 객체 저장 예제
  Future<void> _saveObject() async {
    final user = User(name: '홍길동', age: 25, email: 'hong@example.com');
    await CustomStorageUtil.setObject('user', user);

    // 객체 불러오기
    final savedUser = await CustomStorageUtil.getObject<User>(
      'user',
      (json) => User.fromJson(json),
    );

    if (savedUser != null && mounted) {
      CustomSnackBar.showSuccess(
        context,
        message: '저장된 사용자: ${savedUser.name}, ${savedUser.age}세',
      );
    }
  }

  /// 리스트 저장 예제
  Future<void> _saveList() async {
    final items = [
      Item(name: '사과', price: 1000),
      Item(name: '바나나', price: 2000),
      Item(name: '오렌지', price: 1500),
    ];

    await CustomStorageUtil.setList('items', items);

    // 리스트 불러오기
    final savedItems = await CustomStorageUtil.getList<Item>(
      'items',
      (json) => Item.fromJson(json),
    );

    if (savedItems != null && mounted) {
      CustomSnackBar.showSuccess(
        context,
        message: '저장된 아이템 개수: ${savedItems.length}',
      );
    }
  }

  /// 키 삭제 예제
  Future<void> _removeKey() async {
    await CustomStorageUtil.remove('username');
    await _loadData();
  }

  /// 모든 데이터 삭제 예제
  Future<void> _clearAll() async {
    await CustomStorageUtil.clear();
    await _loadData();
  }

  /// 키 존재 여부 확인 예제
  Future<void> _checkKey() async {
    final exists = await CustomStorageUtil.containsKey('username');
    if (mounted) {
      if (exists) {
        CustomSnackBar.showSuccess(context, message: 'username 키가 존재합니다');
      } else {
        CustomSnackBar.showInfo(context, message: 'username 키가 존재하지 않습니다');
      }
    }
  }

  /// 모든 키 가져오기 예제
  Future<void> _getAllKeys() async {
    final keys = await CustomStorageUtil.getAllKeys();
    if (mounted) {
      CustomSnackBar.showInfo(context, message: '모든 키: ${keys.join(", ")}');
    }
  }

  @override
  Widget build(BuildContext context) {
    final p = context.palette;
    return Scaffold(
      backgroundColor: p.background,
      appBar: CustomAppBar(
        title: 'StorageUtil 예제',
        backgroundColor: Colors.teal, // 예제용 색상 유지
        foregroundColor: Colors.white,
      ),
      body: SingleChildScrollView(
        child: CustomPadding.all(
          16.0,
          child: CustomColumn(
            spacing: 16,
            children: [
              // 저장된 데이터 표시
              CustomCard(
                padding: const EdgeInsets.all(16),
                child: CustomColumn(
                  spacing: 12,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    CustomText(
                      '저장된 데이터',
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                    ),
                    const SizedBox(height: 8),
                    CustomText('이름: ${_username ?? '없음'}'),
                    CustomText('나이: ${_age ?? '없음'}'),
                    CustomText('다크모드: ${_isDarkMode ?? '없음'}'),
                    CustomText('태그: ${_tags?.join(', ') ?? '없음'}'),
                  ],
                ),
              ),

              // 기본 타입 저장 버튼
              SizedBox(
                width: double.infinity,
                child: CustomButton(
                  btnText: '기본 타입 저장',
                  // backgroundColor를 지정하지 않으면 테마 primary 색상 자동 적용
                  onCallBack: _saveBasicTypes,
                ),
              ),

              // 객체 저장 버튼
              SizedBox(
                width: double.infinity,
                child: CustomButton(
                  btnText: '객체 저장',
                  backgroundColor: Colors.green,
                  onCallBack: _saveObject,
                ),
              ),

              // 리스트 저장 버튼
              SizedBox(
                width: double.infinity,
                child: CustomButton(
                  btnText: '리스트 저장',
                  backgroundColor: Colors.purple,
                  onCallBack: _saveList,
                ),
              ),

              // 키 삭제 버튼
              SizedBox(
                width: double.infinity,
                child: CustomButton(
                  btnText: '키 삭제 (username)',
                  backgroundColor: Colors.orange,
                  onCallBack: _removeKey,
                ),
              ),

              // 키 존재 여부 확인 버튼
              SizedBox(
                width: double.infinity,
                child: CustomButton(
                  btnText: '키 존재 여부 확인',
                  backgroundColor: Colors.indigo,
                  onCallBack: _checkKey,
                ),
              ),

              // 모든 키 가져오기 버튼
              SizedBox(
                width: double.infinity,
                child: CustomButton(
                  btnText: '모든 키 가져오기',
                  backgroundColor: Colors.cyan,
                  onCallBack: _getAllKeys,
                ),
              ),

              // 모든 데이터 삭제 버튼
              SizedBox(
                width: double.infinity,
                child: CustomButton(
                  btnText: '모든 데이터 삭제',
                  backgroundColor: Colors.red,
                  onCallBack: _clearAll,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

/// 예제용 User 클래스
class User {
  final String name;
  final int age;
  final String email;

  User({required this.name, required this.age, required this.email});

  Map<String, dynamic> toJson() => {'name': name, 'age': age, 'email': email};

  factory User.fromJson(Map<String, dynamic> json) => User(
    name: json['name'] as String,
    age: json['age'] as int,
    email: json['email'] as String,
  );
}

/// 예제용 Item 클래스
class Item {
  final String name;
  final int price;

  Item({required this.name, required this.price});

  Map<String, dynamic> toJson() => {'name': name, 'price': price};

  factory Item.fromJson(Map<String, dynamic> json) =>
      Item(name: json['name'] as String, price: json['price'] as int);
}
