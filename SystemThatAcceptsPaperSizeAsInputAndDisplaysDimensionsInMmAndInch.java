import java.util.Scanner;
public class SystemThatAcceptsPaperSizeAsInputAndDisplaysDimensionsInMmAndInch{
    public static void main(String[]args){
        Scanner sc=new Scanner(System.in);
        String paperSize=sc.next();
        
        switch (paperSize){
            
            case "A0":System.out.println("Dimensions in mm = 841 × 1189 mm \ninch= 33.1 × 46.8 in ");
            break;
            
            case "A1":System.out.println("Dimensions in mm = 594 × 841 mm\ninch= 23.4 × 33.1 in");
            break;
            
            case "A2":System.out.println("Dimensions in mm = 420 × 594 mm\ninch= 16.5 × 23.4 in");
            break;
            
            case "A3":System.out.println("Dimensions in mm = 297 × 420 mm\ninch= 11.7 × 16.5 in");
            break;
            
            case "A4":System.out.println("Dimensions in mm = 210 × 297 mm\ninch= 8.3 × 11.7 in");
            break;
            
            case "A5":System.out.println("Dimensions in mm = 148 × 210 mm\ninch= 5.8 × 8.3 in");
            break;
            
            default:System.out.println("Invaild paper size.");
        }
    }
}