import java.util.Scanner;
public class ClassRoutineByDay{
    public static void main(){
        Scanner sc=new Scanner(System.in);
        String day=sc.next();
        
        switch(day){
            
            case "Sunday":System.out.println("Lecture:CHASA,Programming");
            break;
            case "Monday":System.out.println("Lecture:IS,logic");
            break;
            case "Tuesday":System.out.println("Tutorial:CHASA,Programming");
            break;
            case "Wednesday":System.out.println("Tutorial:IS,logic");
            break;
            case "Thursday":System.out.println("Workshop:CHASA,Programming");
            break;
            case "Friday":System.out.println("Workshop:IS,logic");
        }
    }
}