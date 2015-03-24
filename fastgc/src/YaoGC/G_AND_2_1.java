// Copyright (C) 2010 by Yan Huang <yhuang@virginia.edu>

package YaoGC;
import java.io.FileNotFoundException;

class G_AND_2_1 extends AND_2_1 {
    public G_AND_2_1() {
	super();
    }

    protected void execYao() {
	try {
    fillTruthTable();
  } catch (FileNotFoundException e){
    System.out.println("Error in fileTruthTable");
  }

	encryptTruthTable();
  sendGTT();
	gtt = null;
    }
}
