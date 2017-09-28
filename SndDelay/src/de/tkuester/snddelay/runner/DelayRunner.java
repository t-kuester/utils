package de.tkuester.snddelay.runner;

import javax.sound.sampled.AudioFormat;
import javax.sound.sampled.AudioSystem;
import javax.sound.sampled.LineUnavailableException;
import javax.sound.sampled.SourceDataLine;
import javax.sound.sampled.TargetDataLine;

/**
 * Sound Delay Runner class. This captures sound from the microphone,
 * and sends it to the speaker after a short delay. It also supports
 * variation in pitch, although this is only rudimentary now, by 
 * choosing a different sample rate for the output channel, and does
 * not really work well yet.
 *
 * @author tkuester
 */
public class DelayRunner extends AbstractRunner {

	/** sample rate. 8 kHz should be enough for speech; CD-Audio uses 44.1 kHz. Lower 
	 * probably better for post-processing (FFT), but unless used, higher is better*/ 
	public static final float SAMPLE_RATE = 44_100.0f;
	
	/** bits per sample */
	public static final int SAMPLE_BITS = 32;
	
	/** buffer size */
	public static final int BUFFER_SIZE = 1_000_000;

	/** audio data line representing the microphone */
	private TargetDataLine microphone;
	
	/** audio data line representing the loudspeaker */
	private SourceDataLine loudspeaker;
	
	/** the delay between reading from microphone and writing to speaker */
	private final int delay;
	
	
	/**
	 * Create new Sound Delay Runner.
	 * 
	 * @param delay		the delay between recording and playback, in milliseconds
	 * @param pitch		the variation in pith between recording and playback, in percent
	 * @throws LineUnavailableException
	 */
	public DelayRunner(int delay, float pitch) throws LineUnavailableException {
		this.delay = delay;
		
		// initialize microphone and speaker
		AudioFormat inFormat = new AudioFormat(SAMPLE_RATE, SAMPLE_BITS, 1, true, true);
		microphone = AudioSystem.getTargetDataLine(inFormat);
		microphone.open(inFormat);

		AudioFormat outFormat = new AudioFormat(SAMPLE_RATE * pitch, SAMPLE_BITS, 1, true, true);
		loudspeaker = AudioSystem.getSourceDataLine(outFormat);
		loudspeaker.open(outFormat);
	}
	
	/**
	 * While running, the thread will repeatedly read small chunks of audio
	 * from the microphone and write them back to the speaker after a short
	 * delay. Meanwhile, the data is buffered in a ring-buffer.
	 */
	public void run() {
		// set up ring buffer and other variables
		byte[] buffer = new byte[BUFFER_SIZE];

		// determine chunk size
		double bytesPerSecond = (int) (SAMPLE_BITS * SAMPLE_RATE) / 8.;
//		int chunkSIze = (int) Math.min(microphone.getBufferSize() / 2, 
//				                       delay * bytesPerSecond / 1000.);
		int chunkSIze = microphone.getBufferSize() / 4; 
		// make chunk size integral number of frames
		int frameSize = SAMPLE_BITS / 8;
		chunkSIze = (chunkSIze / frameSize) * frameSize;
		
		int micPosition = 0;
		int spkPosition = 0;
		long start = System.currentTimeMillis();
		long last = start;
		
		System.out.println(chunkSIze);
		System.out.println((SAMPLE_BITS * SAMPLE_RATE) / 8000. * delay);
		
		// start delay loop
		microphone.start();
		loudspeaker.start();
		
		while (running) {
			// read chunk from microphone
			int bytesToRead = Math.min(buffer.length - micPosition, chunkSIze);
			int bytesFromMic = microphone.read(buffer, micPosition, bytesToRead);
			micPosition = (micPosition + bytesFromMic) % buffer.length;
			
			System.out.println(System.currentTimeMillis() - last);
			System.out.println("mic >>> " + bytesFromMic + "/" + chunkSIze + " \t " + micPosition);

			if (System.currentTimeMillis() > start + delay) {
				// write chunk to speaker
				int bytesToWrite = Math.min(buffer.length - spkPosition, chunkSIze);
				int bytesToSpk = loudspeaker.write(buffer, spkPosition, bytesToWrite);
				spkPosition = (spkPosition + bytesToSpk) % buffer.length;
				System.out.println("spk <<< " + bytesToSpk+ "/" + chunkSIze + " \t " + spkPosition);
				
				System.out.println((micPosition - spkPosition) / (float) bytesPerSecond);
			}
			last = System.currentTimeMillis();
		}
		
		// stop microphone and speaker
		microphone.stop();
		loudspeaker.stop();
		System.out.println("finished");
	}
}
