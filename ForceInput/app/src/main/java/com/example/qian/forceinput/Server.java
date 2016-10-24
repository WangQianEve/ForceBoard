package com.example.qian.forceinput;

import android.graphics.Color;
import android.util.Log;
import android.view.Gravity;
import android.view.View;
import android.widget.GridLayout;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;

import org.json.JSONArray;
import org.json.JSONObject;
import org.w3c.dom.Text;

import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.lang.reflect.Array;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.logging.Handler;
import java.util.logging.LogRecord;

/**
 * Created by qian on 2016/9/1.
 */
public class Server implements Runnable {
    private final int UDP_SERVER_PORT = 65401;
    private final int MAX_UDP_DATAGRAM_LEN = 2048;
    private static ServerSocket serverSocket = null;
    private static Socket socket = null;
    private static String content = "";
    private TextView input;
    private ImageView imginput;
    private static LinearLayout layout;

    boolean shouldStop=false;
    private int last_pos=0,pos=0;
    private String cand;
    private String re;
    int k,k2;
    public Server(LinearLayout lay){
        this.layout=lay;
    }
    public void setStop(){
        shouldStop=true;
    }
    public void run(){
        int time=0;
        try {
            serverSocket = new ServerSocket(UDP_SERVER_PORT);
            while (!shouldStop) {
                socket = serverSocket.accept();
                Log.e("timestamp",System.currentTimeMillis()+"");
                BufferedReader br = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                String str = br.readLine();
                if (str.length() > 0) {
                    JSONObject jo = new JSONObject(str);
                    String type = jo.getString("type");
                    if (type.equals("update")) {
                        int timestamp = jo.getInt("timestamp");
                        if (timestamp < time) continue;
                        time = timestamp;
                        pos = (int)jo.getDouble("position");
                        final int temp_pos=last_pos;
                        MainActivity.handler.post(new Runnable() {
                            @Override
                            public void run() {
                                refreshBar(temp_pos,pos);
                            }
                        });
                        last_pos=pos;
                        cand=jo.getString("candidates");
                        cand=cand.substring(1,cand.length()-1);
                        k=jo.getInt("selected_index");
                        MainActivity.handler.post(new Runnable() {
                            @Override
                            public void run() {
                                refreshCand(k);
                            }
                        });
                        re=jo.getString("result");
                        MainActivity.handler.post(new Runnable() {
                            @Override
                            public void run() {
                                input = (TextView) layout.getChildAt(2);
                                input.setText(" "+re);
                            }
                        });
                    } else if (type.equals("task")) {
                        k=jo.getInt("id");
                        k2=jo.getInt("count");
                        content=jo.getString("task");
                        MainActivity.handler.post(new Runnable() {
                            @Override
                            public void run() {
                                LinearLayout l=(LinearLayout)layout.getChildAt(0);
                                input=(TextView)l.getChildAt(1);
                                input.setText(k+"/"+k2);
                                input=(TextView)layout.getChildAt(1);
                                input.setTextColor(Color.WHITE);
                                input.setGravity(Gravity.LEFT);
                                input.setText(" "+content);
                                input=(TextView)layout.getChildAt(2);
                                input.setText(" _");
                            }
                        });
                    } else if (type.equals("rest")) {
                        MainActivity.handler.post(new Runnable() {
                            @Override
                            public void run() {
                                input=(TextView)layout.getChildAt(1);
                                input.setText("You can have a rest now~");
                                input.setGravity(Gravity.CENTER);
                                input.setTextColor(0xAA30FF60);
                            }
                        });
                    }
                }
                try{
                    socket.close();
                }catch(Exception e){}
            }
        } catch (Exception e) {
//            Log.e("me_exception",e.getLocalizedMessage());
        } finally {
            try{
                socket.close();
                serverSocket.close();
            }catch(Exception e){}
        }
    }
    void refreshBar(int old, int nw){
        if(old==100||old==33)old=32;
        LinearLayout linearLayout=(LinearLayout)layout.getChildAt(3);
        imginput=(ImageView)linearLayout.getChildAt(old);
        imginput.setBackgroundColor(Color.DKGRAY);
        if(old>0){
            imginput=(ImageView)linearLayout.getChildAt(old-1);
            imginput.setBackgroundColor(Color.DKGRAY);
        }
        if(old>1){
            imginput=(ImageView)linearLayout.getChildAt(old-2);
            imginput.setBackgroundColor(Color.DKGRAY);
        }
        if(old>2){
            imginput=(ImageView)linearLayout.getChildAt(old-3);
            imginput.setBackgroundColor(Color.DKGRAY);
        }
        //
        if(old<32){
            imginput=(ImageView)linearLayout.getChildAt(old+1);
            imginput.setBackgroundColor(Color.DKGRAY);
        }
        if(old<31){
            imginput=(ImageView)linearLayout.getChildAt(old+2);
            imginput.setBackgroundColor(Color.DKGRAY);
        }
        if(old<30){
            imginput=(ImageView)linearLayout.getChildAt(old+3);
            imginput.setBackgroundColor(Color.DKGRAY);
        }
        //
        if(nw<33){
            imginput=(ImageView)linearLayout.getChildAt(nw);
            imginput.setBackgroundColor(0xAA30CC10);
        } else if(nw==100){
            imginput=(ImageView)linearLayout.getChildAt(32);
            imginput.setBackgroundColor(Color.RED);
        }
        if(nw<32){
            imginput=(ImageView)linearLayout.getChildAt(nw+1);
            imginput.setBackgroundColor(0xAA30CC10);
        }
        if(nw>0&&nw!=100){
            imginput=(ImageView)linearLayout.getChildAt(nw-1);
            imginput.setBackgroundColor(0xAA30CC10);
        }
    }
    void refreshCand(int selected){
        String[] candidate=cand.split(",");
        GridLayout gridLayout;
        int row=selected/3;
        if(row==candidate.length/3 && row>0) row--;
        try{
            for(int i=0; i<6; ++i){
                if(i>=(candidate.length-3*row)) content="   ";
                else content=candidate[i+row*3];
                gridLayout=(GridLayout)layout.getChildAt(4);
                input=(TextView)gridLayout.getChildAt(i);
                content=content.substring(1,content.length()-1);
                input.setText(content);
                if(selected==(i+3*row))input.setTextColor(0xAA55FFFF);
                else input.setTextColor(Color.DKGRAY);
            }
        }catch(Exception e){
            Log.e("me_exception",e.getLocalizedMessage());
        }
    }
}
