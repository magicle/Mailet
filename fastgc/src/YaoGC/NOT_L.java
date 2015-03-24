// copyright belongs to shuai@cs.umn.edu
//


package YaoGC;

public class NOT_L extends Circuit {


  private int bitLength;

  public NOT_L(int l) {
    super(l, l, "NOT_L");
    bitLength = l;
    Circuit.counter_NOT = Circuit.counter_NOT + l;
  }

  public void build() throws Exception{
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
    for(int i = 0; i < outDegree; i++){
      if(inputWires[i].value != Wire.UNKNOWN_SIG) {
        outputWires[i].value = inputWires[i].value == 1? 0 : 1;
        outputWires[i].invd = inputWires[i].invd;
      }
      else {
          // set outputWire value to be Unknown. Or
          // the value will cause error in next usage
          // of this circuit...
        outputWires[i].value = Wire.UNKNOWN_SIG;
        outputWires[i].invd = ! inputWires[i].invd;
      }

      outputWires[i].setLabel(inputWires[i].lbl);
      outputWires[i].setReady();
    }
  }

    protected void compute()
    {}



}
