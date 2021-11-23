"""

Unittests for the classes in app/models/inventory.py

"""

# All imports go here
import pytest
from app.models import inventory


# Fixtures for Resource class
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


# Fixtures for CPU class
@pytest.fixture
def cpu_values():
    return dict(
        name='Intel Core i7',
        manufacturer='Intel',
        total=10,
        allocated=5,
        cores=7,
        sockets='10 Gen',
        power_watts=5
    )


@pytest.fixture
def cpu(cpu_values):
    return inventory.CPU(**cpu_values)


@pytest.fixture
def cpu_readonly_props(resource_readonly_props, cpu_values):
    return resource_readonly_props | cpu_values.keys()


# Fixtures for the Storage class
@pytest.fixture
def storage_values(resource_values):
    extra_values = dict(capacity_gb=1)
    return dict(**resource_values, **extra_values)


@pytest.fixture
def storage(storage_values):
    return inventory.Storage(**storage_values)


class TestResource:
    """

    Tests for the Resource class in app/models/inventory.py

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
        for attr_name in resource_readonly_props:
            with pytest.raises(AttributeError):
                setattr(resource, attr_name, None)

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


class TestCPU:
    """

    Tests for the CPU class in app/models/inventory.py

    """

    def test_create_valid_cpu(self, cpu_values, cpu):
        """

        Test for a valid CPU

        """
        for attr_name, attr_value in cpu_values.items():
            assert getattr(cpu, attr_name) == attr_value

    def test_invalid_cores_type(self, cpu_values):
        """

        Test to check if `TypeError` is raised when an invalid type is passed as cores to CPU

        """
        cpu_values['cores'] = 10.5
        with pytest.raises(TypeError):
            inventory.CPU(**cpu_values)

    @pytest.mark.parametrize('cores', (0, -1))
    def test_invalid_cores_value(self, cores, cpu_values):
        """

        Test to check if a `ValueError` is raised when an invalid number of cores is passed to CPU

        """
        cpu_values['cores'] = cores
        with pytest.raises(ValueError):
            inventory.CPU(**cpu_values)

    def test_invalid_power_watts_type(self, cpu_values):
        """

        Test to check if `TypeError` is raised when an invalid type is passed as power_watts to CPU

        """
        cpu_values['power_watts'] = 10.5
        with pytest.raises(TypeError):
            inventory.CPU(**cpu_values)

    @pytest.mark.parametrize('power_watts', (0, -1))
    def test_invalid_power_watts_value(self, power_watts, cpu_values):
        """

        Test to check if a `ValueError` is raised when an invalid number of power_watts is passed to CPU

        """
        cpu_values['power_watts'] = power_watts
        with pytest.raises(ValueError):
            inventory.CPU(**cpu_values)

    def test_cores_property(self, cpu):
        """

        Test to check the cores property

        """
        assert cpu.cores == cpu._cores

    def test_sockets_property(self, cpu):
        """

        Test to check the sockets property

        """
        assert cpu.sockets == cpu._sockets

    def test_power_watts_property(self, cpu):
        """

        Test to check the power_watts property

        """
        assert cpu.power_watts == cpu._power_watts

    def test_invalid_readonly_prop_assignments(self, cpu, cpu_readonly_props):
        """

        Tests if an `AttributeError` is raised when a value is assigned to a read-only property

        """
        for readonly_prop in cpu_readonly_props:
            with pytest.raises(AttributeError):
                setattr(cpu, readonly_prop, None)

    def test_repr_repr(self, cpu):
        """

        Test to check __repr__ of the Resource

        """
        assert repr(cpu) == (f'CPU(name={cpu.name}, manufacturer={cpu.manufacturer}, '
                             f'total={cpu.total}, allocated={cpu.allocated}, '
                             f'cores={cpu.cores}, sockets={cpu.sockets}, power_watts={cpu.power_watts})')


class TestStorage:
    """

    Test for Storage class in app/models/inventory.py

    """

    def test_create_storage(self, storage, storage_values):
        """

        Test to check a valid Storage

        """
        for attr_name, attr_value in storage_values.items():
            assert getattr(storage, attr_name) == attr_value

    @pytest.mark.parametrize('capacity_gb, exception',
                             [(1.5, TypeError), (0, ValueError), (-1, ValueError)])
    def test_invalid_capacity_gb(self, capacity_gb, exception, storage_values):
        """

        Test to check if proper exception is raised when invalid values are passed as capacity_gb to Storage

        """
        storage_values['capacity_gb'] = capacity_gb
        with pytest.raises(exception):
            inventory.Storage(**storage_values)

    def test_capacity_gb_prop(self, storage):
        """

        Test to check the capacity_gb property

        """
        assert storage.capacity_gb == storage._capacity_gb

    def test_invalid_readonly_prop_assignments(self, storage, storage_values):
        """

        Tests if an `AttributeError` is raised when a value is assigned to a read-only property

        """
        for readonly_prop in storage_values:
            with pytest.raises(AttributeError):
                setattr(storage, readonly_prop, None)

    def test_str_repr(self, storage):
        """

        Test to check __str__ of Storage class

        """
        assert str(storage) == f'storage : {storage.capacity_gb} GB'

    def test_repr_repr(self, storage):
        """

        Test to check __repr__ of Storage class

        """
        assert repr(storage) == (f'Storage(name={storage.name}, manufacturer={storage.manufacturer}, '
                                 f'total={storage.total}, allocated={storage.allocated}, '
                                 f'capacity_gb={storage.capacity_gb})')