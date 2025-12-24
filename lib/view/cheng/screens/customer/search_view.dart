import 'package:flutter/material.dart';

import 'package:shoes_store_app/database/handlers/manufacturer_handler.dart';
import 'package:shoes_store_app/custom/custom_dialog.dart';
import 'package:shoes_store_app/custom/util/navigation/custom_navigation_util.dart';
import 'package:shoes_store_app/database/handlers/product_base_handler.dart';
import 'package:shoes_store_app/database/handlers/product_handler.dart';
import 'package:shoes_store_app/model/product/manufacturer.dart';
import 'package:shoes_store_app/model/product/product.dart';
import 'package:shoes_store_app/model/product/product_base.dart';
import 'package:shoes_store_app/view/customer/address_payment_view.dart';
import 'package:shoes_store_app/view/cheng/storage/user_storage.dart';
import 'package:shoes_store_app/view/cheng/test_navigation_page.dart';
import 'package:shoes_store_app/view/cheng/screens/auth/login_view.dart';
import 'package:shoes_store_app/view/cheng/screens/customer/order_list_view.dart';
import 'package:shoes_store_app/view/cheng/screens/customer/return_list_view.dart';
import 'package:shoes_store_app/view/cheng/screens/customer/user_profile_edit_view.dart';

class SearchView extends StatefulWidget {
  const SearchView({super.key});

  @override
  State<SearchView> createState() => _SearchViewState();
}

class _SearchViewState extends State<SearchView> {
  /// 제조사 핸들러
  final ManufacturerHandler _manufacturerHandler = ManufacturerHandler();
  
  /// 제품 핸들러
  final ProductHandler _productHandler = ProductHandler();
  
  /// 제품 기본 정보 핸들러
  final ProductBaseHandler _productBaseHandler = ProductBaseHandler();

  /// 사용자 정보
  String _userName = '사용자';
  String _userEmail = '이메일 없음';

  final TextEditingController _searchController = TextEditingController();
  
  /// 전체 ProductBase 목록
  List<ProductBase>? _allPBs;
  
  /// 필터링된 ProductBase 목록
  List<ProductBase>? _filteredPBs;

  /// pbid -> Product 매핑
  Map<int, Product> _prodMap = {};
  
  /// mfid -> Manufacturer 매핑
  Map<int, Manufacturer> _mfMap = {};

