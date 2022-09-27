/**
	A method that represents a matrix
	it incudes method to do matrix calculations
*/

public class Matrix
{
	private double[][] matrix;
	private int row;
	private int col;
	/**
		A constructor that defines the matrix
		@param 2dArray the array that will be used to make the array
	*/
	public Matrix(double[][] array)
	{
		this.col = array[0].length;
		this.row = array.length;
		this.matrix = new double[this.row][this.col];
		for(int i = 0; i < this.row; i++)
		{
			for(int j = 0; j < this.col; j++)
			{
				this.matrix[i][j] = array[i][j];
			}
		}
	}

	/**
		A method that returns a copy of this matrix
		@return a copy of this matrix
	*/
	public Matrix copy()
	{
		Matrix copy = new Matrix(this.matrix);
		return copy;
	}

	/**
		A method that generates a random matrix based on a given dimension and range of value
		@param row
		@param col
		@param lower_bound
		@param upper_bound
		@return a matrix with random elements
	*/
	public static Matrix randMatrix(int row, int col, double lower_bound, double upper_bound)
	{
		double[][] randArray = new double[row][col];
		for(int i = 0; i < row; i++)
		{
			for(int j = 0; j < col; j++)
			{
				randArray[i][j] = Math.random() * (upper_bound - lower_bound) + lower_bound;
			}
		}
		Matrix randMatrix = new Matrix(randArray);
		return randMatrix;

	}

	/**	
		A method that generates a new matrix filled with a sigle value
		@param row
		@param col
		@param input 
		@return a matrix
	*/
	public static Matrix full(int row, int col, double input)
	{
		double[][] full_array = new double[row][col];
		for(int i = 0; i < row; i++)
		{
			for(int j = 0; j < col; j++)
			{
				full_array[i][j] = input;
			}
		}
		Matrix full_matrix = new Matrix(full_array);
		return full_matrix;
	}

	/**
		A method that prints the array
	*/
	public void print()
	{
		System.out.print("[");
		for(int i = 0; i < this.row; i++)
		{
			System.out.print(" [");
			for(int j = 0; j < this.col; j++)
			{
				System.out.print(this.matrix[i][j] + " ");
			}
			System.out.print("]");
			if(i < (this.row - 1)){ System.out.println(); }
		}
		System.out.println("]");
	}

	/**
		A method that gets a specific element in the matrix
		@param row
		@param col
		@return the element
	*/
	public double get(int row, int col)
	{
		return this.matrix[row][col];
	}

	/**
		sets the value of the index to the input
		@param row
		@param col
		@param val
	*/
	public void set(int row, int col, double val)
	{
		matrix[row][col] = val;
	}

	/**
		A method that returns the row of the matrix
		@return row
	*/
	public int getRow()
	{
		return this.row;
	}
	/**
		A method that returns the col of the matrix
		@return col
	*/
	public int getCol()
	{
		return this.col;
	}


	/**
		checks wether a given has the same dimension to our matrix
		@param m
		@return true or false
	*/
	public boolean equalDim(Matrix m)
	{
		if(this.row == m.getRow() && this.col == m.getCol())
		{
			return true;
		}
		else
		{
			System.out.println("Incompatible dimesnions: this matrix is (" + this.row + "x" + this.col + ") while input matrix is (" + m.getRow() + "x" + m.getCol() + ")" );
			return false;
		}
	}

	/**
		A method that does element wise addition with annother matrix
		@param m
	*/
	public void elwAdd(Matrix m)
	{
		if(equalDim(m))
		{
			for(int i = 0; i < this.row; i++)
			{
				for(int j = 0; j < this.col; j++)
				{
					this.matrix[i][j] += m.get(i, j);
				}
			}
		}
	}

	/**
		A method that does element wise subtraction with annother matrix
		@param m
	*/
	public void elwSub(Matrix m)
	{
		if(equalDim(m))
		{
			for(int i = 0; i < this.row; i++)
			{
				for(int j = 0; j < this.col; j++)
				{
					this.matrix[i][j] -= m.get(i, j);
				}
			}
		}
	}

	/**
		A method that does element wise multiplication with annother matrix
		@param m
	*/
	public void elwMul(Matrix m)
	{
		if(equalDim(m))
		{
			for(int i = 0; i < this.row; i++)
			{
				for(int j = 0; j < this.col; j++)
				{
					this.matrix[i][j] *= m.get(i, j);
				}
			}
		}
	}

