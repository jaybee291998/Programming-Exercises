/**
	A class that contains 3 points that represents the triangle
*/

public class Triangle
{
	private Point a;
	private Point b;
	private Point c;
	public Triangle(Point a, Point b, Point c)
	{
		this.a = a;
		this.b = b;
		this.c = c;
	}

  /**
    return an array of matrix
    @return array
  */
  public Matrix[] getPoints()
  {
    Matrix[] points = {a.getVec(), b.getVec(), c.getVec()};
    return points;
  }

	/**
		get the matrix form the triagle
	*/

	/**
		return a string representaion of the triangle
		@return str
	*/
	public String toString()
	{
		return "[a: " + a + " b: " + b + " c: " + c + "]";
	}
}
