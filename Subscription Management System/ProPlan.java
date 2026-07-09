/**
 * ProPlan - Child class of AIModel representing a professional/team subscription plan.
 * Provides team collaboration features with member slots.
 * @author Student
 */
public class ProPlan extends AIModel {

    // Attribute
    private int teamSlots; // Available team member slots

    /**
     * Constructor for ProPlan.
     * @param modelName      Name of the AI model
     * @param price          Price per 1 Lakh tokens (NPR)
     * @param parameterCount Number of parameters in billions
     * @param contextWindow  Context window size
     * @param teamSlots      Initial number of available team member slots
     */
    public ProPlan(String modelName, double price, int parameterCount,
                   String contextWindow, int teamSlots) {
        super(modelName, price, parameterCount, contextWindow);
        this.teamSlots = teamSlots;
    }

    // Accessor Method

    /**
     * Returns the number of available team slots.
     * @return teamSlots
     */
    public int getTeamSlots() {
        return teamSlots;
    }

    /**
     * Adds a team member if slots are available.
     * Decreases available team slots by 1.
     * @param memberName Name of the team member to add
     * @return Success or error message
     */
    public String addTeamMember(String memberName) {
        if (teamSlots > 0) {
            teamSlots--;
            return "Team member '" + memberName + "' added successfully. Slots remaining: " + teamSlots;
        } else {
            return "Error: No available team slots. Please upgrade your plan.";
        }
    }

    /**
     * Removes a team member and increases available team slots by 1.
     * @param memberName Name of the team member to remove
     * @return Confirmation message
     */
    public String removeTeamMember(String memberName) {
        teamSlots++;
        return "Team member '" + memberName + "' removed successfully. Slots available: " + teamSlots;
    }

    /**
     * Displays details of the ProPlan, including parent class details.
     * Overrides the parent display() method.
     * @return Formatted string with all ProPlan details
     */
    @Override
    public String display() {
        return super.display() +
                "\nPlan Type: Pro Plan" +
                "\nAvailable Team Slots: " + teamSlots;
    }
}
