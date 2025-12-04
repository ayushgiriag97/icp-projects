public class PatternsQuestionsInJava{
    public static void main(String[]args){
        System.out.println("Printing solid rectangle");
        System.out.println("\n");
        int n=4;
        int m=5;
        //Outer loop. 
        for(int i=1;i<=n;i++){
            //inner loop.
            for(int j=1;j<=m;j++){
                System.out.print("*");
            }
            System.out.println("");
        }
        
        
        System.out.println("Printing solid hollow rectangle");
        System.out.println("\n");
        
        for(int i=1;i<=n;i++){
            for(int j=1;j<=m;j++){
                if(i==1||j==1||i==n||j==m){
                    System.out.print("*");
                }else{
                    System.out.print(" ");
                }
                
            }
            System.out.println("");
        }
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
        
        
        
    }
}