package de.tkuester.snddelay.ui;

import java.awt.event.ActionEvent;

import javax.swing.JButton;
import javax.swing.JPanel;

import de.tkuester.snddelay.runner.AbstractRunner;

public abstract class AbstractRunnerPanel<T extends AbstractRunner> extends JPanel {

	private static final long serialVersionUID = -9083735452967369501L;

	/** button for starting and stopping the feedback */
	protected final JButton button;
	
	/** thread running the sound delay runnable */
	private T runner = null;

	public AbstractRunnerPanel() {

		// button for starting/stopping the recording and playback
		this.button = new JButton("Start");
		this.button.addActionListener((ActionEvent e) -> {
			if (runner == null) {
				startRunner();
			} else {
				stopRunner();
			}
		});
	}

	protected abstract T createRunner() throws Exception;
	
	/**
	 * Callback for starting the delayed audio feedback.
	 */
	protected void startRunner() {
		// update UI
		this.button.setText("Stop");

		try {
			// start thread
			this.runner = createRunner();
			new Thread(this.runner).start();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	/**
	 * Callback for stopping the audio feedback.
	 */
	protected void stopRunner() {
		// update UI
		this.button.setText("Start");
		
		// stop thread
		this.runner.stopRunning();
		this.runner = null;
	}
	
}
