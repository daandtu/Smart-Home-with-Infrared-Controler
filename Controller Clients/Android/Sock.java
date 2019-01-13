package com.daandtu.smarthome;

import android.content.Context;
import android.content.res.Resources;
import android.util.Log;

import javax.net.ssl.*;
import java.io.*;
import java.net.InetAddress;
import java.net.Socket;
import java.security.*;
import java.security.cert.Certificate;
import java.security.cert.CertificateException;
import java.security.cert.CertificateFactory;

class Sock {

    private OnCreatedListener onCreatedListener;

    private String IP = "000.000.000.000";  //Set your server IP here
    private int PORT = 4444;  // Your server port

    private SSLSocket socket;
    private BufferedReader reader;
    private BufferedWriter writer;

    private Context context;
    private OnMessageListener onMessageListener;

    private boolean receive = false;


    Sock(Context context){
        this.context = context;
    }


    void create(){
        new Thread(new Runnable() {
            @Override
            public void run() {
                try (InputStream caInput = context.getResources().openRawResource(
                        context.getResources().getIdentifier("cert", "raw", context.getPackageName())
						// Store certificate file in raw folder
                )) {

                    Certificate ca = CertificateFactory.getInstance("X.509").generateCertificate(caInput);
                    // Load the key store using the CA
                    caInput.close();
                    KeyStore keyStore = KeyStore.getInstance(KeyStore.getDefaultType());
                    keyStore.load(null, null);
                    keyStore.setCertificateEntry("ca", ca);
                    // Initialize the TrustManager with this CA
                    TrustManagerFactory tmf = TrustManagerFactory.getInstance(TrustManagerFactory.getDefaultAlgorithm());
                    tmf.init(keyStore);
                    // Create an SSL context that uses the created trust manager
                    SSLContext sslContext = SSLContext.getInstance("TLS");
                    sslContext.init(null, tmf.getTrustManagers(), new SecureRandom());
                    SSLSocketFactory factory = sslContext.getSocketFactory();

                    socket = (SSLSocket) factory.createSocket(InetAddress.getByName(IP), PORT);
                    writer = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));
                    reader = new BufferedReader(new InputStreamReader(socket.getInputStream()));
					// Create reader and writer for the ssl socket

                    onCreatedListener.created(true, null);
                    receive = true;
                    startListening();

                } catch (KeyManagementException | NoSuchAlgorithmException | KeyStoreException | CertificateException | IOException e) {
                    e.printStackTrace();
                    receive = false;
                    onCreatedListener.created(false, e);
                }
            }
        }).start();
    }

    private void startListening(){
        new Thread(() -> {  // Listening Thread
            char[] buf = new char[1024];
            while (receive) {
                try {
                    if (onMessageListener != null){
                        String text = reader.readLine();
                        if (text != null && text.length() > 0) onMessageListener.gotMessage(text);
                    }
                }catch (IOException ioe){
                    ioe.printStackTrace();
                }
            }
        }).start();
    }

    void write(final String message){
        new Thread(() -> {
            try {
                writer.write(message);
                writer.flush();
            }catch (IOException ioe){
                ioe.printStackTrace();
            }
        }).start();
    }

    void close(){  // Close Socket
        new Thread(() -> {
            try {
                receive = false;
                if (writer != null) {
                    writer.write("q");
                    writer.flush();
                    writer.close();
                }
                if (socket != null) socket.close();
                if (reader != null) reader.close();
            }catch (IOException ignored){}
        }).start();
    }

    public interface OnCreatedListener{  // Register an onCreatedListener in your MainActivity
        void created(boolean success, Exception e);
    }

    void setOnCreatedListener(OnCreatedListener onCreatedListener) {
        this.onCreatedListener = onCreatedListener;
    }

    public interface OnMessageListener{  // Register an onMessageListener in your MainActivity
        void gotMessage(String message);
    }

    void setOnMessageListener(OnMessageListener onMessageListener){
        this.onMessageListener = onMessageListener;
    }
}
