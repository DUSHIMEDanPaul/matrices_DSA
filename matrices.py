import re

class SparseMatrix:
    def __init__(self, matrixFilePath=None, numRows=0, numCols=0):
        self.numRows = numRows
        self.numCols = numCols
        self.elements = {}
        if matrixFilePath:
            self.load_from_file(matrixFilePath)
    
    def load_from_file(self, matrixFilePath):
        try:
            with open(matrixFilePath, 'r') as file:
                lines = file.readlines()
                
                # Extract matrix dimensions
                rows_line = lines[0].strip()
                cols_line = lines[1].strip()
                self.numRows = int(rows_line.split('=')[1])
                self.numCols = int(cols_line.split('=')[1])
                
                # Parse each line to get matrix elements
                for line in lines[2:]:
                    line = line.strip()
                    if not line:  # Skip empty lines
                        continue
                    match = re.match(r'\((\d+),\s*(\d+),\s*(-?\d+)\)', line)
                    if not match:
                        raise ValueError("Input file has wrong format")
                    row, col, value = map(int, match.groups())
                    self.setElement(row, col, value)
        except Exception as e:
            raise ValueError(f"Error reading matrix file: {str(e)}")
    
    def getElement(self, currRow, currCol):
        return self.elements.get((currRow, currCol), 0)
    
    def setElement(self, currRow, currCol, value):
        if value != 0:
            self.elements[(currRow, currCol)] = value
        elif (currRow, currCol) in self.elements:
            del self.elements[(currRow, currCol)]  # Remove if value is zero to maintain sparsity
    
    def add(self, other):
        if self.numRows != other.numRows or self.numCols != other.numCols:
            raise ValueError("Matrices must have the same dimensions for addition")
        
        result = SparseMatrix(numRows=self.numRows, numCols=self.numCols)
        
        # Add elements from both matrices
        for (row, col), value in self.elements.items():
            result.setElement(row, col, value + other.getElement(row, col))
        
        for (row, col), value in other.elements.items():
            if (row, col) not in self.elements:
                result.setElement(row, col, value)
        
        return result
    
    def subtract(self, other):
        if self.numRows != other.numRows or self.numCols != other.numCols:
            raise ValueError("Matrices must have the same dimensions for subtraction")
        
        result = SparseMatrix(numRows=self.numRows, numCols=self.numCols)
        
        # Subtract elements from both matrices
        for (row, col), value in self.elements.items():
            result.setElement(row, col, value - other.getElement(row, col))
        
        for (row, col), value in other.elements.items():
            if (row, col) not in self.elements:
                result.setElement(row, col, -value)
        
        return result
    
    def multiply(self, other):
        if self.numCols != other.numRows:
            raise ValueError("Matrix multiplication is not possible. Columns of first must equal rows of second")
        
        result = SparseMatrix(numRows=self.numRows, numCols=other.numCols)
        
        # Perform multiplication by computing dot product
        for (row1, col1), value1 in self.elements.items():
            for col2 in range(other.numCols):
                value2 = other.getElement(col1, col2)
                if value2 != 0:
                    result.setElement(row1, col2, result.getElement(row1, col2) + value1 * value2)
        
        return result


def main():
    # Load two sparse matrices from files
    matrix1 = SparseMatrix(matrixFilePath='DSA//small_sample_input_02.txt')
    matrix2 = SparseMatrix(matrixFilePath='DSA/small_sample_input_03.txt')
    
    # Get user input to choose operation
    operation = input("Choose operation: add, subtract, multiply: ").strip().lower()
    
    if operation == 'add':
        result = matrix1.add(matrix2)
    elif operation == 'subtract':
        result = matrix1.subtract(matrix2)
    elif operation == 'multiply':
        result = matrix1.multiply(matrix2)
    else:
        print("Invalid operation")
        return
    
    # Output result matrix (in sparse format)
    for (row, col), value in result.elements.items():
        print(f"({row}, {col}, {value})")


if __name__ == "__main__":
    main()
