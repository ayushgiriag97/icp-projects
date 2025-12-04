import java.util.Scanner;
public class JavaClass{
 public static void main(String[]args){
     //First question using loop where we create the code to find out the user is adult or not.
     System.out.print("Enter your age:");
     Scanner sc=new Scanner(System.in);
     int age=sc.nextInt();
     

     
     if (age>=18){
         System.out.print("Adult");
     }else{
         System.out.print("Not Adult");
     }
     System.out.print("\n");
     
     
     
     //Second quesion where we are finding out if the number is odd or even.
     System.out.print("Enter number to find out if your number is even or odd.");
     int number=sc.nextInt();
     
     if(number%2==0){
         System.out.println("EVEN");
     }else{
         System.out.println("ODD");
     }
     System.out.print("\n");
     
     
     //Third question where we are finding out the relationship between the numbers.
     System.out.println("Enter two numbers to find out their relation.");
     int firstNumber=sc.nextInt();
     int secondNumber=sc.nextInt();
     
     if(firstNumber==secondNumber){
         System.out.print("They are equal.");
     }else if (firstNumber>secondNumber){
         System.out.print("firstNumber is greater");
     }else {
         System.out.print("firstNumber is lesser");
     }
     System.out.print("\n");
     
     //fourth question is about the buttom which on presssing gives greetings 
     
     System.out.println("Press any one buttom for greetings:");
     int buttom=sc.nextInt();
     
     if(buttom==1){
         System.out.println("Hello");
     }else if(buttom==2){
         System.out.println("Namaste");
     }else if(buttom==3){
         System.out.print("Bonjure");
     }else{
         System.out.println("Invaild buttom");
     }
     System.out.print("\n");
     //Fifth same as fourth but we are using switch case.
     
     System.out.println("Press the button for the greetings.");
     int Button=sc.nextInt();
     
     switch(Button){
         case 1:System.out.println("Hello");
         break;
         case 2:System.out.println("Namaste");
         break;
         case 3:System.out.println("Bonjure");
         break;
         default:System.out.println("Invaild Button");
     }
 }
}