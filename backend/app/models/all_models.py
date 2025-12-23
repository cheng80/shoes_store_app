"""
모든 모델 정의 (간단한 버전)
Flutter 모델과 호환되도록 필드명 그대로 사용
"""

from pydantic import BaseModel
from typing import Optional


# ============================================
# Customer
# ============================================
class Customer(BaseModel):
    id: Optional[int] = None
    cEmail: str
    cPhoneNumber: str
    cName: str
    cPassword: str


# ============================================
# Employee
# ============================================
class Employee(BaseModel):
    id: Optional[int] = None
    eEmail: str
    ePhoneNumber: str
    eName: str
    ePassword: str
    eRole: str


# ============================================
# Manufacturer
# ============================================
class Manufacturer(BaseModel):
    id: Optional[int] = None
    mName: str


# ============================================
# ProductBase
# ============================================
class ProductBase(BaseModel):
    id: Optional[int] = None
    pName: str
    pDescription: str
    pColor: str
    pGender: str
    pStatus: str
    pCategory: str
    pModelNumber: str


# ============================================
# ProductImage
# ============================================
class ProductImage(BaseModel):
    id: Optional[int] = None
    pbid: Optional[int] = None
    imagePath: str


# ============================================
# Product
# ============================================
class Product(BaseModel):
    id: Optional[int] = None
    pbid: Optional[int] = None
    mfid: Optional[int] = None
    size: int
    basePrice: int
    pQuantity: int


# ============================================
# Purchase
# ============================================
class Purchase(BaseModel):
    id: Optional[int] = None
    cid: Optional[int] = None
    pickupDate: str
    orderCode: str
    timeStamp: str


# ============================================
# PurchaseItem
# ============================================
class PurchaseItem(BaseModel):
    id: Optional[int] = None
    pid: int
    pcid: int
    pcQuantity: int
    pcStatus: str


# ============================================
# LoginHistory
# ============================================
class LoginHistory(BaseModel):
    id: Optional[int] = None
    cid: Optional[int] = None
    loginTime: str
    lStatus: str
    lVersion: float
    lAddress: str
    lPaymentMethod: str

