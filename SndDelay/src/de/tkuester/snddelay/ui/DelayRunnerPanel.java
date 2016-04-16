package de.tkuester.snddelay.ui;

import java.awt.BorderLayout;

import de.tkuester.snddelay.runner.DelayRunner;

public class DelayRunnerPanel extends AbstractRunnerPanel<DelayRunner> {

	private static final long serialVersionUID = -5517890785243234835L;

	/** slider panel for the delay */
	private final SliderPanel delayPanel;
	
	/** slider panel for pitch variation */
	private final SliderPanel pitchPanel;

	public DelayRunnerPanel() {
		// widgets for setting delay and pitch
		this.delayPanel = new SliderPanel("Delay, in millis", 150, 0, 1000, 100);
		this.pitchPanel = new SliderPanel("Pitch variation, in %", 150, 50, 200, 100);
		
		// assemble UI elements
		this.setLayout(new BorderLayout());
		this.add(delayPanel, BorderLayout.NORTH);
		this.add(pitchPanel, BorderLayout.CENTER);
		this.add(button, BorderLayout.SOUTH);
	}

	@Override
	protected DelayRunner createRunner() throws Exception {
		int delay = this.delayPanel.getValue();
		float pitch = this.pitchPanel.getValue() / 100.f;
		return new DelayRunner(delay, pitch);
	}
	
	@Override
	protected void startRunner() {
		super.startRunner();
		this.delayPanel.setEnabled(false);
		this.pitchPanel.setEnabled(false);
	}

	@Override
	protected void stopRunner() {
		super.stopRunner();
		this.delayPanel.setEnabled(true);
		this.pitchPanel.setEnabled(true);
	}

}
