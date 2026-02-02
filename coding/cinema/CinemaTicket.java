import java.util.Scanner;
public class CinemaTicket{
    public static void main(String[]args){
            
            
            //Used Scanner to get input from user.
            
            Scanner sc=new Scanner(System.in);
            
            // ageGroup (e.g., "Child", "Adult", "Senior")
            System.out.println("Enter your age group: \nChild(0–12) \nAdult(13–64) \nSenior(65+)");
            String ageGroup=sc.next().toUpperCase();
            System.out.println("\n");
            
            
            // movieLanguage (e.g., "Nepali", "Hindi", "English")
            System.out.println("Enter a movie language you prefere:(e.g., 'Nepali', 'Hindi', 'English')");
            String movieLanguage=sc.next().toUpperCase();
            System.out.println("\n");
            
            
            // isStudent (true/false)
            System.out.println("If you are student select True otherwise false:");
            boolean isStudent=sc.nextBoolean();
            System.out.println("\n");
            
            
            // isFestival (true/false)
            
            System.out.println("If today is festival select True otherwise false:");
            boolean isFestival=sc.nextBoolean();
            System.out.println("\n");
            
            
            // TODO: Declared variables for base price and final price
            double basePrice=0;
            
            
            //Adding base price in age group.
            
            
            if(ageGroup.equals("CHILD")){
                basePrice=150;
            }else if (ageGroup.equals("ADULT")){
                basePrice=300;
            }else if (ageGroup.equals("SENIOR")){
                basePrice=200;
            }else{
                System.out.println("Invaild age group!"); 
            }
            
            
            //Adding surcharge from movie language
            
            if(movieLanguage.equals("NEPALI")){
                basePrice+=50;
            }else if(movieLanguage.equals("ENGLISH")){
                basePrice+=60;
            }else if(movieLanguage.equals("HINDI")){
                basePrice+=70;
            }else{
                System.out.println("Invaild age Language!"); 
            }
            
            
            //Applying student discount
            
            if(isStudent){
                basePrice-=(basePrice)*0.10;
            }else{
                basePrice=basePrice;
            }
            
            
            //Applying festival discount
            
            if(isFestival){
                basePrice-=(basePrice)*0.10;
            }else{
                basePrice=basePrice;
            }
            
            System.out.print("Your ticket price is:"+basePrice);
   }
}