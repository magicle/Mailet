// copyright bellongs to shuai@cs.umn.edu
// 
// FT1 implements f(t,B,C,D) function for sha1 generation
//
//
//
//
//
package YaoGC.Mailet;
import YaoGC.*;

public class FT4 extends CompositeCircuit {
  public FT4() {
    super(96, 32, 2, "FT4");
  }

  protected void createSubCircuits() throws Exception{
    subCircuits[0] = new XOR_2L_L(32);
    subCircuits[1] = new XOR_2L_L(32);

    super.createSubCircuits();
  }

  protected void connectWires() {
    
    // deal with 1st XOR gate 
    for(int i = 0; i < 64; i++) {
      inputWires[i].connectTo(subCircuits[0].inputWires, i);
    }

    // deal with 2nd XOR gate 
    for(int i = 0; i < 32; i++) {
      subCircuits[0].outputWires[i].connectTo(subCircuits[1].inputWires, i);
    }

    for(int i = 32; i < 64; i++) {
      inputWires[32+i].connectTo(subCircuits[1].inputWires, i);
    }

  }
  
  protected void defineOutputWires() {
    for(int i = 0; i < outDegree; i++) {
      outputWires[i] = subCircuits[1].outputWires[i];
    }
  }




}
