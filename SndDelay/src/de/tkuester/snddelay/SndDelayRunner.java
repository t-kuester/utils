package de.tkuester.snddelay;

import javax.sound.sampled.AudioFormat;
import javax.sound.sampled.AudioSystem;
import javax.sound.sampled.LineUnavailableException;
import javax.sound.sampled.SourceDataLine;
import javax.sound.sampled.TargetDataLine;

public class SndDelayRunner implements Runnable {

	private TargetDataLine microphone;
	private SourceDataLine loudspeaker;
	
	public int delay = 1000;
	
	public SndDelayRunner() throws LineUnavailableException {
		// initialize microphone and speaker
		AudioFormat format = new AudioFormat(8000.0f, 32, 1, true, true);
		microphone = AudioSystem.getTargetDataLine(format);
		loudspeaker = AudioSystem.getSourceDataLine(format);
		microphone.open(format);
		loudspeaker.open(format);
	}
	
	public void run() {
		// set up ring buffer and other variables
		byte[] buffer = new byte[100_000];
		int chunkSIze = microphone.getBufferSize() / 2;
		int micPosition = 0;
		int spkPosition = 0;
		long start = System.currentTimeMillis();

		// start delay loop
		microphone.start();
		loudspeaker.start();
		while (delay != -1) {
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
		microphone.stop();
		loudspeaker.stop();
		System.out.println("finished");
	}
	
}
