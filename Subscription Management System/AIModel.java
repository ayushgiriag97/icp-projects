/**
 * AIModel - Parent class representing an AI model with subscription details.
 * @author Student
 */
public class AIModel {

    // Attributes
    private String modelName;
    private double price;          // in Nepali Rupees per 1 Lakh tokens
    private int parameterCount;    // in billions
    private String contextWindow;  // e.g., "64K"

    /**
     * Constructor for AIModel.
     * @param modelName     Name of the AI model
     * @param price         Price per 1 Lakh tokens (NPR)
     * @param parameterCount Number of parameters in billions
     * @param contextWindow Context window size (e.g., "64K")
     */
    public AIModel(String modelName, double price, int parameterCount, String contextWindow) {
        this.modelName = modelName;
        this.price = price;
        this.parameterCount = parameterCount;
        this.contextWindow = contextWindow;
    }

    // Accessor Methods

    /**
     * Returns the model name.
     * @return modelName
     */
    public String getModelName() {
        return modelName;
    }

    /**
     * Returns the price per 1 Lakh tokens.
     * @return price
     */
    public double getPrice() {
        return price;
    }

    /**
     * Returns the parameter count in billions.
     * @return parameterCount
     */
    public int getParameterCount() {
        return parameterCount;
    }

    /**
     * Returns the context window size.
     * @return contextWindow
     */
    public String getContextWindow() {
        return contextWindow;
    }

    /**
     * Displays the details of the AIModel.
     * @return A formatted string with model details
     */
    public String display() {
        return "Model Name: " + modelName +
                "\nPrice (per 1 Lakh tokens): NPR " + price +
                "\nParameter Count: " + parameterCount + " billion" +
                "\nContext Window: " + contextWindow;
    }
}