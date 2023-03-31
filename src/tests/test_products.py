# Packages
import unittest
from unittest.mock import patch
from mock_alchemy.mocking import AlchemyMagicMock


# Modules
from models.products import ProductsModel
from usecases.products import ProductsUsecase
from schemas.products import ProductsAddSchema, ProductsUpdateSchema


class TestProducts(unittest.TestCase):
    _products_usecase = ProductsUsecase()

    def setUp(self) -> None:
        self._db = AlchemyMagicMock()

    @patch.object(ProductsUsecase, "_is_product_image_exists", return_value=True)
    def test_create_product_and_check_response_status(self, mock_image_exists):
        product = {
            "name": "Water Bottle",
            "description": "Water bottle for daily use",
            "color": "Black",
            "size": "1L",
            "image": "SpGrnP_requirements.txt",
            "price": 150
        }

        product_schema = ProductsAddSchema(**product)
        response = self._products_usecase.create_product(
            self._db, product_schema, ProductsModel,
        )
        self.assertTrue(response.status)

    def test_get_product_by_id_and_check_response_status(self):
        self._db.query(ProductsModel).filter(
            ProductsModel.id == 1).first.return_value = ProductsModel

        response = self._products_usecase.get_product_by_id(
            self._db, 1, ProductsModel)
        self.assertTrue(response.status)

    def test_get_list_products_check_empty_response(self):
        self._db.query(ProductsModel).offset(0).limit(10).all.return_value = []
        response = self._products_usecase.list_products(
            self._db, 1, ProductsModel)
        self.assertEqual([], response.data)

    def test_delete_product_and_check_product_not_exists_in_response_message(self):
        self._db.query(ProductsModel).filter(ProductsModel.id ==
                                             1).first.return_value = None
        response = self._products_usecase.delete_product(
            self._db, 1, ProductsModel)
        self.assertEqual("Product not exists", response.message)

    def test_update_product_and_check_response_data(self):
        product = {
            "name": "Water Bottle",
            "description": "Water bottle for daily use",
            "color": "Black",
            "size": "1L",
            "image": "SpGrnP_requirements.txt",
            "price": 200
        }
        product_schema = ProductsUpdateSchema(**product)
        self._db.query(ProductsModel).filter(
            ProductsModel.id == 1).first.return_value = ProductsModel(**product)

        response = self._products_usecase.update_product(
            self._db, 1, product_schema, ProductsModel
        )
        self.assertEqual(200, response.data.price)
