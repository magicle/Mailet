//  copyright belongs to shuai@cs.umn.edu
//  TEMP() implements the temp function in SHA1 design
//  
//  TEMP = S^5(A) + f(t;B,C,D) + E + W(t) + K(t)
//  input1: A
//  input2: f(t;B,C,D)
//  input3: E
//  input4: W(t)
//  input5: K(t)
//

package YaoGC.Mailet;
import YaoGC.*;


public class TEMP extends CompositeCircuit {
  public TEMP() {
    super(160, 32, 5, "TEMP");
  }
  
  protected void createSubCircuits() throws Exception {
    subCircuits[0] = new SHIFT_L(32, 5);
    for(int i = 0; i < 4; i++) {
      subCircuits[i+1] = new ADD_MOD_2L_L(32);
    }

    super.createSubCircuits();
  }

  protected void connectWires() {
    // gate 0
    for(int i = 0; i < 32; i++) {
      inputWires[i].connectTo(subCircuits[0].inputWires, i);
    }

    
    for(int i = 0; i < 32; i++) {
      // gate 1
      subCircuits[0].outputWires[i].connectTo(subCircuits[1].inputWires, i);
      inputWires[i+32].connectTo(subCircuits[1].inputWires, i+32);
      
      // gate 2
      subCircuits[1].outputWires[i].connectTo(subCircuits[2].inputWires, i);
      inputWires[i+64].connectTo(subCircuits[2].inputWires, i+32);

      // gate 3
      subCircuits[2].outputWires[i].connectTo(subCircuits[3].inputWires, i);
      inputWires[i+96].connectTo(subCircuits[3].inputWires, i+32);

      //gate 4
      subCircuits[3].outputWires[i].connectTo(subCircuits[4].inputWires, i);
      inputWires[i+128].connectTo(subCircuits[4].inputWires, i+32);
    }
  }

  protected void defineOutputWires() {
    for(int i = 0; i < 32; i++) {
      outputWires[i] = subCircuits[4].outputWires[i];
    }
  }


}
