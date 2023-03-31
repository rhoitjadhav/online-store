# Packages
import os
from typing import Type
from sqlalchemy.orm import Session
from fastapi import status, UploadFile

# Modules
from config import STATIC_FILES_PATH
from models.products import ProductsModel
from utils.helper import ReturnValue, Helper
from schemas.products import ProductsAddSchema, ProductsUpdateSchema


class ProductsUsecase:
    @staticmethod
    def _is_product_image_exists(product_image: str) -> bool:
        """Check if product image file exists in local storage

        Args:
            product_image: name of product image

        Returns:
            True if product image file exists otherwise False
        """
        file_path = os.path.join(STATIC_FILES_PATH, product_image)
        return os.path.exists(file_path)

    @staticmethod
    def get_product_by_id(
        db: Session,
        product_id: int,
        product_model: Type[ProductsModel]
    ) -> ReturnValue:
        """Get product details by id

        Args:
            db: sqlalchemy instance
            product_id: id of product
            product_model: ProductsModel instance

        Returns:
            products details
        """
        product = db.query(product_model).filter(
            product_model.id == product_id).first()

        if not product:
            return ReturnValue(False, status.HTTP_404_NOT_FOUND, "Product doesn't exists")

        return ReturnValue(True, status.HTTP_200_OK, message="Product found", data=product)

    @staticmethod
    def list_products(
        db: Session,
        product_model: Type[ProductsModel],
        limit: int = 10,
        skip: int = 0
    ) -> ReturnValue:
        """List details of products

        Args:
            db: sqlalchemy instance
            product_model: ProductsModel instance
            limit: number of rows to be fetched from database. Defaults to 10.
            skip: number of rows to be skipped. Defaults to 0.

        Returns:
            list of products
        """
        products = db.query(product_model).offset(skip).limit(limit).all()
        return ReturnValue(True, status.HTTP_200_OK, message="Products Fetched", data=products)

    @staticmethod
    def create_product(
        db: Session,
        product_schema: ProductsAddSchema,
        produt_model: Type[ProductsModel]
    ) -> ReturnValue:
        """Create product

        Args:
            db: sqlalchemy instance
            product_schema: product payload in schema format
            product_model: ProductsModel instance

        Returns:
            True if product created otherwise False
        """
        if not ProductsUsecase._is_product_image_exists(product_schema.image):
            return ReturnValue(
                False,
                status.HTTP_404_NOT_FOUND,
                "Product image doesn't exists, please upload first"
            )

        product = produt_model(**product_schema.dict())
        db.add(product)
        db.commit()
        db.refresh(product)
        return ReturnValue(
            True, status.HTTP_200_OK, "Product Added", data=product
        )

    @staticmethod
    def update_product(
        db: Session,
        product_id: int,
        product_schema: ProductsUpdateSchema,
        product_model: Type[ProductsModel]
    ) -> ReturnValue:
        """Update product details

        Args:
            db: sqlalchemy instance
            product_id: product id
            product_schema: product payload in schema format
            product_model: ProductsModel instance

        Returns:
            True if product is updated otherwise False
        """
        product = db.query(product_model).filter(
            product_model.id == product_id).first()

        if not product:
            return ReturnValue(False, status.HTTP_404_NOT_FOUND, "Product not exists")

        if not ProductsUsecase._is_product_image_exists(product_schema.image):
            return ReturnValue(
                False,
                status.HTTP_404_NOT_FOUND,
                "Product image doesn't exists, please upload first"
            )

        product.name = product_schema.name
        product.description = product_schema.description
        product.color = product_schema.color
        product.size = product_schema.size
        product.image = product_schema.image
        product.price = product_schema.price
        db.commit()

        return ReturnValue(True, status.HTTP_200_OK, "Product details updated", data=product_schema)

    @staticmethod
    def delete_product(
        db: Session,
        product_id: int,
        product_model: Type[ProductsModel]
    ) -> ReturnValue:
        """Delete product

        Args:
            db: sqlalchemy instance
            product_id: product id
            product_model: ProductsModel instance

        Returns:
            True if product is deleted otherwise False
        """
        product = db.query(product_model).filter(
            product_model.id == product_id).first()
        if not product:
            return ReturnValue(False, status.HTTP_404_NOT_FOUND, "Product not exists")

        db.delete(product)
        db.commit()
        return ReturnValue(True, status.HTTP_200_OK, "Product Deleted", data=product)

    @staticmethod
    def upload_product_image(
        file: UploadFile
    ) -> ReturnValue:
        """Upload product image

        Args:
            file: UploadFile instance

        Returns:
            True if file is saved
        """
        filename = f"{Helper.generate_random_text()}_{file.filename}"
        file_path = os.path.join(STATIC_FILES_PATH, filename)
        with open(file_path, "wb+") as fb:
            fb.write(file.file.read())

        return ReturnValue(True, status.HTTP_200_OK, "File Saved", data=filename)
