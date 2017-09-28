package de.tkuester.snddelay.ui;

import java.awt.BorderLayout;

import javax.swing.JLabel;

import de.tkuester.snddelay.runner.NoiseRunner;

public class NoiseRunnerPanel extends AbstractRunnerPanel<NoiseRunner>{

	private static final long serialVersionUID = 3423708590853161551L;

	public NoiseRunnerPanel() {
		// assemble UI elements
		this.setLayout(new BorderLayout());
		this.add(new JLabel("No settings required"), BorderLayout.CENTER);
		this.add(button, BorderLayout.SOUTH);
	}

	@Override
	protected NoiseRunner createRunner() throws Exception {
		return new NoiseRunner();
	}

}
