import java.util.Scanner;
public class JavaClass1{
    public static void main(String[]args){
        
        System.out.println("using forvloop to print upto 11.");
        for(int i=0;i<11;i++){
            System.out.println(""+i);
        }
        
        
        System.out.println("using while loop to print upto 21.");
        int x=11;
        while(x<22){
            System.out.println(""+x);
            x++;
        }
        
        System.out.println("using do while loop to print upto 31.");
        int y=22;
        do{
        System.out.println(""+y);
        y++;
        }while(y<32);
        System.out.println("\n");
        
        
        
        System.out.println("Printing the sum of first n Natural Number.");
        System.out.println("\n");
        Scanner sc=new Scanner(System.in);
        System.out.println("Enter a natural number for sum.");
        int naturalNumber=sc.nextInt();
        int sum=0;
        for(int i=1;i<=naturalNumber;i++){
            sum=sum+i;
        }
        System.out.println("Sum of natural number is:"+sum);
        System.out.println("\n");
        
        
        System.out.println("Generating table based on user input.");
        System.out.println("\n");
        System.out.println("Enter a number to generate its table:");
        int number=sc.nextInt();
        for(int i=1;i<=10;i++){
            System.out.println(""+number*i);
        }
    }
}