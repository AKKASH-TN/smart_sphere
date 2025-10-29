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

      // Clean up the response to remove markdown formatting
      String cleanedResponse = response.text ??
          'Sorry, I couldn\'t generate a response. Please try again.';
      
      // Remove markdown formatting
      cleanedResponse = _cleanMarkdown(cleanedResponse);

      return cleanedResponse;
    } catch (e) {
      return 'Sorry, I encountered an error: ${e.toString()}. Please check your internet connection and try again.';
    }
  }

  String _cleanMarkdown(String text) {
    // Remove bold markers (**)
    text = text.replaceAll(RegExp(r'\*\*'), '');
    // Remove italic markers (*)
    text = text.replaceAll(RegExp(r'(?<!\*)\*(?!\*)'), '');
    // Remove code block markers (```)
    text = text.replaceAll(RegExp(r'```[\w]*\n?'), '');
    // Remove inline code markers (`)
    text = text.replaceAll('`', '');
    // Remove header markers (#)
    text = text.replaceAll(RegExp(r'^#{1,6}\s+', multiLine: true), '');
    // Clean up multiple spaces
    text = text.replaceAll(RegExp(r'\s+'), ' ');
    // Clean up multiple newlines (keep max 2)
    text = text.replaceAll(RegExp(r'\n{3,}'), '\n\n');
    
    return text.trim();
  }

  String _buildSmartHomePrompt(String userMessage, String? context) {
    return '''
You are SmartSphere AI, a friendly and helpful smart home assistant. You're talking to Ash, who uses the SmartSphere app to control their home.

IMPORTANT INSTRUCTIONS:
- Talk like a friendly human assistant, not a robot
- Use natural, conversational language
- Don't use markdown formatting (no **, *, #, `, etc.)
- Keep responses concise and to the point (2-4 sentences max for simple questions)
- Use simple bullet points with • if listing items, but avoid other formatting
- Be warm, personable, and encouraging
- Address the user directly ("you" and "your")
- Show enthusiasm when appropriate
- If something is good news, express positivity naturally

Your expertise covers:
• Smart device control and automation
• Energy efficiency and saving tips
• Voice control setup and usage
• Scheduling and automation
• Device troubleshooting
• Home security recommendations

${context != null ? 'Current situation: $context' : ''}

User: $userMessage

Respond naturally as if you're having a friendly conversation. No markdown formatting. Be helpful and conversational:''';
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
