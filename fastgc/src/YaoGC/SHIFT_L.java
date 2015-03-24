// copyright belongs to shuai@cs.umn.edu


package YaoGC;

public class SHIFT_L extends Circuit {

  private int shift;

  public SHIFT_L(int length, int l) {
    super(length, length, "SHIFT");
    shift = l;
    Circuit.counter_shift++;
  }

  public void build() throws Exception {
    createInputWires();
    createOutputWires();
  }

  protected void createInputWires() {
    super.createInputWires();

    for(int i = 0; i < inDegree; i++) {
      inputWires[i].addObserver(this, new TransitiveObservable.Socket(inputWires, i));
    }

  }

  protected void createOutputWires() {
    for(int i = 0; i < outDegree; i++) {
      outputWires[i] = new Wire();
    }
  }

  protected void execute() {
  
    int idx;
    for(int i = 0; i < outDegree; i++) {
      idx = (i + shift) % outDegree;
      outputWires[i].value = inputWires[idx].value;
      outputWires[i].invd = inputWires[idx].invd;
      outputWires[i].setLabel(inputWires[idx].lbl);
      outputWires[i].setReady();
    }

  }
  protected void compute() 
  {}


}
