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
        self._total -= num
        self._allocated -= num

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
        return (f'{type(self).__name__}(name={self.name}, manufacturer={self.manufacturer}), '
                f'total={self.total}, allocated={self.allocated}')


