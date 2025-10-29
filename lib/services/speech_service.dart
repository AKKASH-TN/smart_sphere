import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:path_provider/path_provider.dart';
import 'package:record/record.dart';
import 'dart:convert';

class SpeechService {
  static const String whisperApiUrl = 'https://jeevesh256-whisper-endpoint.hf.space/api/predict';
  final AudioRecorder _audioRecorder = AudioRecorder();
  String? _recordingPath;
  bool _isRecording = false;

  bool get isRecording => _isRecording;

  Future<bool> startRecording() async {
    try {
      // Check and request permission
      if (await _audioRecorder.hasPermission()) {
        // Get temporary directory
        final directory = await getTemporaryDirectory();
        _recordingPath = '${directory.path}/voice_command.wav';

        // Start recording
        await _audioRecorder.start(
          const RecordConfig(
            encoder: AudioEncoder.wav,
            sampleRate: 16000,
            numChannels: 1,
          ),
          path: _recordingPath!,
        );
        
        _isRecording = true;
        return true;
      }
      return false;
    } catch (e) {
      print('Error starting recording: $e');
      return false;
    }
  }

  Future<String?> stopRecordingAndTranscribe() async {
    try {
      if (!_isRecording) return null;

      // Stop recording
      await _audioRecorder.stop();
      _isRecording = false;

      if (_recordingPath == null) return null;

      // Transcribe the audio
      final transcript = await _transcribeAudio(_recordingPath!);
      
      // Clean up the file
      try {
        await File(_recordingPath!).delete();
      } catch (e) {
        print('Error deleting temp file: $e');
      }

      return transcript;
    } catch (e) {
      print('Error stopping recording: $e');
      _isRecording = false;
      return null;
    }
  }

  Future<String?> _transcribeAudio(String audioPath) async {
    try {
      // Create multipart request
      var request = http.MultipartRequest(
        'POST',
        Uri.parse(whisperApiUrl),
      );

      // Add the audio file
      request.files.add(
        await http.MultipartFile.fromPath(
          'data',
          audioPath,
          filename: 'audio.wav',
        ),
      );

      // Send the request
      final streamedResponse = await request.send();
      final response = await http.Response.fromStream(streamedResponse);

      if (response.statusCode == 200) {
        final jsonResponse = json.decode(response.body);
        
        // Parse the response - adjust based on actual API response format
        if (jsonResponse['data'] != null && jsonResponse['data'].isNotEmpty) {
          return jsonResponse['data'][0].toString().trim();
        }
        
        return null;
      } else {
        print('Whisper API error: ${response.statusCode} - ${response.body}');
        return null;
      }
    } catch (e) {
      print('Error transcribing audio: $e');
      return null;
    }
  }

  Future<void> cancelRecording() async {
    if (_isRecording) {
      await _audioRecorder.stop();
      _isRecording = false;
      
      // Clean up the file
      if (_recordingPath != null) {
        try {
          await File(_recordingPath!).delete();
        } catch (e) {
          print('Error deleting temp file: $e');
        }
      }
    }
  }

  void dispose() {
    _audioRecorder.dispose();
  }
}
