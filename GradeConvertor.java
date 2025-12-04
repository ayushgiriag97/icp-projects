import java.util.Scanner;
public class GradeConvertor{
    public static void main(String[]args){
        
        System.out.println("Enter your GPA to know your Grade.");
        
        
        System.out.println("Enter your GPA:");
        Scanner sc= new Scanner(System.in);
        float gpa= sc.nextFloat();
        
        
        if(gpa>=3.65){
            System.out.println("Congratulations for securing grade 'A+'");
        }else if(gpa>=3.2){
            System.out.println("Congratulations for securing grade 'A'");
        }else if(gpa>=2.8){
            System.out.println("Congratulations for securing grade 'B+'");
        }else if(gpa>=2.4){
            System.out.println("Congratulations for securing grade 'B'");
        }else if(gpa>=2.0){
            System.out.println("Congratulations for securing grade 'C+'");
        }else if(gpa>=1.6){
            System.out.println("Congratulations for securing grade 'C'");
        }else if(gpa>=0.8){
            System.out.println("Congratulations for securing grade 'D'");
        }if(gpa<=0.8){
            System.out.println("NG");
        }
    }
}