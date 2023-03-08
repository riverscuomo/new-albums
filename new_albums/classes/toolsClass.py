
class toolsClass :

    def unique(list_of_elements):
        """
        This function remove duplicates in an array.
        """

        # Intilize a null list
        unique_list_of_elements = []

        # Traverse for all elements
        for x in list_of_elements:
            # Csheck if exists in unique_list or not
            if x not in unique_list_of_elements:
                unique_list_of_elements.append(x)
        return unique_list_of_elements

