# Voice Command Integration with Whisper AI

This document explains the voice-to-text integration using Whisper AI for SmartSphere.

## Overview

The app now supports voice commands for controlling devices, navigating screens, and interacting with the chatbot using speech-to-text powered by Whisper AI.

## Components

### 1. **SpeechService** (`lib/services/speech_service.dart`)
Handles audio recording and transcription via Whisper API.

**Features:**
- Records audio using the device microphone
- Sends audio to Whisper API endpoint
- Returns transcribed text
- Automatic cleanup of temporary files

**API Endpoint:** `https://jeevesh256-whisper-endpoint.hf.space/api/predict`

### 2. **VoiceCommandProcessor** (`lib/services/voice_command_processor.dart`)
Processes transcribed text and converts it into actionable commands.

**Supported Commands:**

#### Device Control:
- "Turn on light" / "Switch on light" → Turns on the light
- "Turn off light" / "Switch off light" → Turns off the light
- "Turn on fan" / "Switch on fan" → Turns on the fan
- "Turn off fan" / "Switch off fan" → Turns off the fan

#### Navigation:
- "Open devices" / "Show devices" → Opens devices screen
- "Open energy" / "Show analytics" → Opens energy analytics screen
- "Go to home" / "Open dashboard" → Returns to home screen

#### Chatbot:
- "Ask chatbot [question]" → Opens chatbot with the question
- "Chat [message]" → Opens chatbot with the message
- Any unrecognized command → Forwards to chatbot

#### Status:
- "Check status" / "What's the status" → Shows device status dialog

## Usage

### User Flow:

1. **Tap the Microphone FAB** (Floating Action Button) on the home screen
2. **Start Recording**: Tap the blue "Start" button
3. **Speak Your Command**: The button turns red while listening
4. **Stop Recording**: Tap the red "Stop" button
5. **Processing**: Audio is sent to Whisper AI for transcription
6. **Execution**: Command is processed and executed automatically

### Example Commands:

```
"Turn on the light"
"Switch off fan"
"Open chatbot and ask about energy saving tips"
"Show device status"
"Go to analytics"
```

## Technical Details

### Audio Recording:
- **Format**: WAV
- **Sample Rate**: 16000 Hz
- **Channels**: Mono (1 channel)
- **Package**: `record` v5.2.1

### Permissions Required:
- **Android**: Microphone permission
- **iOS**: Microphone permission
- **Windows**: Microphone access

### API Integration:

**Request Format:**
```http
POST https://jeevesh256-whisper-endpoint.hf.space/api/predict
Content-Type: multipart/form-data

data: [audio.wav file]
```

**Response Format:**
```json
{
  "data": ["transcribed text here"]
}
```

## Error Handling

The system handles various error scenarios:

1. **Permission Denied**: Shows error message if microphone access is denied
2. **API Failure**: Displays fallback message if transcription fails
3. **Empty Transcript**: Prompts user to try again
4. **Unknown Command**: Forwards to chatbot for assistance

## Future Enhancements

Potential improvements:
- Offline speech recognition
- Multi-language support
- Custom wake word detection
- Voice feedback responses
- Continuous listening mode

## Troubleshooting

### Microphone Not Working:
1. Check app permissions in device settings
2. Ensure microphone is not in use by another app
3. Restart the app

### Transcription Issues:
1. Check internet connection
2. Speak clearly and avoid background noise
3. Try shorter, simpler commands first

### API Connectivity:
- Ensure the Whisper API endpoint is accessible
- Check HuggingFace Space status if issues persist

## Credits

- **Whisper Model**: OpenAI Whisper (base model)
- **Deployment**: HuggingFace Spaces
- **Optimization**: Faster-Whisper with INT8 quantization
