//  Configuration of the App


import 'package:flutter/material.dart';
import 'package:shoes_store_app/custom/custom_common_util.dart';


const String kDBName = 'shoes_store_db';
const String kDBFileExt = '.db';
const int kVersion = 1;



//  Screen Datas
const seedColorDefault = Colors.deepPurple;
const defaultThemeMode = ThemeMode.system;

//  Paths
const String kImageAssetPath = 'images/';
const String kIconAssetPath = 'icons/';

//  DB Dummies
const int kDefaultUserId = -1;  //  UserID befor login
const String kDefaultProductImage = '${kImageAssetPath}default.png';  //  Default image for ProductBase

//  Storage Keys
const String kStorageKeyDBInitialized = 'db_initialized';  //  DB 초기화 완료 여부 저장 키

//  Formats
const String dateFormat = 'yyyy-MM-dd';
const String dateTimeFormat = 'yyyy-MM-dd HH:mm:ss';
String priceFormatter(int price) => CustomCommonUtil.formatNumber(price);
const int minPasswordLength = 8;
const int maxPasswordLength = 20;

final RegExp emailRegex = RegExp(
  r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$',
);
const int kDefaultPageSize = 20;  //  Pagenation
const Duration kApiTimeout = Duration(seconds: 10); //  App timeout
const Duration kLoginDelay = Duration(seconds: 2);  //  Delay when pressing Login button

//  Searchview presets
const TextStyle rLabel = TextStyle(color: Colors.black, fontSize: 20, fontWeight: FontWeight.bold);

//  Features
const bool kEnableSaleFeature = true;
const bool kEnableStockAutoRequest = true;
const bool kUseLocalDBOnly = true;

//  Tables
const String kTableCustomer = 'Customer';
const String kTableProductImage = 'ProductImage';
const String kTableProductBase = 'ProductBase';
const String kTableManufacturer = 'Manufacturer';
const String kTableProduct = 'Product';
const String tTableEmployee = 'Employee';
//  Point 3
const String kTableLoginHistory = 'LoginHistory';
const String kTablePurchaseItem = 'PurchaseItem';


//  Routes
const String routeLogin = '/';
const String routeSettings = '/settings';
const String routeProductDetail = '/product';
const String routeCart = '/cart';
const String routePurchaseHistory = '/history';

// Pickup 상태
// Point 6
Map pickupStatus = {
  0 : '제품 준비 중',
  1 : '제품 준비 완료',
  2 : '제품 수령 완료',
  3 : '반품 신청',
  4 : '반품 처리 중',
  5 : '반품 완료'
};

// 회원 상태 
Map loginStatus =  {
  0 : '활동 회원',
  1 : '휴면 회원',
  2 : '탈퇴 회원'
}; 

// 서울 내 자치구 리스트.
const List<String> district = [
  '강남구',
  '강동구',
  '강북구',
  '강서구',
  '관악구',
  '광진구',
  '구로구',
  '금천구',
  '노원구',
  '도봉구',
  '동대문구',
  '동작구',
  '마포구',
  '서대문구',
  '서초구',
  '성동구',
  '성북구',
  '송파구',
  '양천구',
  '영등포구',
  '용산구',
  '은평구',
  '종로구',
  '중구',
  '중랑구',
];