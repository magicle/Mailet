// copyright by shuai@cs.umn.edu





// TOFIX: bugs in testbit, only for highest bit of the type byte


// with reFormat, the input 



package Test;

import java.util.*;
import java.math.*;


import jargs.gnu.CmdLineParser;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;


import Utils.*;
import Program.*;

public class TestMailetServer {




    static short[] msgIn;
//  static short[] msgIn = {0x61,0x62,0x63,0x64,0x65,0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00};

  private static void printUsage() {
    System.out.println("Usage: java ..");
  }




  private static short[] hexString2ShortArray(String s) {
    int i;
    int len = s.length();
    short[] data = new short[len/2];
    
    for(i = 0; i < len; i += 2) {
      int higher = Character.digit(s.charAt(i), 16);
      int lower = Character.digit(s.charAt(i+1), 16);
      data[i/2] = (short) ((higher << 4) + lower);
    }
    return data;
  }

  private static void process_cmdline_args(String[] args) {
    CmdLineParser parser = new CmdLineParser();
  }






  public static void main(String[] args) throws Exception {
    StopWatch.pointTimeStamp("Starting Program!");
    process_cmdline_args(args);

    System.out.format("Note starts here!");


    // read from stdin
//    String str;
    try {
      String str;
      InputStreamReader in = new InputStreamReader(System.in);
      BufferedReader input = new BufferedReader(in);

      str = input.readLine();
      msgIn = hexString2ShortArray(str);
      System.out.println(str);

    }
    catch (IOException io) {
      io.printStackTrace();
    }





    for (int j=0; j<msgIn.length; j++) {
         System.out.format("%02X ", msgIn[j]);
    }
     System.out.println();


     System.out.format("Note ends here!");

    MailetServer mserver = new MailetServer(msgIn, 8*msgIn.length);
    mserver.run();
  }
}
