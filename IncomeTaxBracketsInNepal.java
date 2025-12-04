import java.util.Scanner;
public class IncomeTaxBracketsInNepal{
    public static void main(String[]args){
        Scanner sc=new Scanner(System.in);
        double annualIncome=sc.nextDouble();
        double tax=0;
        if(annualIncome<=500000){
            tax=(annualIncome*0.01);
        }else if(annualIncome<=700000){
            tax=5000+(annualIncome-500000)*0.10;
        }else if(annualIncome<=1000000){
            tax=15000+(annualIncome-700000)*0.20;
        }else if(annualIncome<=2000000){
            tax=15000+(annualIncome-1000000)*0.30;
        }else if(annualIncome<=5000000){
            tax=15000+(annualIncome-2000000)*0.36;
        }else if(annualIncome<5000000){
            tax=15000+(annualIncome-5000000)*0.39;
        }
        System.out.println("Amount you need to pay="+tax);
    }
}