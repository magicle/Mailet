// Copyright by shuai@cs.umn.edu
//

package Program;

import java.math.*;


import java.io.OutputStream;
import java.io.FileOutputStream;






import YaoGC.*;
import Utils.*;


public class MailetClient extends ProgClient {

  private short[] msg;    // message of m_1 (msg2)  password|pad
  private BigInteger m;   // BigInteger version of msg2
  private short[] key;    // key for HMAC
  private BigInteger k;   // BigInteger version of key

  private short[] http;
  private BigInteger Http;



  private int bitLengthS;   
  private int bitLengthC;

  private BigInteger[] msg1Lab, msg2Lab, keyLab, keyMsg2Lab;




  private State outputState;
  public MailetClient(short[] msgIn, short[] keyIn, int length, short[] constIn) {
    msg = msgIn;
    key = keyIn;
    http = constIn;
    bitLengthC = length;
    
    m = MailetCommon.array2Biginteger(msg, bitLengthC);
    k = MailetCommon.array2Biginteger(key, MailetCommon.keyLength);
    Http = MailetCommon.array2Biginteger(http, http.length*8);
  }

  protected void init() throws Exception {

    
    // read length info from server
    bitLengthS = MailetCommon.ois.readInt();

    // write length info to client
    MailetCommon.oos.writeInt(bitLengthC);
    MailetCommon.oos.flush();

    // write Http and its length
//    Utils.writeBigInteger(Http, ,MailetCommon.oos);
//    MailetCommon.oos.flush();

    MailetCommon.oos.writeInt(http.length*8);
    MailetCommon.oos.flush();
        
    Utils.writeBigInteger(Http, http.length, MailetCommon.oos);
    MailetCommon.oos.flush();


    // init MailetCommon
    MailetCommon.bitLengthS = bitLengthS;
    MailetCommon.bitLengthC = bitLengthC;





    Circuit.isForGarbling = false;     // setup isForGarbling flag BEFORE create instance!!

    MailetCommon.initCircuits();  
    otNumOfPairs = bitLengthC + MailetCommon.keyLength;

    System.out.println(bitLengthC);
    System.out.println(MailetCommon.keyLength);
    System.out.println(key.length);

    super.init();
  }
  
  protected void execTransfer() throws Exception {

    StopWatch.taskTimeStamp("enter execTranser...");
    int bytelength = (Wire.labelBitLength-1)/8 + 1;
    msg1Lab = new BigInteger[bitLengthS];
    msg2Lab = new BigInteger[bitLengthC];
    keyLab = new BigInteger[MailetCommon.keyLength];

    System.out.println("msg2length is:");
    System.out.println(msg2Lab.length);



    for(int i = 0; i < bitLengthS; i++) {
      msg1Lab[i] = Utils.readBigInteger(bytelength, MailetCommon.ois);
    }
    StopWatch.taskTimeStamp("receiving labels for peer's inputs");


    // combine key and msg2
    
    BigInteger keyMsg2 = m;
    keyMsg2 = keyMsg2.shiftLeft(MailetCommon.keyLength);
    keyMsg2 = keyMsg2.xor(k);





    rcver.execProtocol(keyMsg2);
    keyMsg2Lab= rcver.getData();
    StopWatch.taskTimeStamp("receiving labels for self's inputs");



    // split keyMsg2Lab
    for(int i = 0; i < MailetCommon.keyLength; i++) {
      keyLab[i] = keyMsg2Lab[i];
    }
    
    for(int i = 0; i < bitLengthC; i++) {
      msg2Lab[i] = keyMsg2Lab[MailetCommon.keyLength + i];
    }



//  // Test by Shuai
//  System.out.println(new String(m.toByteArray()));
//  OutputStream testoutstream = new FileOutputStream("/home/shuai/workspace/output/client.txt");
//  Utils.writeBigInteger(m, bytelength, testoutstream);
//
//
//
//  OutputStream test2outstream = new FileOutputStream("/home/shuai/workspace/output/receive.txt");
//  for (int i = 0; i < keyLab.length; i++) {
//    Utils.writeBigInteger(keyLab[i], bytelength, test2outstream);
//    test2outstream.write((byte)'\n');
//  }
//
//
//  // Test End
//




  }


  protected void execCircuit() throws Exception {
    outputState = MailetCommon.execCircuit(msg1Lab, msg2Lab, keyLab, Http, http.length*8); 
  }

  protected void interpretResult() throws Exception {
    MailetCommon.oos.writeObject(outputState.toLabels());
    MailetCommon.oos.flush();
  }


  protected void verify_result() throws Exception{
  }



}
