package de.tkuester.snddelay.ui;

import java.awt.BorderLayout;
import java.awt.event.ActionEvent;

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.SwingUtilities;

import de.tkuester.snddelay.SndDelayRunner;

/**
 * This class provides a very simple UI for the sound delay runner.
 * It only shows minimal controls for setting the delay in milli
 * seconds and for starting and stopping the recording/playback.
 *
 * @author tkuester
 */
public class SndDelayUI extends JFrame {

	private static final long serialVersionUID = -3961217351765298695L;
	
	/** slider panel for the delay */
	private final SliderPanel delayPanel;
	
	/** slider panel for pitch variation */
	private final SliderPanel pitchPanel;
	
	/** button for starting and stopping the feedback */
	private final JButton button;
	
	/** thread running the sound delay runnable */
	private Thread runner = null;

	/**
	 * Initialize sound delay UI.
	 */
	public SndDelayUI() {
		super("Sound Delay UI");
		
		// widgets for setting delay and pitch
		this.delayPanel = new SliderPanel("Delay, in millis", 150, 0, 1000, 100);
		this.pitchPanel = new SliderPanel("Pitch variation, in %", 150, 50, 200, 100);
		
		// button for starting/stopping the recording and playback
		this.button = new JButton("Start");
		this.button.addActionListener((ActionEvent e) -> {
			if (runner == null) {
				startFeedback();
			} else {
				stopFeedback();
			}
		});
		
		// assemble UI elements
		this.getContentPane().setLayout(new BorderLayout());
		this.getContentPane().add(delayPanel, BorderLayout.NORTH);
		this.getContentPane().add(pitchPanel, BorderLayout.CENTER);
		this.getContentPane().add(button, BorderLayout.SOUTH);
		this.pack();
	}

	/**
	 * Callback for starting the delayed audio feedback.
	 */
	protected void startFeedback() {
		// update UI
		this.delayPanel.setEnabled(false);
		this.pitchPanel.setEnabled(false);
		this.button.setText("Stop");

		try {
			// start thread
			int delay = this.delayPanel.getValue();
			this.runner = new SndDelayRunner(delay);
			this.runner.start();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	/**
	 * Callback for stopping the audio feedback.
	 */
	protected void stopFeedback() {

		// update UI
		this.delayPanel.setEnabled(true);
		this.pitchPanel.setEnabled(true);
		this.button.setText("Start");
		
		// stop thread
		this.runner.interrupt();
		this.runner = null;
	}
	
	/**
	 * Execute program and show Sound Delay UI.
	 * 
	 * @param args	command line arguments (currently not used)
	 */
	public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
        		JFrame frame = new SndDelayUI();
        		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        		frame.setVisible(true);
        	});
	}
	
}
