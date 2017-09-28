package de.tkuester.snddelay.ui;

import javax.swing.JFrame;
import javax.swing.JTabbedPane;
import javax.swing.SwingUtilities;

/**
 * This class provides a very simple UI for the sound delay runner.
 * It only shows minimal controls for setting the delay in milli
 * seconds and for starting and stopping the recording/playback.
 *
 * @author tkuester
 */
public class SndDelayUI extends JFrame {

	private static final long serialVersionUID = -8831179642357330800L;

	/**
	 * Initialize sound delay UI.
	 */
	public SndDelayUI() {
		super("Sound Delay UI");
		
		JTabbedPane tabs = new JTabbedPane();
		tabs.add("Delay", new DelayRunnerPanel());
		tabs.add("Noise", new NoiseRunnerPanel());
		
		this.getContentPane().add(tabs);
		this.pack();
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
