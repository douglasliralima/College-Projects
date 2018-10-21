using System;
using System.Diagnostics; //Necessário para usar o Stack Trace

namespace ConsoleApp1
{
	class PreencheMemoria
	{
		//Para forçar um erro	
		static int[] arrayzinho = new int[4];

		

		static void Main(string[] args)
		{
			int valor = 250;
			try{
				using (System.IO.StreamWriter file =
						new System.IO.StreamWriter(@"memoria.txt", true))
				{
					for(int i = valor; i >= 1; i--)
					{
						file.WriteLine(i);
					}
				}
			}catch(Exception e){
				Console.WriteLine(e.ToString());
			}
		}
	}
}