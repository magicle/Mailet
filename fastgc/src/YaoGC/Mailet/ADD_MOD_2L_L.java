// Copyright belongs to shuai@cs.umn.edu
//
//  addition module 2^L
//  input1: l1 l2 l3 l4 ... (0~L-1)
//  input2: L1 L2 L3 L4 ... (L~2L-1)
//  output: result (L)
//

package YaoGC.Mailet;
import YaoGC.*;




public class ADD_MOD_2L_L extends CompositeCircuit {
    private final int L;

    public ADD_MOD_2L_L(int l) {
	super(2*l, l, l, "ADD_MOD_" + 2*l + "_" + l);
	
	L = l;
    }

    protected void createSubCircuits() throws Exception {
	for (int i = 0; i < L; i++) 
	    subCircuits[i] = new ADD_3_2();

	super.createSubCircuits();
    }

    protected void connectWires() {
	inputWires[X(0)].connectTo(subCircuits[0].inputWires, ADD_3_2.X);
	inputWires[Y(0)].connectTo(subCircuits[0].inputWires, ADD_3_2.Y);
	
	for (int i = 1; i < L; i++) {
	    inputWires[X(i)].connectTo(subCircuits[i].inputWires, ADD_3_2.X);
	    inputWires[Y(i)].connectTo(subCircuits[i].inputWires, ADD_3_2.Y);
	    subCircuits[i-1].outputWires[ADD_3_2.COUT].connectTo(subCircuits[i].inputWires,
								 ADD_3_2.CIN);
	}
    }

    protected void defineOutputWires() {
	for (int i = 0; i < L; i++)
	    outputWires[L-1-i] = subCircuits[i].outputWires[ADD_3_2.S];
    }

    protected void fixInternalWires() {
    	Wire internalWire = subCircuits[0].inputWires[ADD_3_2.CIN];
    	internalWire.fixWire(0);
    }

    private int X(int i) {
	return L-1-i;
    }

    private int Y(int i) {
	return 2*L-1-i;
    }
}
