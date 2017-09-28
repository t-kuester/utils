package de.tkuester.snddelay.runner;

public abstract class AbstractRunner implements Runnable {
	
	/** flag indicating whether the thread should still be running */
	protected boolean running = true;

	/**
	 * Set a flag so the thread stops running.
	 */
	public void stopRunning() {
		this.running = false;
	}
	
}
