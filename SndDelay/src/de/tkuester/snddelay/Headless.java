package de.tkuester.snddelay;

/**
 * Run SndDelayRunner without a UI, mainly for quick testing.
 *
 * @author tkuester
 */
public class Headless {
	
	public static void main(String[] args) throws Exception {
		SndDelayRunner runner = new SndDelayRunner();
		runner.delay = 1000;
		new Thread(runner).start();
	}
	
}
