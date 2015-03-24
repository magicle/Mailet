// copyrights belong to shuai@cs.umn.edu
//
// WT.java implements w(t) functions in sha1 generation

// Circuit outline
//
//     SHIFT
//       L
//      L L
//      | 4
//      L
//     L L
//     | 3
//     L
//    L L
//    1 2
//
//



package YaoGC.Mailet;

import YaoGC.*;


public class WT extends CompositeCircuit {

  public WT() {
    super(128, 32, 4, "WT");
  }

  protected void createSubCircuits() throws Exception {
    
    // create subcircuits for 4 Bitwise Xor
    for(int i = 0; i < 3; i++) {
      subCircuits[i] = new XOR_2L_L(32);
    }

    // create subcircuit for one shift operation
    subCircuits[3] = new SHIFT_L(32, 1);
    super.createSubCircuits();
  }

  protected void connectWires() {
    // input: 1
    for(int j = 0; j < 32; j++) {
      inputWires[j].connectTo(subCircuits[0].inputWires, j);
    }

    // input: 2,3,4
    for(int i  = 0; i < 3; i++) {
      for(int j = 0; j < 32; j++) {
      inputWires[32*(i+1) + j].connectTo(subCircuits[i].inputWires, 32+j);
      }
    }

    // gate0/1 <-> gate1/2
    for(int i = 1; i < 3; i++) {
      for(int j = 0; j < 32; j++) {
        subCircuits[i-1].outputWires[j].connectTo(subCircuits[i].inputWires, j);
      }
    }

    // shift function
    for(int j = 0; j < 32; j++) {
      subCircuits[2].outputWires[j].connectTo(subCircuits[3].inputWires, j);
    }
  }





  protected void defineOutputWires() {
    for(int j = 0; j < 32; j++) {
      outputWires[j] = subCircuits[3].outputWires[j];
    }
  }





}
