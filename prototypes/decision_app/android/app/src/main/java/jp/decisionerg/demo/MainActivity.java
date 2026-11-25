package jp.decisionerg.demo;
import android.app.Activity;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.webkit.*;
import android.widget.Toast;
import androidx.webkit.WebViewAssetLoader;
import java.io.OutputStream;
import java.nio.charset.StandardCharsets;

public class MainActivity extends Activity {
    private WebView web;
    private ValueCallback<Uri[]> chooser;
    private String exportText;
    private static final String LOCAL="https://appassets.androidplatform.net/assets/index.html";
    private static final int IMPORT=31, EXPORT=32;
    @Override public void onCreate(Bundle state) {
        super.onCreate(state);
        web=new WebView(this);
        web.setBackgroundColor(0xff111312);
        WebSettings s=web.getSettings();
        s.setJavaScriptEnabled(true);s.setDomStorageEnabled(true);
        s.setAllowFileAccess(false);s.setAllowContentAccess(true);
        s.setMixedContentMode(WebSettings.MIXED_CONTENT_NEVER_ALLOW);
        WebViewAssetLoader loader=new WebViewAssetLoader.Builder()
            .addPathHandler("/assets/",new WebViewAssetLoader.AssetsPathHandler(this)).build();
        web.setWebViewClient(new WebViewClient(){
            @Override public WebResourceResponse shouldInterceptRequest(WebView v,WebResourceRequest req){
                WebResourceResponse response=loader.shouldInterceptRequest(req.getUrl());
                if(response!=null)return response;
                return new WebResourceResponse("text/plain","UTF-8",403,"Blocked",java.util.Collections.emptyMap(),new java.io.ByteArrayInputStream(new byte[0]));
            }
            @Override public boolean shouldOverrideUrlLoading(WebView v,WebResourceRequest req){
                Uri u=req.getUrl();
                if(LOCAL.equals(u.toString()))return false;
                if(req.isForMainFrame()&&req.hasGesture()&&"https".equals(u.getScheme())&&"github.com".equals(u.getHost())){
                    try{startActivity(new Intent(Intent.ACTION_VIEW,u));}catch(Exception e){notifyUser("リンクを開けません");}
                }
                return true;
            }
        });
        web.setWebChromeClient(new WebChromeClient(){
            @Override public boolean onShowFileChooser(WebView v,ValueCallback<Uri[]> cb,FileChooserParams params){
                if(chooser!=null)chooser.onReceiveValue(null);
                chooser=cb;
                try{Intent i=new Intent(Intent.ACTION_OPEN_DOCUMENT);i.addCategory(Intent.CATEGORY_OPENABLE);i.setType("*/*");startActivityForResult(i,IMPORT);}
                catch(Exception e){chooser.onReceiveValue(null);chooser=null;}
                return true;
            }
        });
        web.addJavascriptInterface(new FilesBridge(),"NativeFiles");
        setContentView(web);web.loadUrl(LOCAL);
    }
    private void notifyUser(String s){runOnUiThread(()->Toast.makeText(this,s,Toast.LENGTH_LONG).show());}
    public class FilesBridge {
        @JavascriptInterface public void save(String name,String text,String mime){
            if(name==null||!name.matches("[A-Za-z0-9._-]{1,100}")||text==null||text.length()>50000000){notifyUser("書き出しデータが不正です");return;}
            runOnUiThread(()->{if(exportText!=null)return;exportText=text;try{Intent i=new Intent(Intent.ACTION_CREATE_DOCUMENT);
                i.addCategory(Intent.CATEGORY_OPENABLE);i.setType(name.endsWith(".json")?"application/json":"text/plain");i.putExtra(Intent.EXTRA_TITLE,name);startActivityForResult(i,EXPORT);
            }catch(Exception e){exportText=null;notifyUser("保存先を開けません");}});
        }
    }
    @Override protected void onActivityResult(int request,int result,Intent data){
        super.onActivityResult(request,result,data);
        if(request==IMPORT&&chooser!=null){chooser.onReceiveValue(result==RESULT_OK&&data!=null&&data.getData()!=null?new Uri[]{data.getData()}:null);chooser=null;}
        if(request==EXPORT){String value=exportText;exportText=null;
            if(result==RESULT_OK&&data!=null&&data.getData()!=null&&value!=null){
                try(OutputStream out=getContentResolver().openOutputStream(data.getData(),"wt")){
                    if(out==null)throw new java.io.IOException("no output");out.write(value.getBytes(StandardCharsets.UTF_8));notifyUser("保存しました");
                }catch(Exception e){notifyUser("保存に失敗しました");}
            }
        }
    }
    @Override protected void onDestroy(){if(chooser!=null){chooser.onReceiveValue(null);chooser=null;}if(web!=null){web.removeJavascriptInterface("NativeFiles");web.destroy();}super.onDestroy();}
}
