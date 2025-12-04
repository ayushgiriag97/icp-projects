import java.util.Scanner;
public class SellingPriceCalculator{
    public static void main(String[]args){
        Scanner sc=new Scanner(System.in);
        System.out.println("Enter your marked price and its category labeled in the item.");
        double markedPrice=sc.nextDouble();
        char category=sc.next().charAt(0);
        
        switch(category){
            case 'A':markedPrice=markedPrice -(markedPrice*0.60);
            System.out.println("New marked price="+markedPrice);
            break;
            case 'B':markedPrice=markedPrice -(markedPrice*0.40);
            System.out.println("New marked price="+markedPrice);
            break;
            case 'C':markedPrice=markedPrice -(markedPrice*0.20);
            System.out.println("New marked price="+markedPrice);
            break;
            case 'D':markedPrice=markedPrice -(markedPrice*10);
            System.out.println("New marked price="+markedPrice);
            break;
            default:System.out.println("Invaild category.");
        }
    }
}