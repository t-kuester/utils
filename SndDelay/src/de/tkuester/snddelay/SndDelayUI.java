package de.tkuester.snddelay;

import java.awt.Dimension;
import java.awt.FlowLayout;
import java.awt.event.ActionEvent;

import javax.sound.sampled.LineUnavailableException;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JSlider;
import javax.swing.SwingUtilities;
import javax.swing.event.ChangeEvent;

/**
 * This class provides a very simple UI for the sound delay runner.
 * It only shows minimal controls for setting the delay in milli
 * seconds and for starting and stopping the recording/playback.
 *
 * @author tkuester
 */
public class SndDelayUI extends JFrame {

	private static final long serialVersionUID = -3961217351765298695L;

	/** thread running the sound delay runnable */
	private Thread thread = null;

	/**
	 * Initialize sound delay UI.
	 * 
	 * @param runner	the sound delay runner to use
	 */
	public SndDelayUI(SndDelayRunner runner) {
		super("Sound Delay UI");
		
		// widgets for setting and showing the delay in milli seconds
		JLabel label = new JLabel("Delay in ms");
		JSlider slider = new JSlider(0, 1000, 100);
		JLabel current = new JLabel(String.valueOf(slider.getValue()));
		current.setPreferredSize(new Dimension(50, 30));
		slider.addChangeListener((ChangeEvent e) -> {
			current.setText(String.valueOf(slider.getValue()));
		});
		
		// button for starting/stopping the recording and playback
		JButton button = new JButton("Start");
		button.addActionListener((ActionEvent e) -> {
			if (thread == null) {
				// update UI
				slider.setEnabled(false);
				button.setText("Stop");
				// start thread
				runner.delay = slider.getValue();
				thread = new Thread(runner);
				thread.start();
			} else {
				// update UI
				slider.setEnabled(true);
				button.setText("Start");
				// stop thread
				runner.delay = -1;
				thread = null;
			}
		});
		
		// assemble UI elements
		this.getContentPane().setLayout(new FlowLayout());
		this.getContentPane().add(label);
		this.getContentPane().add(slider);
		this.getContentPane().add(current);
		this.getContentPane().add(button);
		this.pack();
	}
	
	/**
	 * Execute program and show Sound Delay UI.
	 * 
	 * @param args	command line arguments (currently not used)
	 */
	public static void main(String[] args) {
        SwingUtilities.invokeLater(new Runnable() {
            public void run() {
            	try {
            		SndDelayRunner runner = new SndDelayRunner();
            		JFrame frame = new SndDelayUI(runner);
            		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            		frame.setVisible(true);
            	} catch (LineUnavailableException e) {
		        	e.printStackTrace();
		        }
            }
        });
	}
	
}
