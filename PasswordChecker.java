import java.util.Scanner;
public class PasswordChecker{
    public static void main(){
        Scanner sc=new Scanner(System.in);
        String correctPass="Java123";
        
        for(int i=1;i<=3;i++){
            System.out.println("Enter Password:");
            String pass=sc.nextLine();
            
            if(pass.equals(correctPass)){
                System.out.println("Login Sucessful!");
                break;
            }
            System.out.println("Wrong Password.");
        }
    }
}