import 'package:shoes_store_app/config.dart' as config;
import 'package:shoes_store_app/database/core/database_manager.dart';
import 'package:shoes_store_app/database/dummy_data/dummy_data_setting.dart';
import 'package:shoes_store_app/view/cheng/screens/auth/login_view.dart';
import 'package:shoes_store_app/view/cheng/screens/customer/search_view.dart';
import 'package:shoes_store_app/view/customer/address_payment_view.dart';
import 'package:shoes_store_app/view/customer/cart.dart';
import 'package:shoes_store_app/view/customer/detail_view.dart';
import 'package:shoes_store_app/view/customer/purchase_view.dart';

import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:get_storage/get_storage.dart';
import 'package:path/path.dart';
import 'package:sqflite/sqflite.dart';

// final GoRouter router = GoRouter(

//   initialLocation: config.routeLogin,
//   routes: [
//     GoRoute(path: config.routeLogin, builder: (context, state) => SearchView()),
//     GoRoute(
//       path: config.routeSettings,
//       builder: (context, state) => SettingPage(),
//     ),
//   ],
// );
Future<void> main() async {
  // GetStorage 초기화 (get_storage 사용 전 필수)
  await GetStorage.init();
  WidgetsFlutterBinding.ensureInitialized();

  // 데이터베이스 초기화 (DatabaseManager 사용)
  final dbPath = await getDatabasesPath();
  final path = join(dbPath, '${config.kDBName}${config.kDBFileExt}');
  
  // 개발 중이므로 기존 DB 삭제 (운영 환경에서는 제거)
  await deleteDatabase(path);
  
  // DatabaseManager로 DB 초기화
  final dbManager = DatabaseManager();
  await dbManager.initializeDB();

  // 더미 데이터 삽입 (새 핸들러 방식 사용)
  final dummyDataSetting = DummyDataSetting();
  await dummyDataSetting.insertAllDummyData();
  
  runApp(const MyApp());
}

class MyApp extends StatefulWidget {
  const MyApp({super.key});

  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  final ThemeMode _themeMode = ThemeMode.system; // 시스템에서 설정한 색상으로 초기화

  final Color _seedColor = Colors.deepPurple;

  @override
  Widget build(BuildContext context) {
    return GetMaterialApp(
      title: 'Flutter Demo',
      // routerConfig: router,
      themeMode: _themeMode,
      theme: ThemeData(
        brightness: Brightness.light,

        colorSchemeSeed: _seedColor,
      ),
      darkTheme: ThemeData(
        brightness: Brightness.dark,
        colorSchemeSeed: _seedColor,
      ),
      initialRoute: '/',
      getPages: [
        GetPage(name: '/', page: () => LoginView(),),
        GetPage(name: '/cart', page: () => Cart(),),
        GetPage(name: '/searchview', page: () => SearchView(),),
        GetPage(name: '/detailview', page: () => DetailView(),),
        GetPage(name: '/purchaseview', page: () => PurchaseView(),),
        // GetPage(name: '/returnview', page: () => ReturnView(),),
        GetPage(name: '/address-payment', page: () => AddressPaymentView()),
      ],
      debugShowCheckedModeBanner: false,
    );
  }
}
