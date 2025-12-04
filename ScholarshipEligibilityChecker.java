import java.util.Scanner;
public class ScholarshipEligibilityChecker{
public static void main(String[]args){
    Scanner sc=new Scanner(System.in);
    
    
    System.out.println("Enter your details.");
    System.out.println("\n");
    
    System.out.println("Enter your GPA:");
    float gpa=sc.nextFloat();
    
    System.out.println("Enter your Attandance:");
    int Attendance=sc.nextInt();
    
    System.out.println("Enter your attitude score:");
    int attitudeScore=sc.nextInt();
    
    if(gpa>=3.2){
        if(Attendance>80){
            if(attitudeScore>5){
                System.out.println("Congratulation you are eigible for scholarship.");
            }
            else
               {
                System.out.println("DID NOT MET THE THRESHOLD.");
               }
        }
               else
               {
                System.out.println("DID NOT MET THE THRESHOLD.");
               }
    }
    else
               {
                System.out.println("DID NOT MET THE THRESHOLD.");
               }
}
}    