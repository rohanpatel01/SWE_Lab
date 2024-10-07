class HardwareSet:
    def __init__(self, name=None, capacity=-1):

        self.name = name if name else ""
        
        self.__Capacity = capacity if capacity >= 0 else -1
        self.initialize_capacity()
        self.__Availability = 0       # number of units available to check out
        self.__CheckedOut = []          # List containing checkedout quantities. projectID = index of the array

    def initialize_capacity(self, qty):
        self.__Capacity = qty
        self.__Availability = qty

    def get_availability(self):
        return self.__Availability

    def get_capacity(self):
        return self.__Capacity

    def check_out(self, qty, projectID):

        if projectID < 0: 
            return -1       # invalid projectID

        # add more projectIDs to get the index they want
        while (len(self.__CheckedOut) <= projectID):
            self.__CheckedOut.append(0)

        if self.__Availability <= 0:
            return -1

        # check out the amount they want
        # handle case where they want more 
        if self.__Availability < qty:
            self.__CheckedOut[projectID] += self.__Availability
            self.__Availability = 0
            return -1                               # -1 since they checked out everything
        else:
            self.__Availability -= qty
            self.__CheckedOut[projectID] += qty
            return 0
        

    def check_in(self, qty, projectID):

        # add more projectIDs to get the index they want
        while (len(self.__CheckedOut) <= projectID):
            self.__CheckedOut.append(0)
        
        # don't allow them to check in more than they have checked out
        if self.__CheckedOut[projectID] < qty:
            return -1
        
        # process correct checkout
        self.__Availability += qty
        self.__CheckedOut[projectID] -= qty
        return 0
