import SwiftUI
import AppKit

class FloatingWindow: NSObject {
    private var window: NSPanel?
    private var chatViewModel = ChatViewModel()
    
    override init() {
        super.init()
        setupWindow()
    }
    
    private func setupWindow() {
        // Create the panel
        let panel = NSPanel(
            contentRect: NSRect(x: 0, y: 0, width: 400, height: 600),
            styleMask: [.titled, .closable, .resizable, .nonactivatingPanel, .fullSizeContentView],
            backing: .buffered,
            defer: false
        )
        
        // Configure panel behavior
        panel.title = "🧠 Second Brain"
        panel.level = .floating  // Float above other windows
        panel.collectionBehavior = [.canJoinAllSpaces, .fullScreenAuxiliary]
        panel.isFloatingPanel = true
        panel.becomesKeyOnlyIfNeeded = true
        panel.hidesOnDeactivate = false
        panel.titlebarAppearsTransparent = true
        panel.backgroundColor = NSColor(white: 0.1, alpha: 0.95)
        
        // Center on screen
        panel.center()
        
        // Set SwiftUI content
        let contentView = ChatView(viewModel: chatViewModel)
        panel.contentView = NSHostingView(rootView: contentView)
        
        self.window = panel
    }
    
    func show() {
        window?.makeKeyAndOrderFront(nil)
        NSApp.activate(ignoringOtherApps: true)
    }
    
    func hide() {
        window?.orderOut(nil)
    }
    
    func toggle() {
        if window?.isVisible == true {
            hide()
        } else {
            show()
        }
    }
}

