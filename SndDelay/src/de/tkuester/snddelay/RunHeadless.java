package de.tkuester.snddelay;

import de.tkuester.snddelay.runner.DelayRunner;

/**
 * Run SndDelayRunner without a UI, mainly for quick testing.
 *
 * @author tkuester
 */
public class RunHeadless {
	
	public static void main(String[] args) throws Exception {
		new Thread(new DelayRunner(1000, 1f)).start();
//		new Thread(new NoiseRunner()).start();
	}
	
}
