import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.util.ArrayList;
import java.io.*;

/**
 * SubscriptionGUI - Main GUI class for managing AI model subscriptions.
 * Stores an ArrayList of AIModel objects and provides a graphical interface
 * for adding, managing, and exporting subscription plans.
 * @author Student
 */
public class SubscriptionGUI extends JFrame implements ActionListener {

    // ArrayList to store AI model plans
    private ArrayList<AIModel> subscriptionList = new ArrayList<>();

    // Text Fields
    private JTextField tfModelName      = new JTextField(15);
    private JTextField tfPrice          = new JTextField(10);
    private JTextField tfParameters     = new JTextField(10);
    private JTextField tfContextWindow  = new JTextField(10);
    private JTextField tfPromptQuota    = new JTextField(10);
    private JTextField tfTeamSlots      = new JTextField(10);
    private JTextField tfPromptText     = new JTextField(20);
    private JTextField tfResponseLength = new JTextField(10);
    private JTextField tfMemberName     = new JTextField(15);
    private JTextField tfIndex          = new JTextField(5);

    // Buttons
    private JButton btnAddPersonal  = new JButton("Add Personal Plan");
    private JButton btnAddPro       = new JButton("Add Pro Plan");
    private JButton btnDisplayAll   = new JButton("Display All");
    private JButton btnClear        = new JButton("Clear");
    private JButton btnGivePrompt   = new JButton("Give a Prompt");
    private JButton btnAddMember    = new JButton("Add Team Member");
    private JButton btnCheckType    = new JButton("Check Plan Type");
    private JButton btnExport       = new JButton("Export to File");
    private JButton btnLoad         = new JButton("Load From File");

    // Display Area
    private JTextArea displayArea = new JTextArea(12, 50);

    /**
     * Constructor - sets up the GUI layout and registers action listeners.
     */
    public SubscriptionGUI() {
        setTitle("AI Subscription Manager");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLayout(new BorderLayout(10, 10));

        // --- Top Panel: Input Fields ---
        JPanel inputPanel = new JPanel(new GridLayout(0, 4, 5, 5));
        inputPanel.setBorder(BorderFactory.createTitledBorder("AI Model Details"));

        inputPanel.add(new JLabel("Model Name:"));
        inputPanel.add(tfModelName);
        inputPanel.add(new JLabel("Price (NPR/1L tokens):"));
        inputPanel.add(tfPrice);

        inputPanel.add(new JLabel("Parameters (billions):"));
        inputPanel.add(tfParameters);
        inputPanel.add(new JLabel("Context Window:"));
        inputPanel.add(tfContextWindow);

        inputPanel.add(new JLabel("Prompt Quota (Personal):"));
        inputPanel.add(tfPromptQuota);
        inputPanel.add(new JLabel("Team Slots (Pro):"));
        inputPanel.add(tfTeamSlots);

        inputPanel.add(new JLabel("Prompt Text:"));
        inputPanel.add(tfPromptText);
        inputPanel.add(new JLabel("Response Length (tokens):"));
        inputPanel.add(tfResponseLength);

        inputPanel.add(new JLabel("Team Member Name:"));
        inputPanel.add(tfMemberName);
        inputPanel.add(new JLabel("Index Number:"));
        inputPanel.add(tfIndex);

        add(inputPanel, BorderLayout.NORTH);

        // --- Middle Panel: Buttons ---
        JPanel buttonPanel = new JPanel(new FlowLayout(FlowLayout.CENTER, 8, 8));
        buttonPanel.add(btnAddPersonal);
        buttonPanel.add(btnAddPro);
        buttonPanel.add(btnDisplayAll);
        buttonPanel.add(btnClear);
        buttonPanel.add(btnGivePrompt);
        buttonPanel.add(btnAddMember);
        buttonPanel.add(btnCheckType);
        buttonPanel.add(btnExport);
        buttonPanel.add(btnLoad);
        add(buttonPanel, BorderLayout.CENTER);

        // --- Bottom Panel: Display Area ---
        displayArea.setEditable(false);
        displayArea.setFont(new Font("Monospaced", Font.PLAIN, 12));
        JScrollPane scrollPane = new JScrollPane(displayArea);
        scrollPane.setBorder(BorderFactory.createTitledBorder("Output"));
        add(scrollPane, BorderLayout.SOUTH);

        // Register Action Listeners
        btnAddPersonal.addActionListener(this);
        btnAddPro.addActionListener(this);
        btnDisplayAll.addActionListener(this);
        btnClear.addActionListener(this);
        btnGivePrompt.addActionListener(this);
        btnAddMember.addActionListener(this);
        btnCheckType.addActionListener(this);
        btnExport.addActionListener(this);
        btnLoad.addActionListener(this);

        pack();
        setLocationRelativeTo(null);
        setVisible(true);
    }

