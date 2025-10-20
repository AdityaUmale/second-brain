import Foundation

class APIClient {
    static let shared = APIClient()
    
    private let baseURL = "http://127.0.0.1:5555"
    private let session: URLSession
    
    private init() {
        let config = URLSessionConfiguration.default
        config.timeoutIntervalForRequest = 30
        config.timeoutIntervalForResource = 60
        session = URLSession(configuration: config)
    }
    
    // MARK: - Health Check
    
    func checkHealth() async -> Bool {
        guard let url = URL(string: "\(baseURL)/api/health") else { return false }
        
        do {
            let (data, _) = try await session.data(from: url)
            let response = try JSONDecoder().decode(HealthResponse.self, from: data)
            return response.initialized
        } catch {
            print("Health check failed: \(error)")
            return false
        }
    }
    
    // MARK: - Chat
    
    func sendQuery(_ query: String) async -> String? {
        guard let url = URL(string: "\(baseURL)/api/query") else { return nil }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let body = ["query": query]
        request.httpBody = try? JSONEncoder().encode(body)
        
        do {
            let (data, _) = try await session.data(for: request)
            let response = try JSONDecoder().decode(QueryResponse.self, from: data)
            return response.response
        } catch {
            print("Query failed: \(error)")
            return nil
        }
    }
    
    func getChatHistory() async -> [Message] {
        guard let url = URL(string: "\(baseURL)/api/history") else { return [] }
        
        do {
            let (data, _) = try await session.data(from: url)
            let response = try JSONDecoder().decode(HistoryResponse.self, from: data)
            return response.history
        } catch {
            print("Failed to load history: \(error)")
            return []
        }
    }
    
    func clearChatHistory() async {
        guard let url = URL(string: "\(baseURL)/api/history") else { return }
        
        var request = URLRequest(url: url)
        request.httpMethod = "DELETE"
        
        do {
            _ = try await session.data(for: request)
        } catch {
            print("Failed to clear history: \(error)")
        }
    }
    
    // MARK: - Capture
    
    func captureFullScreen() async -> (success: Bool, message: String) {
        guard let url = URL(string: "\(baseURL)/api/capture/full") else {
            return (false, "Invalid URL")
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        
        do {
            let (data, _) = try await session.data(for: request)
            let response = try JSONDecoder().decode(CaptureResponse.self, from: data)
            return (response.success, response.message)
        } catch {
            print("Capture failed: \(error)")
            return (false, "Capture failed: \(error.localizedDescription)")
        }
    }
    
    // MARK: - Database
    
    func getStats() async -> [String: Any] {
        guard let url = URL(string: "\(baseURL)/api/stats") else { return [:] }
        
        do {
            let (data, _) = try await session.data(from: url)
            if let json = try JSONSerialization.jsonObject(with: data) as? [String: Any],
               let stats = json["stats"] as? [String: Any] {
                return stats
            }
        } catch {
            print("Failed to get stats: \(error)")
        }
        return [:]
    }
    
    func clearDatabase() async -> Bool {
        guard let url = URL(string: "\(baseURL)/api/database") else { return false }
        
        var request = URLRequest(url: url)
        request.httpMethod = "DELETE"
        
        do {
            let (data, _) = try await session.data(for: request)
            let response = try JSONDecoder().decode(SuccessResponse.self, from: data)
            return response.success
        } catch {
            print("Failed to clear database: \(error)")
            return false
        }
    }
}

// MARK: - Response Models

struct HealthResponse: Codable {
    let status: String
    let initialized: Bool
    let message: String
}

struct QueryResponse: Codable {
    let response: String
    let success: Bool
}

struct HistoryResponse: Codable {
    let history: [Message]
}

struct CaptureResponse: Codable {
    let success: Bool
    let message: String
}

struct SuccessResponse: Codable {
    let success: Bool
}

