

class BaseDb:
    """
    Each database used will extend this class
    """

    def get(self, date):
        """
        Get task execution information for a specific date
        :param date:
        :return: dictionnary with the tasks details
        """
        raise NotImplementedError("DB Should implement get method")

    def insert(self, document):
        """
        Insert a task execution
        :param document:
        :return:
        """
        raise NotImplementedError("DB Should implement insert method")

    def update(self, date, new_data):
        """
        Update a task execution
        :param date: To identify which document we wish to update
        :param new_data: The data to update
        :return:
        """
        raise NotImplementedError("DB Should implement update method")