    /**
     * Validates and returns the index entered in tfIndex.
     * Returns -1 if the input is invalid or out of range.
     * @return Valid index integer, or -1 on error
     */
    private int getDisplayNumber() {
        int displayNumber = -1;
        try {
            int input = Integer.parseInt(tfIndex.getText().trim());
            if (input >= 0 && input < subscriptionList.size()) {
                displayNumber = input;
            } else {
                JOptionPane.showMessageDialog(this,
                        "Error: Index out of range. Please enter a value between 0 and "
                                + (subscriptionList.size() - 1) + ".",
                        "Invalid Index", JOptionPane.ERROR_MESSAGE);
            }
        } catch (NumberFormatException e) {
            JOptionPane.showMessageDialog(this,
                    "Error: Please enter a valid integer index.",
                    "Invalid Input", JOptionPane.ERROR_MESSAGE);
        }
        return displayNumber;
    }

    /**
     * Determines and displays the plan type (PersonalPlan or ProPlan) at the given index.
     * @param index Index in the subscriptionList
     */
    private void checkPlanType(int index) {
        AIModel model = subscriptionList.get(index);
        if (model instanceof PersonalPlan) {
            JOptionPane.showMessageDialog(this, "Plan at index " + index + " is a: Personal Plan",
                    "Plan Type", JOptionPane.INFORMATION_MESSAGE);
        } else if (model instanceof ProPlan) {
            JOptionPane.showMessageDialog(this, "Plan at index " + index + " is a: Pro Plan",
                    "Plan Type", JOptionPane.INFORMATION_MESSAGE);
        } else {
            JOptionPane.showMessageDialog(this, "Plan at index " + index + " is of an unknown type.",
                    "Plan Type", JOptionPane.WARNING_MESSAGE);
        }
    }

    /**
     * Handles all button click events.
     * @param e The ActionEvent triggered by a button
     */
    @Override
    public void actionPerformed(ActionEvent e) {
        Object source = e.getSource();

        // --- Add Personal Plan ---
        if (source == btnAddPersonal) {
            try {
                String name    = tfModelName.getText().trim();
                double price   = Double.parseDouble(tfPrice.getText().trim());
                int params     = Integer.parseInt(tfParameters.getText().trim());
                String context = tfContextWindow.getText().trim();
                int quota      = Integer.parseInt(tfPromptQuota.getText().trim());

                PersonalPlan plan = new PersonalPlan(name, price, params, context, quota);
                subscriptionList.add(plan);
                displayArea.setText("Personal Plan added successfully!\n" + plan.display());
            } catch (NumberFormatException ex) {
                JOptionPane.showMessageDialog(this, "Error: Please enter valid numeric values for price, parameters, and quota.",
                        "Input Error", JOptionPane.ERROR_MESSAGE);
            }
        }

        // --- Add Pro Plan ---
        else if (source == btnAddPro) {
            try {
                String name    = tfModelName.getText().trim();
                double price   = Double.parseDouble(tfPrice.getText().trim());
                int params     = Integer.parseInt(tfParameters.getText().trim());
                String context = tfContextWindow.getText().trim();
                int slots      = Integer.parseInt(tfTeamSlots.getText().trim());

                ProPlan plan = new ProPlan(name, price, params, context, slots);
                subscriptionList.add(plan);
                displayArea.setText("Pro Plan added successfully!\n" + plan.display());
            } catch (NumberFormatException ex) {
                JOptionPane.showMessageDialog(this, "Error: Please enter valid numeric values for price, parameters, and team slots.",
                        "Input Error", JOptionPane.ERROR_MESSAGE);
            }
        }

        // --- Display All ---
        else if (source == btnDisplayAll) {
            if (subscriptionList.isEmpty()) {
                displayArea.setText("No plans in the list.");
                return;
            }
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < subscriptionList.size(); i++) {
                sb.append("=== Index: ").append(i).append(" ===\n");
                sb.append(subscriptionList.get(i).display()).append("\n\n");
            }
            displayArea.setText(sb.toString());
        }

