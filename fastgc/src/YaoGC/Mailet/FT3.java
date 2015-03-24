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

public class FT3 extends CompositeCircuit {
  public FT3() {
    super(96, 32, 5, "FT3");
  }

  protected void createSubCircuits() throws Exception{
    subCircuits[0] = new AND_2L_L(32);
    subCircuits[1] = new AND_2L_L(32);
    subCircuits[2] = new OR_2L_L(32);
    subCircuits[3] = new AND_2L_L(32);
    subCircuits[4] = new OR_2L_L(32);

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
      inputWires[i].connectTo(subCircuits[3].inputWires, i-32);
    }

    // deal with D
    for(int i = 64; i < 96; i++) {
      inputWires[i].connectTo(subCircuits[1].inputWires, i-32);
      inputWires[i].connectTo(subCircuits[3].inputWires, i-32);
    }

    // deal with 1st OR gate 
    for(int i = 0; i < 32; i++) {
      subCircuits[0].outputWires[i].connectTo(subCircuits[2].inputWires, i);
      subCircuits[1].outputWires[i].connectTo(subCircuits[2].inputWires, i+32);
    }


    // deal with 2nd OR gate
    for(int i = 0; i < 32; i++) {
      subCircuits[2].outputWires[i].connectTo(subCircuits[4].inputWires, i);
      subCircuits[3].outputWires[i].connectTo(subCircuits[4].inputWires, i+32);
    }

  }
  
  protected void defineOutputWires() {
    for(int i = 0; i < outDegree; i++) {
      outputWires[i] = subCircuits[4].outputWires[i];
    }
  }




}
