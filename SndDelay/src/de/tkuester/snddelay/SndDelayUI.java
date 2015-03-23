package de.tkuester.snddelay;

import java.awt.Dimension;
import java.awt.FlowLayout;
import java.awt.event.ActionEvent;

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JSlider;
import javax.swing.event.ChangeEvent;

public class SndDelayUI extends JFrame {

	private static final long serialVersionUID = -3961217351765298695L;
	
	private Thread thread = null;

	public SndDelayUI(SndDelayRunner runner) {
		super("Sound Delay UI");
		
		JLabel label = new JLabel("Delay in ms");
		JSlider slider = new JSlider(0, 1000, 100);
		JLabel current = new JLabel(String.valueOf(slider.getValue()));
		current.setPreferredSize(new Dimension(50, 30));
		slider.addChangeListener((ChangeEvent e) -> {
			current.setText(String.valueOf(slider.getValue()));
		});
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
		
		this.getContentPane().setLayout(new FlowLayout());
		this.getContentPane().add(label);
		this.getContentPane().add(slider);
		this.getContentPane().add(current);
		this.getContentPane().add(button);
		this.pack();
	}
	
	public static void main(String[] args) throws Exception {
        SwingUtilities.invokeLater(new Runnable() {
            public void run() {
				SndDelayRunner runner = new SndDelayRunner();
				JFrame frame = new SndDelayUI(runner);
				frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
				frame.setVisible(true);
            }
        });
	}
	
}
