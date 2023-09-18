# STEPS
- Open VS code
- open SeamlessM4T folder from desktop
- open terminal and run the command "cd seamless_communication-main"

Speech-to-speech translation (S2ST)
Speech-to-text translation (S2TT)
Text-to-speech translation (T2ST)
Text-to-text translation (T2TT)
Automatic speech recognition (ASR)

1) For speech to speech we will need to use s2st , it converted english audio file to hindi audio file.

Syntax: m4t_predict <path_to_input_audio> s2st <tgt_lang> --output_path <path_to_save_audio>

Example: m4t_predict english_speech.wav s2st nob --output_path norwegian_speech.wav

2) For text to text we will need to use t2tt , sample below:

Syntax: m4t_predict <input_text> t2tt <tgt_lang> --src_lang <src_lang>

Example: m4t_predict "Hello, how are you?" t2tt hin --src_lang eng

3) For speech to text we will need to use s2tt , it converted english audio file to text file.

Syntax: m4t_predict <path_to_input_audio> s2tt <tgt_lang> --src_lang <src_lang>

Example: m4t_predict english_speech.wav s2tt eng --src_lang eng

4) For text to speech we will need to use t2st , it converted english text to audio file.

Syntax: m4t_predict <input_text> t2st <tgt_lang> --output_path <path_to_save_audio>

Example: m4t_predict "Welcome to OsloMet?" t2st eng --src_lang eng --output_path english_translated_audio.wav

-
