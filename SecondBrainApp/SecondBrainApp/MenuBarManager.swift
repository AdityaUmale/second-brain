import SwiftUI
import AppKit

class MenuBarManager: NSObject {
    private var statusItem: NSStatusItem?
    private var floatingWindow: FloatingWindow?
    private let apiClient = APIClient.shared
    
    override init() {
        super.init()
        setupMenuBar()
        checkBackendStatus()
    }
    
    private func setupMenuBar() {
        // Create status bar item
        statusItem = NSStatusBar.system.statusItem(withLength: NSStatusItem.variableLength)
        
        if let button = statusItem?.button {
            button.title = "🧠"
            button.action = #selector(menuBarIconClicked)
            button.target = self
        }
        
        // Create menu
        let menu = NSMenu()
        
        menu.addItem(NSMenuItem(title: "💬 Open Chat", action: #selector(openChat), keyEquivalent: "c"))
        menu.addItem(NSMenuItem.separator())
        menu.addItem(NSMenuItem(title: "📸 Capture Screen", action: #selector(captureScreen), keyEquivalent: "s"))
        menu.addItem(NSMenuItem.separator())
        menu.addItem(NSMenuItem(title: "📊 Database Stats", action: #selector(showStats), keyEquivalent: ""))
        menu.addItem(NSMenuItem(title: "🗑️  Clear Database", action: #selector(clearDatabase), keyEquivalent: ""))
        menu.addItem(NSMenuItem.separator())
        menu.addItem(NSMenuItem(title: "❌ Quit", action: #selector(quit), keyEquivalent: "q"))
        
        menu.items.forEach { $0.target = self }
        statusItem?.menu = menu
    }
    
    private func checkBackendStatus() {
        Task {
            let isReady = await apiClient.checkHealth()
            if isReady {
                await MainActor.run {
                    showNotification(title: "Second Brain", message: "Backend is ready! 🎉")
                }
            } else {
                await MainActor.run {
                    showNotification(title: "Second Brain", message: "Starting backend... Please wait.")
                }
            }
        }
    }
    
    @objc private func menuBarIconClicked() {
        // You can add custom behavior here if needed
    }
    
    @objc private func openChat() {
        if floatingWindow == nil {
            floatingWindow = FloatingWindow()
        }
        floatingWindow?.show()
    }
    
    @objc private func captureScreen() {
        Task {
            let result = await apiClient.captureFullScreen()
            if result.success {
                await MainActor.run {
                    showNotification(title: "Capture Complete", message: result.message)
                }
            } else {
                await MainActor.run {
                    showAlert(title: "Capture Failed", message: result.message)
                }
            }
        }
    }
    
    @objc private func showStats() {
        Task {
            let stats = await apiClient.getStats()
            await MainActor.run {
                let message = """
                Total Documents: \(stats["total_points"] ?? 0)
                Vectors: \(stats["vectors_count"] ?? 0)
                Status: \(stats["status"] ?? "Unknown")
                """
                showAlert(title: "Database Statistics", message: message)
            }
        }
    }
    
    @objc private func clearDatabase() {
        let alert = NSAlert()
        alert.messageText = "Clear Database?"
        alert.informativeText = "This will delete all stored knowledge. This cannot be undone!"
        alert.alertStyle = .warning
        alert.addButton(withTitle: "Cancel")
        alert.addButton(withTitle: "Delete All")
        
        if alert.runModal() == .alertSecondButtonReturn {
            Task {
                let success = await apiClient.clearDatabase()
                await MainActor.run {
                    if success {
                        showNotification(title: "Database Cleared", message: "All knowledge has been removed.")
                    } else {
                        showAlert(title: "Error", message: "Failed to clear database")
                    }
                }
            }
        }
    }
    
    @objc private func quit() {
        NSApplication.shared.terminate(nil)
    }
    
    private func showNotification(title: String, message: String) {
        let notification = NSUserNotification()
        notification.title = title
        notification.informativeText = message
        notification.soundName = NSUserNotificationDefaultSoundName
        NSUserNotificationCenter.default.deliver(notification)
    }
    
    private func showAlert(title: String, message: String) {
        let alert = NSAlert()
        alert.messageText = title
        alert.informativeText = message
        alert.alertStyle = .informational
        alert.addButton(withTitle: "OK")
        alert.runModal()
    }
}

