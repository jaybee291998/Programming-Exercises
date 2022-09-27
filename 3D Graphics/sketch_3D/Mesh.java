import java.util.ArrayList;

/**
	A mesh is just a collection of triangles
*/

public class Mesh
{
	private ArrayList<Triangle> mesh;

	public Mesh(ArrayList<Triangle> mesh)
	{
		this.mesh = new ArrayList<Triangle>(mesh);
	}

	/**
		Adds a triangle to the mesh
		@param triangle
	*/
	public void addTriangle(Triangle t)
	{
		mesh.add(t);
	}

  /**
    return all the trianglles
    @return mesh
  */
  public ArrayList<Triangle> getTriangles()
  {
    return mesh;  
  }

  /**
    return a string representation of the mesh
    @return str
  */
  public String toString()
  {
  	String str = "";
  	int i = 0;
  	for(Triangle t : mesh)
  	{
  		str += String.format("Tri %d:%s\n",i,t.toString());
  		i++;
  	}
  	return str;
  }
}
