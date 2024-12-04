class Field:
    def is_empty(self):
        return True
    
    def is_white(self):
        return False

    def is_black(self):
        return False
    
    def __str__(self):
        return "."
    

class Pawn(Field):    
    def __init__(self, is_white, row, col):
        self.__is_white=is_white
        self.row = row
        self.col = col
        
    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        result.__dict__.update(self.__dict__)
        return result  

    def __str__(self):
        if self.is_white():
            return "w"
        return "b"
            
    def is_king(self):
        return False
    
    def is_empty(self):
        return False
    
    def is_white(self):
        return self.__is_white

    def is_black(self):
        return not self.__is_white
    

class King(Pawn):    
    def __init__(self, pawn):
        super().__init__(pawn.is_white(), pawn.row, pawn.col)

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        result.__dict__.update(self.__dict__)
        return result  
    
    def is_king(self):
        return True

    def __str__(self):
        if self.is_white():
            return "W"
        return "B"