import UIKit
import WebKit

@main
class AppDelegate: UIResponder, UIApplicationDelegate {
    var window: UIWindow?
    func application(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
        let w = UIWindow(frame: UIScreen.main.bounds)
        w.rootViewController = DecisionController()
        w.makeKeyAndVisible()
        window = w
        return true
    }
}

final class DecisionController: UIViewController, WKScriptMessageHandler, WKNavigationDelegate, WKUIDelegate {
    private let keys = Set(["yaru-yaranai-p6-v6","yaru-yaranai-p5-v5","yaru-yaranai-p4-v4","yaru-yaranai-p3-v3","yaru-yaranai-p2-v2","yaru-yaranai-p1-v1"])
    private var values: [String: String] = [:]
    private var web: WKWebView!
    private var file: URL!
    override func loadView() {
        let dir = FileManager.default.urls(for: .applicationSupportDirectory, in: .userDomainMask)[0]
        file = dir.appendingPathComponent("decision-store.json")
        if FileManager.default.fileExists(atPath: file.path) {
            do { values = try JSONDecoder().decode([String:String].self, from: Data(contentsOf:file)) }
            catch { values = ["yaru-yaranai-p6-v6": "CORRUPT_NATIVE_STORE"] }
        }
        let config = WKWebViewConfiguration()
        config.websiteDataStore = .default()
        let controller = config.userContentController
        controller.add(self, name:"decisionStorage")
        controller.add(self, name:"decisionFiles")
        let initial = String(data: (try? JSONEncoder().encode(values)) ?? Data("{}".utf8), encoding:.utf8) ?? "{}"
        let js = """
        (()=>{const d=\(initial);window.decisionStore={
        getItem(k){return Object.hasOwn(d,k)?d[k]:null},
        setItem(k,v){d[k]=String(v);window.webkit.messageHandlers.decisionStorage.postMessage({op:"set",key:k,value:d[k]})},
        removeItem(k){delete d[k];window.webkit.messageHandlers.decisionStorage.postMessage({op:"remove",key:k})}
        };})();
        """
        controller.addUserScript(WKUserScript(source:js,injectionTime:.atDocumentStart,forMainFrameOnly:true))
        web = WKWebView(frame:.zero,configuration:config)
        web.navigationDelegate=self;web.uiDelegate=self
        web.backgroundColor=UIColor(red:0.067,green:0.075,blue:0.071,alpha:1)
        view=web
        if let url=Bundle.main.url(forResource:"index",withExtension:"html") {
            web.loadFileURL(url,allowingReadAccessTo:url.deletingLastPathComponent())
        }
    }
    private func message(_ title:String,_ body:String){let a=UIAlertController(title:title,message:body,preferredStyle:.alert);a.addAction(UIAlertAction(title:"OK",style:.default));if presentedViewController == nil {present(a,animated:true)}}
    func userContentController(_ c: WKUserContentController,didReceive m: WKScriptMessage){
        guard m.frameInfo.isMainFrame, let obj=m.body as? [String:Any] else{return}
        if m.name=="decisionStorage" {
            guard let key=obj["key"] as? String, keys.contains(key), let op=obj["op"] as? String else{return}
            var next=values
            if op=="set" {guard let value=obj["value"] as? String,value.utf8.count<=3_000_000 else{message("保存失敗","データ容量を超えました");return};next[key]=value}
            else if op=="remove" {next.removeValue(forKey:key)} else{return}
            do {try FileManager.default.createDirectory(at:file.deletingLastPathComponent(),withIntermediateDirectories:true);try JSONEncoder().encode(next).write(to:file,options:.atomic);values=next}
            catch {message("保存失敗","端末への書き込みに失敗しました。JSONを手動で保存してください。")}
        } else if m.name=="decisionFiles" {
            guard let name=obj["name"] as? String, name.range(of:"^[A-Za-z0-9._-]{1,100}$",options:.regularExpression) != nil,let text=obj["text"] as? String,text.utf8.count<=50_000_000 else{return}
            do {
                let dir=FileManager.default.temporaryDirectory.appendingPathComponent(UUID().uuidString)
                try FileManager.default.createDirectory(at:dir,withIntermediateDirectories:true)
                let url=dir.appendingPathComponent(name);try Data(text.utf8).write(to:url)
                let sheet=UIActivityViewController(activityItems:[url],applicationActivities:nil)
                sheet.popoverPresentationController?.sourceView=view
                sheet.popoverPresentationController?.sourceRect=CGRect(x:view.bounds.midX,y:view.bounds.midY,width:1,height:1)
                sheet.completionWithItemsHandler={_,_,_,_ in try? FileManager.default.removeItem(at:dir)}
                present(sheet,animated:true)
            }catch{message("保存失敗","ファイルを作成できませんでした")}
        }
    }
    func webView(_ webView: WKWebView,decidePolicyFor action: WKNavigationAction,decisionHandler: @escaping (WKNavigationActionPolicy)->Void){
        guard let url=action.request.url else{decisionHandler(.cancel);return}
        if url.isFileURL && url.lastPathComponent=="index.html" {decisionHandler(.allow);return}
        if action.navigationType == .linkActivated && url.scheme=="https" && url.host=="github.com"{UIApplication.shared.open(url)}
        decisionHandler(.cancel)
    }
    func webView(_ webView: WKWebView,runJavaScriptAlertPanelWithMessage text:String,initiatedByFrame frame:WKFrameInfo,completionHandler:@escaping ()->Void){
        let a=UIAlertController(title:nil,message:text,preferredStyle:.alert);a.addAction(UIAlertAction(title:"OK",style:.default){_ in completionHandler()});present(a,animated:true)
    }
    func webView(_ webView:WKWebView,runJavaScriptConfirmPanelWithMessage text:String,initiatedByFrame frame:WKFrameInfo,completionHandler:@escaping (Bool)->Void){
        let a=UIAlertController(title:nil,message:text,preferredStyle:.alert);a.addAction(UIAlertAction(title:"キャンセル",style:.cancel){_ in completionHandler(false)});a.addAction(UIAlertAction(title:"OK",style:.default){_ in completionHandler(true)});present(a,animated:true)
    }
}
