package de.tkuester.snddelay;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

import javax.sound.sampled.AudioFormat;
import javax.sound.sampled.AudioSystem;
import javax.sound.sampled.DataLine;
import javax.sound.sampled.Line;
import javax.sound.sampled.Mixer;
import javax.sound.sampled.SourceDataLine;
import javax.sound.sampled.TargetDataLine;

public class Sandbox {

	final static Random RANDOM = new Random();
	
	public static void main(String[] args) throws Exception {

		AudioFormat format = new AudioFormat(8000.0f, 32, 1, true, true);
		
		// get microphone
		TargetDataLine microphone = AudioSystem.getTargetDataLine(format);
		microphone.open(format);
		System.out.println(microphone);

		// get loudspeaker
		SourceDataLine loudspeaker = AudioSystem.getSourceDataLine(format);
		loudspeaker.open(format);
		System.out.println(loudspeaker);

		
		System.out.println("----");
		
		// set up buffer
		ByteArrayOutputStream baos = new ByteArrayOutputStream();
		int numBytesRead;
		byte[] data = new byte[microphone.getBufferSize()];

		// start audio capture
		System.out.println("start audio capture...");
		System.out.println(microphone.getBufferSize());
		microphone.start();
		Thread.sleep(2000);
		
		System.out.println("Start reading...");
		
		long start = System.currentTimeMillis();
		while (System.currentTimeMillis() < start + 1000) {
			numBytesRead = microphone.read(data, 0, data.length);
			baos.write(data, 0, numBytesRead);
		}
		microphone.stop();
		
		byte[] captured = baos.toByteArray();
		System.out.println(captured.length);
		
		// start audio playback
		System.out.println("start audio playback...");
		loudspeaker.start();
		ByteArrayInputStream bais = new ByteArrayInputStream(captured);
		while ((numBytesRead = bais.read(data, 0, data.length)) > 0) {
			long t = System.currentTimeMillis();
			loudspeaker.write(data, 0, numBytesRead);
			System.out.println(System.currentTimeMillis() - t);
		}
		loudspeaker.stop();

		System.out.println("done");
		System.out.println(System.currentTimeMillis() - start);
		System.out.println(captured.length);
		long sum = 0;
		for (byte b : captured) sum += b;
		System.out.println(sum);
	}

	public static void printAllDevices() throws Exception {
		Mixer.Info[] mixerInfos = AudioSystem.getMixerInfo();
		for (Mixer.Info info : mixerInfos) {
			Mixer m = AudioSystem.getMixer(info);
			System.out.println(info);
			System.out.println(m);
			
			System.out.println("SOURCE LINES");
			for (Line.Info lineInfo : m.getSourceLineInfo()) {
				Line line = m.getLine(lineInfo);
				System.out.println(lineInfo);
				System.out.println(line);
			}
			
			System.out.println("TARGET LINES");
			for (Line.Info lineInfo : m.getTargetLineInfo()) {
				Line line = m.getLine(lineInfo);
				System.out.println(lineInfo);
				System.out.println(line);
			}
			System.out.println("=========");
		}
	}

	public static List<AudioFormat> getSupportedFormats(Class<?> dataLineClass) {
	    /*
	     * These define our criteria when searching for formats supported
	     * by Mixers on the system.
	     */
	    float sampleRates[] = { (float) 8000.0, (float) 16000.0, (float) 44100.0 };
	    int channels[] = { 1, 2 };
	    int bytesPerSample[] = { 2 };

	    AudioFormat format;
	    DataLine.Info lineInfo;

//	    SystemAudioProfile profile = new SystemAudioProfile(); // Used for allocating MixerDetails below.
	    List<AudioFormat> formats = new ArrayList<AudioFormat>();

	    for (Mixer.Info mixerInfo : AudioSystem.getMixerInfo()) {
	        for (int a = 0; a < sampleRates.length; a++) {
	            for (int b = 0; b < channels.length; b++) {
	                for (int c = 0; c < bytesPerSample.length; c++) {
	                    format = new AudioFormat(AudioFormat.Encoding.PCM_SIGNED,
	                            sampleRates[a], 8 * bytesPerSample[c], channels[b], bytesPerSample[c],
	                            sampleRates[a], false);
	                    lineInfo = new DataLine.Info(dataLineClass, format);
	                    if (AudioSystem.isLineSupported(lineInfo)) {
	                        /*
	                         * TODO: To perform an exhaustive search on supported lines, we should open
	                         * TODO: each Mixer and get the supported lines. Do this if this approach
	                         * TODO: doesn't give decent results. For the moment, we just work with whatever
	                         * TODO: the unopened mixers tell us.
	                         */
	                        if (AudioSystem.getMixer(mixerInfo).isLineSupported(lineInfo)) {
	                            formats.add(format);
	                        }
	                    }
	                }
	            }
	        }
	    }
	    return formats;
	}
}
