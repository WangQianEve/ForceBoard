package com.example.qian.forceinput;

import android.app.Activity;
import android.content.Context;
import android.graphics.Color;
import android.net.wifi.WifiManager;
import android.os.Bundle;
import android.view.Gravity;
import android.view.WindowManager;
import android.widget.GridLayout;
import android.widget.LinearLayout;
import android.widget.TextView;

import java.math.BigInteger;
import java.net.InetAddress;
import java.net.UnknownHostException;
import android.os.Handler;

public class MainActivity extends Activity {
    public static Handler handler = new Handler();
    LinearLayout linearLayout = null;
    Thread serverThread = null;
    Server server = null;
    @Override
    protected void onDestroy(){
        super.onDestroy();
        server.setStop();
    }
    private String intIPToString(int ip) {
        String address;
        byte[] gwIp = getIpBytes(ip);

        try {
            InetAddress hostAddr = InetAddress.getByAddress(gwIp);
            address = hostAddr.getHostAddress();
        } catch (UnknownHostException e) {
            address = "";
        }
        return address;
    }

    private byte[] getIpBytes(int ip) {
        byte[] ipAddressReversed = (BigInteger.valueOf(ip).toByteArray());
        byte[] ipAddress = new byte[ipAddressReversed.length];
        for (int i = 0; i < ipAddress.length; i++) {
            ipAddress[i] = ipAddressReversed[ipAddress.length - 1 - i];
        }
        return ipAddress;
    }

    protected void onCreate(Bundle bundle) {
        super.onCreate(bundle);
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
        linearLayout=new LinearLayout(this);
        setContentView(linearLayout);

        linearLayout.setOrientation(LinearLayout.VERTICAL);
        WifiManager wifiManager = (WifiManager)getSystemService(Context.WIFI_SERVICE);
        int ipAddrInt=wifiManager.getDhcpInfo().ipAddress;
        String ipAddr = intIPToString(ipAddrInt);

        TextView ip = new TextView(this);
        ip.setText(ipAddr);
        ip.setTextColor(0x8888FFFF);
        ip.setWidth(320);
        ip.setGravity(Gravity.LEFT);
        ip.setTextSize(18);

        TextView missionStatus = new TextView(this);
        missionStatus.setWidth(320);
        missionStatus.setText("0/32");
        missionStatus.setGravity(Gravity.RIGHT);
        missionStatus.setTextSize(18);

        LinearLayout title=new LinearLayout(this);
        title.addView(ip);
        title.addView(missionStatus);
        linearLayout.addView(title);

        TextView mission = new TextView(this);
        mission.setText(" hello world");
        mission.setGravity(Gravity.LEFT);
        linearLayout.addView(mission);

        TextView input = new TextView(this);
        input.setPadding(0,0,0,6);
        input.setText(" _");
        input.setWidth(mission.getWidth());
        input.setGravity(Gravity.LEFT);
        input.setTextColor(0X80FFFFFF);
        linearLayout.addView(input);

        LinearLayout bar= (LinearLayout) getLayoutInflater().inflate(R.layout.layout,null);
        linearLayout.addView(bar);

        TextView block=null;

        GridLayout candidates = new GridLayout(this);
        candidates.setColumnCount(3);
        candidates.setRowCount(2);
        int k=0;
        while(k<6){
            k+=1;
            block=new TextView(this);
            block.setText("   ");
            block.setGravity(Gravity.CENTER);
            block.setPadding(0,5,0,0);
            block.setWidth(210);
            block.setTextColor(Color.DKGRAY);
            candidates.addView(block);
        }
        linearLayout.addView(candidates);

        server = new Server(linearLayout);
        serverThread = new Thread(server);
        serverThread.start();
    }
}
