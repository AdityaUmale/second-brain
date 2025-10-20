import SwiftUI

struct Message: Identifiable, Codable {
    let id = UUID()
    let role: String
    let content: String
    
    var isUser: Bool { role == "user" }
    var isAssistant: Bool { role == "assistant" }
    var isSystem: Bool { role == "system" }
}

class ChatViewModel: ObservableObject {
    @Published var messages: [Message] = []
    @Published var inputText: String = ""
    @Published var isLoading: Bool = false
    
    private let apiClient = APIClient.shared
    
    init() {
        // Add welcome message
        messages.append(Message(role: "system", content: "Welcome! Ask questions about your captured knowledge."))
        loadHistory()
    }
    
    func loadHistory() {
        Task {
            let history = await apiClient.getChatHistory()
            await MainActor.run {
                self.messages = history
            }
        }
    }
    
    func sendMessage() {
        guard !inputText.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty else { return }
        
        let userMessage = inputText
        inputText = ""
        
        // Add user message
        messages.append(Message(role: "user", content: userMessage))
        isLoading = true
        
        Task {
            let response = await apiClient.sendQuery(userMessage)
            
            await MainActor.run {
                self.isLoading = false
                if let response = response {
                    self.messages.append(Message(role: "assistant", content: response))
                } else {
                    self.messages.append(Message(role: "system", content: "Failed to get response from backend"))
                }
            }
        }
    }
    
    func clearHistory() {
        Task {
            await apiClient.clearChatHistory()
            await MainActor.run {
                self.messages = [Message(role: "system", content: "Chat history cleared")]
            }
        }
    }
}

struct ChatView: View {
    @ObservedObject var viewModel: ChatViewModel
    @FocusState private var isInputFocused: Bool
    
    var body: some View {
        VStack(spacing: 0) {
            // Chat messages
            ScrollViewReader { proxy in
                ScrollView {
                    LazyVStack(alignment: .leading, spacing: 12) {
                        ForEach(viewModel.messages) { message in
                            MessageBubble(message: message)
                                .id(message.id)
                        }
                        
                        if viewModel.isLoading {
                            HStack {
                                ProgressView()
                                    .scaleEffect(0.8)
                                Text("Thinking...")
                                    .font(.caption)
                                    .foregroundColor(.secondary)
                            }
                            .padding(.leading)
                        }
                    }
                    .padding()
                }
                .onChange(of: viewModel.messages.count) { _ in
                    if let lastMessage = viewModel.messages.last {
                        withAnimation {
                            proxy.scrollTo(lastMessage.id, anchor: .bottom)
                        }
                    }
                }
            }
            
            Divider()
            
            // Input area
            HStack(spacing: 8) {
                TextField("Ask a question...", text: $viewModel.inputText, axis: .vertical)
                    .textFieldStyle(.plain)
                    .lineLimit(1...5)
                    .padding(8)
                    .background(Color(nsColor: .controlBackgroundColor))
                    .cornerRadius(8)
                    .focused($isInputFocused)
                    .onSubmit {
                        viewModel.sendMessage()
                    }
                
                Button(action: {
                    viewModel.clearHistory()
                }) {
                    Image(systemName: "trash")
                        .foregroundColor(.red)
                }
                .buttonStyle(.plain)
                .help("Clear chat history")
                
                Button(action: {
                    viewModel.sendMessage()
                }) {
                    Image(systemName: "arrow.up.circle.fill")
                        .foregroundColor(.accentColor)
                        .font(.system(size: 24))
                }
                .buttonStyle(.plain)
                .disabled(viewModel.inputText.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty)
                .help("Send message")
            }
            .padding()
            .background(Color(nsColor: .windowBackgroundColor).opacity(0.95))
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
        .onAppear {
            isInputFocused = true
        }
    }
}

struct MessageBubble: View {
    let message: Message
    
    var body: some View {
        HStack {
            if message.isUser {
                Spacer()
            }
            
            VStack(alignment: message.isUser ? .trailing : .leading, spacing: 4) {
                if !message.isSystem {
                    Text(message.isUser ? "You" : "🧠 Assistant")
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
                
                Text(message.content)
                    .padding(10)
                    .background(backgroundColor)
                    .foregroundColor(textColor)
                    .cornerRadius(12)
                    .textSelection(.enabled)
            }
            .frame(maxWidth: message.isSystem ? .infinity : 300, alignment: message.isUser ? .trailing : .leading)
            
            if message.isAssistant {
                Spacer()
            }
        }
    }
    
    var backgroundColor: Color {
        if message.isUser {
            return Color.accentColor
        } else if message.isAssistant {
            return Color.green.opacity(0.8)
        } else {
            return Color.purple.opacity(0.6)
        }
    }
    
    var textColor: Color {
        return .white
    }
}

#Preview {
    ChatView(viewModel: ChatViewModel())
        .frame(width: 400, height: 600)
}

