class VoiceCommandProcessor {
  // Process the transcribed text and determine the action
  VoiceCommand? processCommand(String transcript) {
    if (transcript.isEmpty) return null;

    final lowerTranscript = transcript.toLowerCase().trim();

    // Device control commands
    if (_containsAny(lowerTranscript, ['turn on', 'switch on', 'enable', 'start'])) {
      if (_containsAny(lowerTranscript, ['light', 'lights', 'lamp'])) {
        return VoiceCommand(
          action: CommandAction.turnOnLight,
          device: 'light',
          transcript: transcript,
        );
      } else if (_containsAny(lowerTranscript, ['fan', 'fans'])) {
        return VoiceCommand(
          action: CommandAction.turnOnFan,
          device: 'fan',
          transcript: transcript,
        );
      }
    }

    if (_containsAny(lowerTranscript, ['turn off', 'switch off', 'disable', 'stop'])) {
      if (_containsAny(lowerTranscript, ['light', 'lights', 'lamp'])) {
        return VoiceCommand(
          action: CommandAction.turnOffLight,
          device: 'light',
          transcript: transcript,
        );
      } else if (_containsAny(lowerTranscript, ['fan', 'fans'])) {
        return VoiceCommand(
          action: CommandAction.turnOffFan,
          device: 'fan',
          transcript: transcript,
        );
      }
    }

    // Chatbot commands
    if (_containsAny(lowerTranscript, ['ask', 'chatbot', 'chat', 'help', 'assistant'])) {
      return VoiceCommand(
        action: CommandAction.openChatbot,
        transcript: transcript,
        query: _extractChatbotQuery(lowerTranscript),
      );
    }

    // Navigation commands
    if (_containsAny(lowerTranscript, ['show', 'open', 'go to', 'navigate'])) {
      if (_containsAny(lowerTranscript, ['device', 'devices'])) {
        return VoiceCommand(
          action: CommandAction.openDevices,
          transcript: transcript,
        );
      } else if (_containsAny(lowerTranscript, ['energy', 'analytics', 'consumption'])) {
        return VoiceCommand(
          action: CommandAction.openEnergy,
          transcript: transcript,
        );
      } else if (_containsAny(lowerTranscript, ['home', 'dashboard'])) {
        return VoiceCommand(
          action: CommandAction.openHome,
          transcript: transcript,
        );
      }
    }

    // Status commands
    if (_containsAny(lowerTranscript, ['status', 'check', 'what is', 'what\'s'])) {
      return VoiceCommand(
        action: CommandAction.checkStatus,
        transcript: transcript,
      );
    }

    // If no command matched, treat it as a chatbot query
    return VoiceCommand(
      action: CommandAction.openChatbot,
      transcript: transcript,
      query: transcript,
    );
  }

  bool _containsAny(String text, List<String> keywords) {
    return keywords.any((keyword) => text.contains(keyword));
  }

  String? _extractChatbotQuery(String text) {
    // Remove common chatbot trigger words to extract the actual query
    final triggers = ['ask', 'chatbot', 'chat', 'help', 'assistant'];
    String query = text;
    
    for (var trigger in triggers) {
      query = query.replaceAll(trigger, '').trim();
    }
    
    return query.isNotEmpty ? query : null;
  }
}

enum CommandAction {
  turnOnLight,
  turnOffLight,
  turnOnFan,
  turnOffFan,
  openChatbot,
  openDevices,
  openEnergy,
  openHome,
  checkStatus,
}

class VoiceCommand {
  final CommandAction action;
  final String transcript;
  final String? device;
  final String? query;

  VoiceCommand({
    required this.action,
    required this.transcript,
    this.device,
    this.query,
  });

  String getConfirmationMessage() {
    switch (action) {
      case CommandAction.turnOnLight:
        return 'Turning on the light';
      case CommandAction.turnOffLight:
        return 'Turning off the light';
      case CommandAction.turnOnFan:
        return 'Turning on the fan';
      case CommandAction.turnOffFan:
        return 'Turning off the fan';
      case CommandAction.openChatbot:
        return 'Opening chatbot${query != null ? ' with your question' : ''}';
      case CommandAction.openDevices:
        return 'Opening devices screen';
      case CommandAction.openEnergy:
        return 'Opening energy analytics';
      case CommandAction.openHome:
        return 'Going to home';
      case CommandAction.checkStatus:
        return 'Checking device status';
    }
  }
}
