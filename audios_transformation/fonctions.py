import tensorflow as tf

wavs_path="audios_transformation/audios-data"
def encode_single_sample(wav_file,frame_length,frame_step,fft_length):
    file = tf.io.read_file(wavs_path+'/'+wav_file)
    
    audio, _ = tf.audio.decode_wav(file)
    audio = tf.squeeze(audio, axis=-1)
    
    audio = tf.cast(audio, tf.float32)
    
    spectrogram = tf.signal.stft(
        audio, frame_length=frame_length, frame_step=frame_step, fft_length=fft_length
    )
    
    spectrogram = tf.abs(spectrogram)
    spectrogram = tf.math.pow(spectrogram, 0.5)
    
    means = tf.math.reduce_mean(spectrogram, 1, keepdims=True)
    stddevs = tf.math.reduce_std(spectrogram, 1, keepdims=True)
    spectrogram = (spectrogram - means) / (stddevs + 1e-10)

    return spectrogram

def extract_audio_signal(wav_file):

    file = tf.io.read_file(wavs_path + '/' + wav_file)
    
    audio, _ = tf.audio.decode_wav(file)
    audio = tf.squeeze(audio, axis=-1)
    
    audio = tf.cast(audio, tf.float32)
    
    return audio