        // --- Clear ---
        else if (source == btnClear) {
            tfModelName.setText("");
            tfPrice.setText("");
            tfParameters.setText("");
            tfContextWindow.setText("");
            tfPromptQuota.setText("");
            tfTeamSlots.setText("");
            tfPromptText.setText("");
            tfResponseLength.setText("");
            tfMemberName.setText("");
            tfIndex.setText("");
            displayArea.setText("");
        }

        // --- Give a Prompt ---
        else if (source == btnGivePrompt) {
            int index = getDisplayNumber();
            if (index != -1) {
                AIModel model = subscriptionList.get(index);
                if (model instanceof PersonalPlan) {
                    try {
                        String promptText    = tfPromptText.getText().trim();
                        int responseLength   = Integer.parseInt(tfResponseLength.getText().trim());
                        PersonalPlan pp      = (PersonalPlan) model;
                        String result        = pp.enterPrompt(promptText, responseLength);
                        displayArea.setText(result);
                    } catch (NumberFormatException ex) {
                        JOptionPane.showMessageDialog(this, "Error: Response length must be a valid integer.",
                                "Input Error", JOptionPane.ERROR_MESSAGE);
                    }
                } else {
                    JOptionPane.showMessageDialog(this,
                            "Error: Give a Prompt is only available for Personal Plan subscriptions.",
                            "Plan Type Error", JOptionPane.ERROR_MESSAGE);
                }
            }
        }

        // --- Add Team Member ---
        else if (source == btnAddMember) {
            int index = getDisplayNumber();
            if (index != -1) {
                AIModel model = subscriptionList.get(index);
                if (model instanceof ProPlan) {
                    String memberName = tfMemberName.getText().trim();
                    ProPlan pp        = (ProPlan) model;
                    String result     = pp.addTeamMember(memberName);
                    displayArea.setText(result);
                } else {
                    JOptionPane.showMessageDialog(this,
                            "Error: Team collaboration is only available for Pro Plan subscriptions.",
                            "Plan Type Error", JOptionPane.ERROR_MESSAGE);
                }
            }
        }

        // --- Check Plan Type ---
        else if (source == btnCheckType) {
            int index = getDisplayNumber();
            if (index != -1) {
                checkPlanType(index);
            }
        }

        // --- Export to File ---
        else if (source == btnExport) {
            if (subscriptionList.isEmpty()) {
                JOptionPane.showMessageDialog(this, "No plans to export.", "Export Error", JOptionPane.WARNING_MESSAGE);
                return;
            }
            try (BufferedWriter writer = new BufferedWriter(new FileWriter("subscriptions.txt"))) {
                for (int i = 0; i < subscriptionList.size(); i++) {
                    writer.write("=== Index: " + i + " ===");
                    writer.newLine();
                    writer.write(subscriptionList.get(i).display());
                    writer.newLine();
                    writer.newLine();
                }
                JOptionPane.showMessageDialog(this, "Data exported successfully to subscriptions.txt",
                        "Export Successful", JOptionPane.INFORMATION_MESSAGE);
            } catch (IOException ex) {
                JOptionPane.showMessageDialog(this, "Error writing to file: " + ex.getMessage(),
                        "Export Error", JOptionPane.ERROR_MESSAGE);
            }
        }

        // --- Load From File ---
        else if (source == btnLoad) {
            try (BufferedReader reader = new BufferedReader(new FileReader("subscriptions.txt"))) {
                StringBuilder sb = new StringBuilder();
                String line;
                while ((line = reader.readLine()) != null) {
                    sb.append(line).append("\n");
                }
                // Display in a new JFrame with JTextArea
                JFrame loadFrame   = new JFrame("Loaded Subscriptions");
                JTextArea loadArea = new JTextArea(sb.toString(), 20, 50);
                loadArea.setEditable(false);
                loadArea.setFont(new Font("Monospaced", Font.PLAIN, 12));
                loadFrame.add(new JScrollPane(loadArea));
                loadFrame.pack();
                loadFrame.setLocationRelativeTo(this);
                loadFrame.setVisible(true);
            } catch (FileNotFoundException ex) {
                JOptionPane.showMessageDialog(this, "File not found. Please export data first.",
                        "Load Error", JOptionPane.ERROR_MESSAGE);
            } catch (IOException ex) {
                JOptionPane.showMessageDialog(this, "Error reading file: " + ex.getMessage(),
                        "Load Error", JOptionPane.ERROR_MESSAGE);
            }
        }
    }

    /**
     * Main method - entry point of the application.
     * @param args Command-line arguments (not used)
     */
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new SubscriptionGUI());
    }
}
