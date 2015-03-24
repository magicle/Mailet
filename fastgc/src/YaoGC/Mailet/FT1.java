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

public class FT1 extends CompositeCircuit {
  public FT1() {
    super(96, 32, 4, "FT1");
  }

  protected void createSubCircuits() throws Exception{
    subCircuits[0] = new AND_2L_L(32);
    subCircuits[1] = new NOT_L(32);
    subCircuits[2] = new AND_2L_L(32);
    subCircuits[3] = new OR_2L_L(32);

    super.createSubCircuits();
  }

  protected void connectWires() {
    
    // deal with B
    for(int i = 0; i < 32; i++) {
      inputWires[i].connectTo(subCircuits[0].inputWires, i);
      inputWires[i].connectTo(subCircuits[1].inputWires, i);
    }

    // deal with C
    for(int i = 32; i < 64; i++) {
      inputWires[i].connectTo(subCircuits[0].inputWires, i);
    }

    // deal with D
    for(int i = 0; i < 32; i++) {
      inputWires[64+i].connectTo(subCircuits[2].inputWires, 32+i);
    }

    // deal with NOT B
    for(int i = 0; i < 32; i++) {
      subCircuits[1].outputWires[i].connectTo(subCircuits[2].inputWires, i);
    }

    // deal with OR gate
    for(int i = 0; i < 32; i++) {
      subCircuits[0].outputWires[i].connectTo(subCircuits[3].inputWires, i);
      subCircuits[2].outputWires[i].connectTo(subCircuits[3].inputWires, i+32);
    }

  }
  
  protected void defineOutputWires() {
    for(int i = 0; i < outDegree; i++) {
      outputWires[i] = subCircuits[3].outputWires[i];
    }
  }




}
