package de.tkuester.snddelay;

/**
 * Run SndDelayRunner without a UI, mainly for quick testing.
 *
 * @author tkuester
 */
public class Headless {
	
	public static void main(String[] args) throws Exception {
		SndDelayRunner runner = new SndDelayRunner(2000);
		runner.start();
	}
	
}
