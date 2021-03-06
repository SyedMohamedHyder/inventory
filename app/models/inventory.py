"""

Inventory of resources

"""

from app.utils.validators import validate_integer


class Resource:
    """

    Base class for resources

    """

    def __init__(self, name, manufacturer, total, allocated):
        """

        Args:
            name (str): Name of the resource
            manufacturer (str): Manufacturer of the resource
            total (int): Current total amount of resources
            allocated (int): Total amount of resources in-use

        Note:
            `allocated` should not exceed `total`
        """

        # Setting name and manufacturer to a private variable
        self._name = name
        self._manufacturer = manufacturer

        # Validation of total and allocated and if valid they are set to private variables
        validate_integer('total', total, 0)
        self._total = total

        validate_integer('allocated', allocated, 0, total,
                         custom_max_msg='Allocated cannot exceed the total resources available')
        self._allocated = allocated

    # Making name a read only property
    @property
    def name(self):
        """

        Returns:
            str : Name of the resource

        """
        return self._name

    # Making manufacturer a read only property
    @property
    def manufacturer(self):
        """

        Returns:
            str: Manufacturer of the resource

        """
        return self._manufacturer

    # Making total a read only property
    @property
    def total(self):
        """

        Returns:
            int: Total number of resources in the inventory

        """
        return self._total

    # Making allocated a read only property
    @property
    def allocated(self):
        """

        Returns:
            int: Total number of resources which are in-use

        """
        return self._allocated

    # Category is the type of the resource. If we have an instance of a subclass of the Resource class then the
    # category of that instance will be name of the subclass
    @property
    def category(self):
        """

        Returns:
            str: Category of the resource

        """
        return type(self).__name__.lower()

    # Calculated property available
    @property
    def available(self):
        """

        Returns:
            int: Total number of resources which are available (i.e resources not in use)

        """
        return self.total - self.allocated

    # Method which claims certain number of resources from the inventory
    def claim(self, num):
        """
        Claim `num` inventory items if available

        Args:
            num (int): Number of inventory items to claim

        Returns:

        """
        validate_integer('num', num, 1, self.available,
                         custom_max_msg='Number of resources claimed cannot exceed the number of available resources')
        self._allocated += num

    # Method to free-up the allocated resources
    def free_up(self, num):
        """
        Frees up `num` items from the allocated resources

        Args:
            num (int): Number of resources to be freed up (cannot exceed the number of allocated resources)

        Returns:

        """
        validate_integer('num', num, 1, self.allocated,
                         custom_max_msg=(f'Number of resources claimed for free up'
                                         f'cannot exceed the number of allocated resources')
                         )
        self._allocated -= num

    def died(self, num):
        """
        Removes `num` items from the inventory

        Args:
            num (int): Number of resources died which are to removed from the inventory

        Returns:

        """
        validate_integer('num', num, 1, self.allocated,
                         custom_max_msg=(f'Number of resources died'
                                         f'cannot exceed the number of allocated resources')
                         )
        self._allocated -= num
        self._total -= num

    def purchased(self, num):
        """
        Adds `num` items to the inventory

        Args:
            num (int): Number of resources purchased which is to be added to the inventory

        Returns:

        """
        validate_integer('num', num, 1)
        self._total += num

    def __str__(self):
        return self.name

    def __repr__(self):
        return (f'{type(self).__name__}(name={self.name}, manufacturer={self.manufacturer}, '
                f'total={self.total}, allocated={self.allocated})')


class CPU(Resource):
    """

    Subclass of Resource which tracks the resources related to CPUs

    """
    def __init__(self, name, manufacturer, total, allocated, cores, sockets, power_watts):
        """

        Args:
            name (str): Name of the resource
            manufacturer (str): Manufacturer of the resource
            total (int): Current total amount of resources
            allocated (int): Total amount of resources in-use
            cores (int): Number of cores in the CPU
            sockets (str): Name of the CPU socket
            power_watts (int): Power consumed by the CPU in watts

        Note:
            `allocated` should not exceed `total`

        """
        super().__init__(name, manufacturer, total, allocated)
        validate_integer('cores', cores, 1)
        validate_integer('power_watts', power_watts, 1)
        self._cores = cores
        self._sockets = sockets
        self._power_watts = power_watts

    @property
    def cores(self):
        """

        Returns:
            int : Cores available in the CPU

        """
        return self._cores

    @property
    def sockets(self):
        """

        Returns:
            str : Name of the CPU socket

        """
        return self._sockets

    @property
    def power_watts(self):
        """

        Returns:
            int : Power in watts consumed by the CPU

        """
        return self._power_watts

    def __repr__(self):
        return (f'{type(self).__name__}(name={self.name}, manufacturer={self.manufacturer}, '
                f'total={self.total}, allocated={self.allocated}, '
                f'cores={self.cores}, sockets={self.sockets}, power_watts={self.power_watts})')


