import 'package:google_generative_ai/google_generative_ai.dart';

class GeminiService {
  static const String _apiKey =
      'AIzaSyC9HJmAywEscaD59nn4sO4ohBIyf6rGDOc'; 
  late final GenerativeModel _model;

  GeminiService() {
    _model = GenerativeModel(model: 'gemini-2.5-flash', apiKey: _apiKey);
  }

  Future<String> getChatResponse(String message, {String? context}) async {
    try {
      // Create a context-aware prompt for smart home automation
      final prompt = _buildSmartHomePrompt(message, context);

      final content = [Content.text(prompt)];
      final response = await _model.generateContent(content);

      return response.text ??
          'Sorry, I couldn\'t generate a response. Please try again.';
    } catch (e) {
      return 'Sorry, I encountered an error: ${e.toString()}. Please check your internet connection and try again.';
    }
  }

  String _buildSmartHomePrompt(String userMessage, String? context) {
    return '''
You are SmartSphere AI, an intelligent assistant for a smart home automation app called SmartSphere. 
Your role is to help users with:

1. Smart home device control and automation
2. Energy efficiency and analytics
3. Voice control features
4. Scheduling and automation setup
5. Device troubleshooting
6. Smart home best practices
7. Energy saving tips
8. Security recommendations for smart homes

Context about the app:
- SmartSphere is a comprehensive smart home automation platform
- Users can control lights, fans, and other smart devices
- The app includes energy analytics and consumption tracking
- Voice control capabilities are available
- Users can schedule automated tasks
- The app provides a modern, intuitive dashboard

${context != null ? 'Current app context: $context' : ''}

User message: $userMessage

Please provide helpful, accurate, and concise responses related to smart home automation. If the user asks about something unrelated to smart homes, politely redirect them to smart home topics. Always be friendly and professional.

Response:''';
  }

  Future<String> getSmartHomeAdvice(String deviceType, String issue) async {
    try {
      final prompt =
          '''
As SmartSphere AI, provide specific advice for this smart home issue:
Device Type: $deviceType
Issue/Question: $issue

Provide practical solutions, troubleshooting steps, or recommendations that would help a smart home user.
''';

      final content = [Content.text(prompt)];
      final response = await _model.generateContent(content);

      return response.text ?? 'Sorry, I couldn\'t provide advice at this time.';
    } catch (e) {
      return 'Error getting advice: ${e.toString()}';
    }
  }
}
