/**
 * PersonalPlan - Child class of AIModel representing a personal subscription plan.
 * Provides limited monthly prompt quota for recreational users.
 * @author Student
 */
public class PersonalPlan extends AIModel {

    // Attribute
    private int promptsRemaining; // Number of prompts remaining in monthly quota

    /**
     * Constructor for PersonalPlan.
     * @param modelName      Name of the AI model
     * @param price          Price per 1 Lakh tokens (NPR)
     * @param parameterCount Number of parameters in billions
     * @param contextWindow  Context window size
     * @param promptsRemaining Initial number of prompts in monthly quota
     */
    public PersonalPlan(String modelName, double price, int parameterCount,
                        String contextWindow, int promptsRemaining) {
        super(modelName, price, parameterCount, contextWindow);
        this.promptsRemaining = promptsRemaining;
    }

    // Accessor Method

    /**
     * Returns the number of prompts remaining in the monthly quota.
     * @return promptsRemaining
     */
    public int getPromptsRemaining() {
        return promptsRemaining;
    }

    /**
     * Allows user to purchase additional prompts.
     * Adds to the monthly quota if the value is positive; returns error message otherwise.
     * @param additionalPrompts Number of additional prompts to purchase
     * @return Result message
     */
    public String purchasePrompts(int additionalPrompts) {
        if (additionalPrompts < 0) {
            return "Error: You must enter a positive value. Consider upgrading to a Pro Plan.";
        }
        promptsRemaining += additionalPrompts;
        return "Successfully added " + additionalPrompts + " prompts. Total remaining: " + promptsRemaining;
    }

    /**
     * Simulates the user entering a prompt.
     * Checks if prompts are available; reduces quota by 1 if so.
     * @param promptText     The text of the prompt
     * @param responseLength Expected response length in tokens
     * @return Result message with prompt details or quota-exceeded message
     */
    public String enterPrompt(String promptText, int responseLength) {
        if (promptsRemaining > 0) {
            promptsRemaining--;
            return "Prompt submitted successfully!" +
                    "\nPrompt: " + promptText +
                    "\nExpected Response Length: " + responseLength + " tokens" +
                    "\nPrompts Remaining: " + promptsRemaining;
        } else {
            return "Monthly prompt limit reached. Please purchase more prompts or upgrade to Pro Plan.";
        }
    }

    /**
     * Displays details of the PersonalPlan, including parent class details.
     * Overrides the parent display() method.
     * @return Formatted string with all PersonalPlan details
     */
    @Override
    public String display() {
        return super.display() +
                "\nPlan Type: Personal Plan" +
                "\nPrompts Remaining (Monthly Quota): " + promptsRemaining;
    }
}