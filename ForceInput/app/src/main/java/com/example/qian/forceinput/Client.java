package com.example.qian.forceinput;

/**
 * Created by qian on 2016/9/1.
 */
import android.util.Log;

import org.json.JSONObject;

import java.io.BufferedWriter;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.Socket;
import java.util.ArrayList;

public class Client implements Runnable{
    String ipString="127.0.0.1";
    static int port=65401;
    InetAddress address=null;
    DatagramSocket ds = null;
    Socket socket = null;
    BufferedWriter bw = null;
    byte[] buf;
    public void run(){
        try {
            socket = new Socket("127.0.0.1", 65401);
            bw = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));
        }catch (Exception e){ Log.e("my_exception",e.getLocalizedMessage()); }
        JSONObject obj = new JSONObject();
        ArrayList<String> list=new ArrayList<String>();
        list.add("cand1");
        list.add("cand2");
        list.add("cand3");
        list.add("cand4");
        try {
            obj.put("type","task");
            obj.put("timestamp",123455);
            obj.put("position",2.3121);
            obj.put("results",list);
            obj.put("selected_index",3);
            obj.put("result","userinput_");
            obj.put("task","a steep learning curve in riding a unicycle");
            obj.put("id",2);
            obj.put("count",60);
            bw.write(obj.toString());
            bw.newLine();
            bw.flush();
//            buf= obj.toString().getBytes();
//            ds=new DatagramSocket();
//            address=InetAddress.getByName(ipString);
//            DatagramPacket dp = new DatagramPacket(buf, buf.length , address , port);
//            ds.send(dp);
        } catch (Exception e) {
            Log.e("me_exception","client");
        } finally {
            try{
                bw.close();
            }catch(Exception e){}
//            if (ds != null) if (ds.isConnected()) ds.close();
        }
    }
}
