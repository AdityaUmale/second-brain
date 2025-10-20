import SwiftUI

@main
struct SecondBrainAppApp: App {
    @NSApplicationDelegateAdaptor(AppDelegate.self) var appDelegate
    
    var body: some Scene {
        Settings {
            EmptyView()
        }
    }
}

class AppDelegate: NSObject, NSApplicationDelegate {
    var menuBarManager: MenuBarManager?
    
    func applicationDidFinishLaunching(_ notification: Notification) {
        // Hide the app from Dock and Cmd+Tab switcher
        NSApp.setActivationPolicy(.accessory)
        
        // Initialize the menu bar
        menuBarManager = MenuBarManager()
    }
}