	/**
		A method that does element wise division with annother matrix
		@param m
	*/
	public void elwDiv(Matrix m)
	{
		if(equalDim(m))
		{
			for(int i = 0; i < this.row; i++)
			{
				for(int j = 0; j < this.col; j++)
				{
					this.matrix[i][j] /= m.get(i, j);
				}
			}
		}
	}

	/**
		A method that use the elements of the matrix as an exponent to an scalar base
		@param m
	*/
	public void elwExp(double scalar)
	{
		for(int i = 0; i < this.row; i++)
		{
			for(int j = 0; j < this.col; j++)
			{
				this.matrix[i][j] = Math.pow(scalar, this.matrix[i][j]);
			}
		}
	}

	/**
		A method that does scalar addition with the matrix
		@param m
	*/
	public void sclAdd(double scalar)
	{
		for(int i = 0; i < this.row; i++)
		{
			for(int j = 0; j < this.col; j++)
			{
				this.matrix[i][j] += scalar;
			}
		}
	}

	/**
		A method that does scalar subtraction with the matrix
		@param m
	*/
	public void sclSub(double scalar)
	{
		for(int i = 0; i < this.row; i++)
		{
			for(int j = 0; j < this.col; j++)
			{
				this.matrix[i][j] -= scalar;
			}
		}
	}

	/**
		A method that does scalar multiplication with the matrix
		@param m
	*/
	public void sclMul(double scalar)
	{
		for(int i = 0; i < this.row; i++)
		{
			for(int j = 0; j < this.col; j++)
			{
				this.matrix[i][j] *= scalar;
			}
		}
	}

	/**
		A method that does scalar division with the matrix
		@param m
	*/
	public void sclDiv(double scalar)
	{
		for(int i = 0; i < this.row; i++)
		{
			for(int j = 0; j < this.col; j++)
			{
				this.matrix[i][j] /= scalar;
			}
		}
	}

	/**
		A method that does scalar exponentiation with the matrix
		@param m
	*/
	public void sclExp(double scalar)
	{
		for(int i = 0; i < this.row; i++)
		{
			for(int j = 0; j < this.col; j++)
			{
				this.matrix[i][j] = Math.pow(this.matrix[i][j], scalar);
			}
		}
	}



	/**
		a method that does the matrix multipliaction with the input array
		@param m
	*/
	public static Matrix matMul(Matrix m1, Matrix m2)
	{	
		int row = m1.getRow();
		int col = m2.getCol();
		double[][] array = new double[row][col];
		for(int i = 0; i < row; i++)
		{
			for(int j = 0; j < col; j++)
			{
				array[i][j] = vecDot(getRowVec(m1, i), getColVec(m2, j));
			}
		}
		Matrix m = new Matrix(array);
		return m;
	}

	/**
		A method that calculates the dot product of two vectors
		@param v1
		@param v2
		@return the dot product of 2 vectors
	*/
	public static double vecDot(double[] v1, double[] v2)
	{
		double dot = 0;
		if(v1.length == v2.length)
		{
			for(int i = 0; i < v1.length; i++)
			{
				dot += v1[i] * v2[i];
			}
		}
		else
		{
			System.out.println("Incompatible vector lengths");
		}
		return dot;
	}


	/**
		A method that returns a array from a row in a given matrix
		@param m
		@param row_index
		@return a vector that conatains all the elements in the matrix m at a given row 
	*/
	public static double[] getRowVec(Matrix m, int row_index)
	{
		int col = m.getCol();
		double[] vector = new double[col];
		for(int i = 0; i < col; i++)
		{
			vector[i] = m.get(row_index, i);
		}

		return vector;
	}

	/**
		A method that returns an array that contains all the elements in the the given col of the given matrix
		@param m
		@param col_index
		@return a vector that conatains all the elements in the matrix m at a given row 
	*/
	public static double[] getColVec(Matrix m, int col_index)
	{
		int row = m.getRow();
		double[] vector = new double[row];
		for(int i = 0; i < row; i++)
		{
			vector[i] = m.get(i, col_index);
		}

		return vector;
	}

	/**
		A method that transpose a given matrix
		@param m
		@return the tranposed matrix
	*/
	public static Matrix transpose(Matrix m)
	{
		int new_row = m.getCol();
		int new_col = m.getRow();
		double[][] array = new double[new_row][new_col];
		for(int i = 0; i < new_row; i++)
		{
			array[i] = getColVec(m, i);
		}

		Matrix transposed_matrix = new Matrix(array);
		return transposed_matrix;
	}



}

/**
	Basic loop
for(int i = 0; i < this.row; i++)
{
	for(int j = 0; j < this.col; j++)
	{

	}
}
*/