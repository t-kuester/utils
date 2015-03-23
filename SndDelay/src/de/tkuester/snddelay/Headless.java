package de.tkuester.snddelay;

public class Headless {
	
	public static void main(String[] args) throws Exception {
		SndDelayRunner runner = new SndDelayRunner();
		runner.delay = 1000;
		new Thread(runner).start();
	}
	
}
