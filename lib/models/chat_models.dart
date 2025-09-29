class ChatMessage {
  final String text;
  final bool isUser;
  final DateTime timestamp;

  ChatMessage({
    required this.text,
    required this.isUser,
    required this.timestamp,
  });
}

class ChatSession {
  final List<ChatMessage> messages;
  final String sessionId;
  final DateTime createdAt;

  ChatSession({
    required this.messages,
    required this.sessionId,
    required this.createdAt,
  });

  ChatSession copyWith({
    List<ChatMessage>? messages,
    String? sessionId,
    DateTime? createdAt,
  }) {
    return ChatSession(
      messages: messages ?? this.messages,
      sessionId: sessionId ?? this.sessionId,
      createdAt: createdAt ?? this.createdAt,
    );
  }
}