# Packages
from typing import Union
from sqlalchemy.orm import Session
from fastapi.routing import APIRouter
from fastapi import Request, Depends, Response, Header, UploadFile


# Modules
from utils.helper import Helper
from models.products import ProductsModel
from db.postgres_db import get_db
from usecases.products import ProductsUsecase
from schemas.products import ProductsAddSchema, ProductsUpdateSchema


router = APIRouter(prefix="/products")


@router.get("/{product_id}")
def get_product_by_id(
    response: Response,
    product_id: int,
    db: Session = Depends(get_db),
    products_usecase: ProductsUsecase = Depends(ProductsUsecase),
):
    result = products_usecase.get_product_by_id(db, product_id, ProductsModel)
    response.status_code = result.http_code
    return result


@router.get("")
def list_products(
    response: Response,
    db: Session = Depends(get_db),
    limit: int = 10,
    skip: int = 0,
    product_usecase: ProductsUsecase = Depends(ProductsUsecase),
):
    result = product_usecase.list_products(db, ProductsModel, limit, skip)
    response.status_code = result.http_code
    return result


@router.post("")
def create_product(
    response: Response,
    product: ProductsAddSchema,
    db: Session = Depends(get_db),
    products_usecase: ProductsUsecase = Depends(ProductsUsecase),
):
    result = products_usecase.create_product(db, product, ProductsModel)
    response.status_code = result.http_code
    return result


@router.put("/{product_id}")
def update_product(
    response: Response,
    product_id: int,
    product: ProductsUpdateSchema,
    db: Session = Depends(get_db),
    products_usecase: ProductsUsecase = Depends(ProductsUsecase),
):
    result = products_usecase.update_product(
        db, product_id, product, ProductsModel
    )
    response.status_code = result.http_code
    return result


@router.delete("/{product_id}")
def delete_product(
    response: Response,
    product_id: int,
    db: Session = Depends(get_db),
    products_usecase: ProductsUsecase = Depends(ProductsUsecase),
):
    result = products_usecase.delete_product(
        db, product_id, ProductsModel
    )
    response.status_code = result.http_code
    return result


@router.post("/upload")
def upload_product_image(
    response: Response,
    file: UploadFile,
    products_usecase: ProductsUsecase = Depends(ProductsUsecase),
):
    result = products_usecase.upload_product_image(file)
    response.status_code = result.http_code
    return result