  /// pbid -> 첫 번째 이미지 경로 매핑
  Map<int, String> _imgMap = {};
  
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _loadUserInfo();
    loadProductData();
    Future.delayed(const Duration(milliseconds: 200), () {
      if (mounted) {
        _loadUserInfo();
      }
    });
  }

  /// 사용자 정보 로드
  void _loadUserInfo() {
    try {
      final savedUser = UserStorage.getUser();
      if (savedUser != null) {
        setState(() {
          _userName = savedUser.cName;
          _userEmail = savedUser.cEmail;
        });
        print('=== 사용자 정보 로드 성공 ===');
        print('  - 이름: $_userName');
        print('  - 이메일: $_userEmail');
      } else {
        // getUser()가 null이면 개별 메서드로 시도
        final name = UserStorage.getUserName();
        final email = UserStorage.getUserEmail();
        if (name != null || email != null) {
          setState(() {
            if (name != null) _userName = name;
            if (email != null) _userEmail = email;
          });
          print('=== 사용자 정보 로드 성공 (개별 메서드) ===');
          print('  - 이름: $_userName');
          print('  - 이메일: $_userEmail');
        } else {
          print('=== 사용자 정보 없음 ===');
        }
      }
    } catch (e) {
      print('사용자 정보 로드 에러: $e');
    }
  }

  /// 제품 데이터 로드
  Future<void> loadProductData() async {
    setState(() => _loading = true);

    /// ProductBase + 첫 번째 이미지 한 번에 조회 (서브쿼리 사용)
    final productsWithImages = await _productBaseHandler.queryListWithFirstImage();

    /// Map에서 ProductBase 객체로 변환 및 이미지 경로 추출
    final pbs = <ProductBase>[];
    final imgMap = <int, String>{};
    
    for (final map in productsWithImages) {
      // ProductBase 객체 생성
      final pb = ProductBase.fromMap(map);
      pbs.add(pb);
      
      // 첫 번째 이미지 경로 추출
      final firstImage = map['firstImage'] as String?;
      if (pb.id != null && firstImage != null && firstImage.isNotEmpty) {
        imgMap[pb.id!] = firstImage;
      }
    }

    /// pbid 목록 수집
    final pbids = <int>{};
    for (final pb in pbs) {
      if (pb.id != null) pbids.add(pb.id!);
    }

    /// pbid -> Product(대표 1개) 캐싱 + mfid 수집
    final prodMap = <int, Product>{};
    final mfids = <int>{};

    for (final pbid in pbids) {
      try {
        final products = await _productHandler.queryByProductBaseId(pbid);
        if (products.isNotEmpty) {
          final prod = products.first;
          prodMap[pbid] = prod;

          if (prod.mfid != null) {
            mfids.add(prod.mfid!);
          }
        }
      } catch (_) {
        // Product가 없으면 스킵
      }
    }

    /// mfid -> Manufacturer 캐싱
    final mfMap = <int, Manufacturer>{};
    for (final mfid in mfids) {
      try {
        final manufacturer = await _manufacturerHandler.queryById(mfid);
        if (manufacturer != null) {
          mfMap[mfid] = manufacturer;
        }
      } catch (_) {
        // Manufacturer가 없으면 스킵
      }
    }

    setState(() {
      _allPBs = pbs;
      _filteredPBs = pbs;
      _prodMap = prodMap;
      _mfMap = mfMap;
      _imgMap = imgMap;
      _loading = false;
    });
  }

  void _onSearchChanged(String keyword) {
    if (keyword.trim().isEmpty) {
      _filteredPBs = _allPBs;
    } else {
      final lower = keyword.toLowerCase();
      _filteredPBs = _allPBs!.where((p) {
        return p.pName.toLowerCase().contains(lower);
      }).toList();
    }
    setState(() {});
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFD9D9D9),

      // 👤 Drawer 안에 사용자 정보
      drawer: _buildUserDrawer(),

      appBar: AppBar(
        backgroundColor: const Color(0xFFD9D9D9),
        elevation: 0,
        leading: Builder(
          builder: (context) => IconButton(
            icon: const Icon(Icons.menu),
            onPressed: () {
              _loadUserInfo();
              Scaffold.of(context).openDrawer(); // 🔥 Drawer 열기
            },
          ),
        ),
        centerTitle: true,
        title: const Text(
          'Shoe King',
          style: TextStyle(fontWeight: FontWeight.bold),
        ),
        actions: [
          // 장바구니 아이콘 버튼 (검색바 텍스트 오른쪽 끝과 정렬되도록 우측 패딩 추가)
          Padding(
            padding: const EdgeInsets.only(right: 16),
            child: IconButton(
              icon: const Icon(Icons.shopping_cart),
              onPressed: () {
                CustomNavigationUtil.toNamed(context, '/cart');
              },
              tooltip: '장바구니',
            ),
          ),
        ],
      ),

      body: Column(
        children: [
          // 🔍 검색바 (페이지 안에서 검색)
          Padding(
            padding: const EdgeInsets.fromLTRB(16, 12, 16, 12),
            child: TextField(
              controller: _searchController,
              onChanged: _onSearchChanged,
              decoration: InputDecoration(
                hintText: '원하는 신발을 찾아보아요',
                filled: true,
                fillColor: Colors.white,
                contentPadding: const EdgeInsets.symmetric(
                  horizontal: 16,
                  vertical: 0,
                ),
                prefixIcon: const Icon(Icons.search),
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(24),
                  borderSide: BorderSide.none,
                ),
              ),
            ),
          ),

          // 🥿 상품 카드 2열 그리드
          Expanded(
            child: _loading
                ? const Center(child: CircularProgressIndicator())
                : GridView.builder(
                    padding: const EdgeInsets.all(8),
                    gridDelegate:
                        const SliverGridDelegateWithFixedCrossAxisCount(
                          crossAxisCount: 2,
                          crossAxisSpacing: 12,
                          mainAxisSpacing: 12,
                          childAspectRatio: 0.75,
                        ),
                    itemCount: _filteredPBs!.length,
                    itemBuilder: (context, index) {
                      final pb = _filteredPBs![index];
                      final pbid = pb.id;

                      final prod = (pbid != null) ? _prodMap[pbid] : null;
                      final mf = (prod?.mfid != null)
                          ? _mfMap[prod!.mfid!]
                          : null;
                      final imgPath = (pbid != null) ? _imgMap[pbid] : null;

                      final priceText = (prod?.basePrice ?? 0)
                          .toString(); // ✅ Product.basePrice

                      return GestureDetector(
                        onTap: () {
                          if (pbid == null) return;
                          CustomNavigationUtil.toNamed(
                            context,
                            '/detailview',
                            arguments: pbid,
                          );
                        },
                        child: Card(
                          elevation: 3,
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(16),
                          ),
                          child: Padding(
                            padding: const EdgeInsets.all(8),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Expanded(
                                  child: ClipRRect(
                                    borderRadius: BorderRadius.circular(12),
                                    child: _buildImage(imgPath),
                                  ),
                                ),
                                const SizedBox(height: 8),
                                Text(
                                  pb.pName,
                                  style: const TextStyle(
                                    fontWeight: FontWeight.bold,
                                    fontSize: 15,
                                  ),
                                  maxLines: 1,
                                  overflow: TextOverflow.ellipsis,
                                ),
                                Text(
                                  mf?.mName ?? '제조사 없음',
                                  style: const TextStyle(color: Colors.grey),
                                  maxLines: 1,
                                  overflow: TextOverflow.ellipsis,
                                ),
                                Text(
                                  '$priceText원',
                                  style: const TextStyle(
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ),
                      );
                    },
                  ),
          ),
        ],
      ),
    );
  }

  Widget _buildImage(String? imagePath) {
    if (imagePath != null && imagePath.isNotEmpty) {
      return Image.asset(imagePath, fit: BoxFit.cover, width: double.infinity);
    }
    return Image.asset(
      'assets/images/no_image.png',
      fit: BoxFit.cover,
      width: double.infinity,
    );
  }

  Drawer _buildUserDrawer() {
    final userInitial = _userName.isNotEmpty && _userName != '사용자'
        ? _userName[0].toUpperCase()
        : 'U';

    // 디버깅: 드로워 빌드 시 사용자 정보 확인
    print('=== Drawer 빌드 - 사용자 정보 ===');
    print('  - userName: $_userName');
    print('  - userEmail: $_userEmail');
    print('  - getUserName(): ${UserStorage.getUserName()}');
    print('  - getUserEmail(): ${UserStorage.getUserEmail()}');

    return Drawer(
      child: ListView(
        padding: EdgeInsets.zero,
        children: [
          UserAccountsDrawerHeader(
            accountName: Text(_userName),
            accountEmail: Text(_userEmail),
            currentAccountPicture: CircleAvatar(child: Text(userInitial)),
          ),
          ListTile(
            leading: const Icon(Icons.person),
            title: const Text('프로필'),
            onTap: () async {
              Navigator.of(context).pop(); // 드로워 닫기
              // 개인정보 수정 페이지로 이동하고 결과를 받아서 사용자 정보 갱신
              final result = await CustomNavigationUtil.to(
                context,
                const UserProfileEditView(),
              );
              // 개인정보 수정이 완료되면 사용자 정보를 다시 로드하여 drawer 갱신
              if (result == true) {
                _loadUserInfo();
                setState(() {
                  // drawer가 다시 빌드되도록 setState 호출
                });
              }
            },
          ),
          ListTile(
            leading: const Icon(Icons.shopping_cart),
            title: const Text('장바구니'),
            onTap: () {
              Navigator.of(context).pop(); // 드로워 닫기
              CustomNavigationUtil.toNamed(context, '/cart');
            },
          ),
          ListTile(
            leading: const Icon(Icons.history),
            title: const Text('주문 내역'),
            onTap: () {
              Navigator.of(context).pop(); // 드로워 닫기
              CustomNavigationUtil.to(context, const OrderListView());
            },
          ),
          ListTile(
            leading: const Icon(Icons.assignment_return),
            title: const Text('수령 / 반품 내역'),
            onTap: () {
              Navigator.of(context).pop(); // 드로워 닫기
              CustomNavigationUtil.to(context, const ReturnListView());
            },
          ),
          ListTile(
            leading: const Icon(Icons.add_box),
            title: const Text('배송지, 결제 방법 수정'),
            onTap: () {
              Navigator.of(context).pop(); // 드로워 닫기
              CustomNavigationUtil.to(context, const AddressPaymentView());
            },
          ),
          ListTile(
            leading: const Icon(Icons.logout),
            title: const Text('로그아웃'),
            onTap: () {
              Navigator.of(context).pop(); // 드로워 닫기
              // 로그아웃 확인 다이얼로그
              CustomDialog.show(
                context,
                title: '로그아웃',
                message: '정말 로그아웃하시겠습니까?',
                type: DialogType.dual,
                confirmText: '로그아웃',
                cancelText: '취소',
                onConfirm: () {
                  // 사용자 정보 삭제
                  UserStorage.clearUser();
                  // 로그인 화면으로 이동 (모든 페이지 제거)
                  CustomNavigationUtil.offAll(context, const LoginView());
                },
              );
            },
          ),

          ListTile(
            leading: const Icon(Icons.add_box),
            title: const Text('테스트 페이지로 이동'),
            onTap: () {
              Navigator.of(context).pop(); // 드로워 닫기
              CustomNavigationUtil.to(context, const TestNavigationPage());
            },
          ),
        ],
      ),
    );
  }
}

/*
// 테스트 페이지로 이동 버튼 (임시)
                      CustomButton(
                        btnText: '테스트 페이지로 이동',
                        buttonType: ButtonType.outlined,
                        onCallBack: _navigateToTestPage,
                        minimumSize: const Size(double.infinity, 56),
                      ),
*/
