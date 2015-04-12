package de.tkuester.snddelay.ui;

import java.awt.Dimension;
import java.awt.FlowLayout;

import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JSlider;
import javax.swing.event.ChangeEvent;

/**
 * Helper class encapsulating a label, slider, and value field.
 *
 * @author tkuester
 */
public class SliderPanel extends JPanel {

	private static final long serialVersionUID = -4300085034221962782L;

	/** slider widget holding the current value */
	private final JSlider slider;
	
	/** label showing the current value */
	private final JLabel current;
	
	/**
	 * Create new SliderPanel.
	 * 
	 * @param title		title for the label
	 * @param width		width of the label (for alignment of multiple panels)
	 * @param min		minimum value
	 * @param max		maximum value
	 * @param value		initial value
	 */
	public SliderPanel(String title, int width, int min, int max, int value) {
		// create controls
		JLabel label = new JLabel(title);
		label.setPreferredSize(new Dimension(width, 30));
		this.slider = new JSlider(min, max, value);
		this.current = new JLabel(String.valueOf(this.slider.getValue()));
		this.current.setPreferredSize(new Dimension(50, 30));
		this.slider.addChangeListener((ChangeEvent e) -> {
			this.current.setText(String.valueOf(this.slider.getValue()));
		});
		
		// assemble widgets
		this.setLayout(new FlowLayout());
		this.add(label);
		this.add(slider);
		this.add(current);
	}

	/**
	 * Get currently selected value.
	 * 
	 * @return	currently selected value
	 */
	public int getValue() {
		return this.slider.getValue();
	}

	/**
	 * Enable or disable the slider widget.
	 */
	public void setEnabled(boolean enabled) {
		this.slider.setEnabled(enabled);
	}
	
}
