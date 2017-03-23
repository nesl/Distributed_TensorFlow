package servlet.tf;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.PrintWriter;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 * Servlet implementation class Run_TF_servlet
 */
@WebServlet("/Run_TF_servlet")
public class Run_TF_servlet extends HttpServlet {
	private static final long serialVersionUID = 1L;
    
	String outfile="/home/sandeep/tensorflow/programs/parallel_programs/out.txt";
	String inputfile="/home/sandeep/tensorflow/programs/parallel_programs/job2.py";
	
    /**
     * @see HttpServlet#HttpServlet()
     */
    public Run_TF_servlet() {
        super();
        // TODO Auto-generated constructor stub
    }

	/**
	 * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
	
		
		
	}

	/**
	 * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
	
		 String command = "python "+inputfile;
		 Process proc=null;
		 String proc_output="";
		 
         try{		 
		 proc = Runtime.getRuntime().exec(command);
		 
	     
		 BufferedReader readerproc =  
                 new BufferedReader(new InputStreamReader(proc.getInputStream()));

       
          
          // line = readerproc.readLine();
           String line="";
	        while((line = readerproc.readLine()) != null) {
	        	
	        	
	        	proc_output=proc_output+line;
	            System.out.println("While:--"+line);
	        }
	        
		 
	     proc.waitFor(); 
	     
	     
	     
		 
         }
         catch(Exception e)
         {
        	 e.printStackTrace();
         }
         
         
         //reading ouputfile in /home/sandeep/tensorflow/programs/parallel_programs/out.txt
        
         String file_data="";
         
         /*
         BufferedReader br = new BufferedReader(new FileReader(outfile));
         try {
        	    StringBuilder sb = new StringBuilder();
        	    String line = br.readLine();

        	    while (line != null) {
        	        sb.append(line);
        	        sb.append(System.lineSeparator());
        	        line = br.readLine();
        	    }
        	    file_data = sb.toString();
        	} finally {
        	    br.close();
        	}
         */
         
         response.setContentType("text/html");
         PrintWriter out = response.getWriter();
         out.println("<title>Results</title>" +
        	       "<body bgcolor=FFFFFF>");
         
         out.println("<h2>Results of Graph</h2>");
         
         out.println("<p>"+file_data+" "+proc_output+"</p>");
         
         out.println("</body>");
         
         out.close();
         
         
         
	}//end post

}
