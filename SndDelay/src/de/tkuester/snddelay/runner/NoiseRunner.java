package de.tkuester.snddelay.runner;

import java.util.Random;

import javax.sound.sampled.AudioFormat;
import javax.sound.sampled.AudioSystem;
import javax.sound.sampled.LineUnavailableException;
import javax.sound.sampled.SourceDataLine;

/**
 * Instead of playing back the speech captured through the microphone, 
 * this runner simply floods the loudspeaker with random noise, blotting 
 * out any outside sounds, including the speakers own words. This might 
 * help, too, but probably should not be used in a debate...
 *
 * @author tkuester
 */
public class NoiseRunner extends AbstractRunner {
	
	/** Different types of noise... currently only white noise is supported */
	enum NOiSE_TYPE {
		WHITE, PINK, BROWN, GRAY;
	}

	public static final float SAMPLE_RATE = 8_000.0f;
	public static final int SAMPLE_BITS = 32;
	public static final int BUFFER_SIZE = 10_000;

	/** audio data line representing the loudspeaker */
	private SourceDataLine loudspeaker;
	
	
	/**
	 * Create new Sound Delay Runner.
	 * 
	 * @throws LineUnavailableException
	 */
	public NoiseRunner() throws LineUnavailableException {
		// initialize speaker
		AudioFormat outFormat = new AudioFormat(SAMPLE_RATE, SAMPLE_BITS, 1, true, true);
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
		
		int spkPosition = 0;

		// start delay loop
		loudspeaker.start();
		
		while (running) {
			// generate new random noise
			new Random().nextBytes(buffer);
			
			// write chunk to speaker
			int bytesToWrite = buffer.length - spkPosition;
			int bytesToSpk = loudspeaker.write(buffer, spkPosition, bytesToWrite);
			spkPosition = (spkPosition + bytesToSpk) % buffer.length;
			System.out.println("spk <<< " + bytesToSpk+ "/" + bytesToWrite + " \t " + spkPosition);
		}
		
		// stop microphone and speaker
		loudspeaker.stop();
		System.out.println("finished");
	}
	
}
