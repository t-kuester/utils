package de.tkuester.snddelay;

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
public class SndDelayRunner extends Thread {

	public static final float SAMPLE_RATE = 8000.0f;
	public static final int SAMPLE_BITS = 32;
	public static final int BUFFER_SIZE = 100_000;

	/** audio data line representing the microphone */
	private TargetDataLine microphone;
	
	/** audio data line representing the loudspeaker */
	private SourceDataLine loudspeaker;
	
	/** the delay between reading from microphone and writing to speaker */
	private final int delay;
	
	/** flag indicating whether the thread should still be running */
	private boolean running = true;
	
	/**
	 * Create new Sound Delay Runner.
	 * 
	 * @param delay		the delay between recording and playback, in milliseconds
	 * @param pitch		the variation in pith between recording and playback, in percent
	 * @throws LineUnavailableException
	 */
	public SndDelayRunner(int delay, float pitch) throws LineUnavailableException {
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
		int chunkSIze = microphone.getBufferSize() / 2;
		int micPosition = 0;
		int spkPosition = 0;
		long start = System.currentTimeMillis();

		// start delay loop
		microphone.start();
		loudspeaker.start();
		
		while (running) {
			// read chunk from microphone
			int bytesToRead = Math.min(buffer.length - micPosition, chunkSIze);
			int bytesFromMic = microphone.read(buffer, micPosition, bytesToRead);
			micPosition = (micPosition + bytesFromMic) % buffer.length;
			System.out.println("mic >>> " + bytesFromMic + "/" + chunkSIze + " \t " + micPosition);

			if (System.currentTimeMillis() > start + delay) {
				// write chunk to speaker
				int bytesToWrite = Math.min(buffer.length - spkPosition, chunkSIze);
				int bytesToSpk = loudspeaker.write(buffer, spkPosition, bytesToWrite);
				spkPosition = (spkPosition + bytesToSpk) % buffer.length;
				System.out.println("spk <<< " + bytesToSpk+ "/" + chunkSIze + " \t " + spkPosition);
			}
		}
		
		// stop microphone and speaker
		microphone.stop();
		loudspeaker.stop();
		System.out.println("finished");
	}
	
	/**
	 * Set a flag so the thread stops running.
	 */
	public void stopRunning() {
		this.running = false;
	}
}
