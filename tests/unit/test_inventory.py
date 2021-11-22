"""

Unittests for the classes in app/models/inventory.py

"""

# All imports go here
import pytest
from app.models import inventory


@pytest.fixture
def resource_values():
    return dict(name='Zenbook15',
                manufacturer='Asus',
                total=10,
                allocated=5)


@pytest.fixture
def resource(resource_values):
    return inventory.Resource(**resource_values)


@pytest.fixture
def resource_readonly_props(resource_values):
    extra_props = {'category', 'available'}
    return resource_values.keys() | extra_props


class TestResource:
    """

    Tests for the resource class in app/models/inventory.py

    """

    def test_create_valid_resource(self, resource, resource_values):
        """

        Test for valid resource

        """
        for attr_name, attr_value in resource_values.items():
            assert getattr(resource, attr_name) == attr_value

    def test_invalid_total_type(self):
        """

        Test to check if `TypeError` is raised when an invalid type is passed as total to Resource

        """
        with pytest.raises(TypeError):
            inventory.Resource('Zenbook15', 'Asus', 10.5, 5)

    @pytest.mark.parametrize('total', (-1,))
    def test_invalid_total_value(self, total):
        """

        Test to check if `ValueError` is raised when invalid values are passed as total to Resource

        """
        with pytest.raises(ValueError):
            inventory.Resource('Zenbook15', 'Asus', total, 0)

    def test_invalid_allocated_type(self):
        """

        Test to check if 'TypeError' is raised when an invalid type is passed as allocated to Resource

        """
        with pytest.raises(TypeError):
            inventory.Resource('Zebook15', 'Asus', 10, 1.5)

    @pytest.mark.parametrize('total, allocated', [(10, -5), (10, 20)])
    def test_invalid_allocated_value(self, total, allocated):
        """

        Test to check if `ValueError` is raised when invalid values are passed as allocated to Resource

        """
        with pytest.raises(ValueError):
            inventory.Resource('Zenbook15', 'Asus', total, allocated)

    def test_name(self, resource):
        """

        Test to check the name property

        """
        assert resource.name == resource._name

    def test_manufacturer(self, resource):
        """

        Test to check the manufacturer property

        """
        assert resource.manufacturer == resource._manufacturer

    def test_total(self, resource):
        """

        Test to check the total property

        """
        assert resource.total == resource._total

    def test_allocated(self, resource):
        """

        Test to check the allocated property

        """
        assert resource.allocated == resource._allocated

    def test_category(self, resource):
        """

        Test to check the category property

        """
        assert resource.category == type(resource).__name__.lower()

    def test_available(self, resource):
        """

        Test to check the available property

        """
        assert resource.available == resource.total - resource.allocated

    def test_invalid_readonly_property_assignments(self, resource, resource_readonly_props):
        """

        Test to check if an `AttributeError` is raised when a value is set to read-only properties

        """
        with pytest.raises(AttributeError):
            for attr_name in resource_readonly_props:
                setattr(resource, attr_name, None)

    def test_str_repr(self, resource):
        """

        Test to check the __str__ of the Resource

        """
        assert str(resource) == resource.name

    def test_repr_repr(self, resource):
        """

        Test to check __repr__ of the Resource

        """
        assert repr(resource) == (f'Resource(name={resource.name}, manufacturer={resource.manufacturer}, '
                                  f'total={resource.total}, allocated={resource.allocated})')

    def test_claim(self, resource):
        """

        Test to check proper working of claim method

        """
        claim_num = 2
        original_total = resource.total
        original_allocated = resource.allocated
        original_available = resource.available
        resource.claim(claim_num)
        assert resource.total == original_total
        assert resource.allocated == original_allocated + claim_num
        assert resource.available == original_available - claim_num

    @pytest.mark.parametrize('claim_num', (0, -1, 6))
    def test_claim_invalid(self, claim_num, resource):
        """

        Test to check if `ValueError` is raised when an invalid number of resources is claimed

        """
        with pytest.raises(ValueError):
            resource.claim(claim_num)

    def test_freeup(self, resource):
        """

        Test to check proper working of free_up method

        """
        freeup_num = 2
        original_total = resource.total
        original_allocated = resource.allocated
        original_available = resource.available
        resource.free_up(freeup_num)
        assert resource.total == original_total
        assert resource.allocated == original_allocated - freeup_num
        assert resource.available == original_available + freeup_num

    @pytest.mark.parametrize('freeup_num', (0, -1, 6))
    def test_freeup_invalid(self, freeup_num, resource):
        """

        Test to check if `ValueError` is raised when an invalid number of resources is called to become free

        """
        with pytest.raises(ValueError):
            resource.free_up(freeup_num)

    def test_died(self, resource):
        """

        Test to check proper working of died method

        """
        died_num = 2
        original_total = resource.total
        original_allocated = resource.allocated
        original_available = resource.available
        resource.died(died_num)
        assert resource.total == original_total - died_num
        assert resource.allocated == original_allocated - died_num
        assert resource.available == original_available

    @pytest.mark.parametrize('died_num', (0, -1, 6))
    def test_died_invalid(self, died_num, resource):
        """

        Test to check if `ValueError` is raised when an invalid number of resources is said to be dead

        """
        with pytest.raises(ValueError):
            resource.died(died_num)

    def test_purchased(self, resource):
        """

        Test to check proper working of purchased method

        """
        purchased_num = 1000
        original_total = resource.total
        original_allocated = resource.allocated
        original_available = resource.available
        resource.purchased(purchased_num)
        assert resource.total == original_total + purchased_num
        assert resource.allocated == original_allocated
        assert resource.available == original_available + purchased_num

    @pytest.mark.parametrize('purchased_num', (0, -1))
    def test_purchased_invalid(self, purchased_num, resource):
        """

        Test to check if `ValueError` is raised when an invalid number of resources is said to be purchased

        """
        with pytest.raises(ValueError):
            resource.purchased(purchased_num)