class Storage(Resource):
    """

    Base class for all storage devices, inheriting from the Resource class

    """

    def __init__(self, name, manufacturer, total, allocated, capacity_gb):
        """

        Args:
            name (str): Name of the resource
            manufacturer (str): Manufacturer of the resource
            total (int): Current total amount of resources
            allocated (int): Total amount of resources in-use
            capacity_gb (int): Capacity of the storage resource in GigaBytes

        Note:
            `allocated` should not exceed `total`

        """
        super().__init__(name, manufacturer, total, allocated)

        validate_integer('capacity_gb', capacity_gb, 1)
        self._capacity_gb = capacity_gb

    @property
    def capacity_gb(self):
        """

        Returns:
            int : capacity of the storage resource in GigaBytes

        """
        return self._capacity_gb

    def __str__(self):
        return f'{self.category} : {self.capacity_gb} GB'

    def __repr__(self):
        return (f'{type(self).__name__}(name={self.name}, manufacturer={self.manufacturer}, '
                f'total={self.total}, allocated={self.allocated}, '
                f'capacity_gb={self.capacity_gb})')


class HDD(Storage):
    """

    Base class for all HDD storage resources which derives from the Storage class

    """

    def __init__(self, name, manufacturer, total, allocated, capacity_gb, size, rpm):
        """

        Args:
            name (str): Name of the resource
            manufacturer (str): Manufacturer of the resource
            total (int): Current total amount of resources
            allocated (int): Total amount of resources in-use
            capacity_gb (int): Capacity of the storage resource in GigaBytes
            size (str): Size of the HDD resource in inches (must be either 2.5" or 3.5")
            rpm (int): HDD spin speed (1000 to 50000 rpm)

        Note:
            `allocated` should not exceed `total`

        """
        super().__init__(name, manufacturer, total, allocated, capacity_gb)

        allowed_sizes = {'2.5"', '3.5"'}

        if size not in allowed_sizes:
            raise ValueError(f'Invalid HDD size. It must be one of {" ,".join(allowed_sizes)}')

        self._size = size

        validate_integer('rpm', rpm, 1_000, 50_000)
        self._rpm = rpm

    @property
    def size(self):
        """

        Returns:
            str : Size of the HDD resource in inches (must be either 2.5" or 3.5")

        """
        return self._size

    @property
    def rpm(self):
        """

        Returns:
            int : HDD spin speed (1000 to 50000 rpm)

        """
        return self._rpm

    def __repr__(self):
        return (f'{type(self).__name__}(name={self.name}, manufacturer={self.manufacturer}, '
                f'total={self.total}, allocated={self.allocated}, '
                f'capacity_gb={self.capacity_gb}, size={self.size}, rpm={self.rpm})')


class SSD(Storage):
    """

    Base class for all SSD storage resources which derives from the Storage class

    """

    def __init__(self, name, manufacturer, total, allocated, capacity_gb, interface):
        """

        Args:
            name (str): Name of the resource
            manufacturer (str): Manufacturer of the resource
            total (int): Current total amount of resources
            allocated (int): Total amount of resources in-use
            capacity_gb (int): Capacity of the storage resource in GigaBytes
            interface (str): Indicates the device interface (e.g. PCIe NVMe 3.0 x4)

        Note:
            `allocated` should not exceed `total`

        """
        super().__init__(name, manufacturer, total, allocated, capacity_gb)
        self._interface = interface

    @property
    def interface(self):
        """

        Returns:
            str : Indicates the device interface (e.g. PCIe NVMe 3.0 x4)

        """
        return self._interface

    def __repr__(self):
        return (f'{type(self).__name__}(name={self.name}, manufacturer={self.manufacturer}, '
                f'total={self.total}, allocated={self.allocated}, '
                f'capacity_gb={self.capacity_gb}, interface={self.interface})')
