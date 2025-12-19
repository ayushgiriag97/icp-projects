/**
 * Create "FixedDepositNIB.java":
• Perform multiple FD calculations using a while loop
• Interest rates: 8–12% (current Nepal rates)
• Monthly compound interest calculation
• Minimum deposit: Rs. 1000, maximum duration: 5 years
• Include 0.5% processing fee in calculations
 */

import java.util.*;
public class FixedDepositNIB{
    public static void main(String[]args){
        Scanner sc=new Scanner(System.in);
        System.out.println("Enter your name =");
        String nameOfAccHolder=sc.nextLine();
        System.out.println("\n");
        
        System.out.println("Amount =");
        int principle=sc.nextInt();
        if(principle<=1000){
         System.out.println("Amount ="+principle);
        }else
        {
        System.out.println("Minimum deposit: Rs. 1000");
        
        }
        System.out.println("\n");
        
        System.out.println("Duration="); 
        int time=sc.nextInt();
        if(time>=5){
           System.out.println("Duration="+time); 
        }else{
            System.out.println("Maximum duration: 5 years");
        }
        System.out.println("\n");
        
        float rate=2.75f;
        int n=12; //the number of times that interest is compounded per year
        double Amount;
        Amount=(principle+Math.pow(1+(rate/n),n*time));
        
        double fee=Amount*0.005;
        double finalAmount=Amount-fee;
        System.out.println("Amount="+finalAmount);
    }
}