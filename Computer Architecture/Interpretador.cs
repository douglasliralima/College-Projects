using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;

namespace ConsoleApp1
{
	class Interpretador
	{

		static bool exit = false;
		static int PC = 0;
		static int RA = 0;
		static int cacheHit = 0;
		static int cacheMiss = 0;
		static string[] lines;
		static string[] mem;
		static int[] regs = new int[9];

		//Tamanho da cache, conjunto, representação do bloco
		//Bloco(0) = Localizações, Bloco(1) = Valores
		static int tamanhoCache = 64;
		static int[,,] cache = new int[tamanhoCache,8,2];

		static int[] ponteirosCache = new int[tamanhoCache];

		

		static void Main(string[] args)
		{
			Console.WriteLine("Tamanho da Cache:" + cache.GetLength(0) +
				"\nTamanho do conjunto:" + cache.GetLength(1) + "\n");
			//Inicialmente vamos deixar todas as posições na cache com linhas
			//invalidas(-1) para simbolizar que não foi feito nenhum acesso
			for(int i = 0; i < cache.GetLength(0); i++){
				for(int j = 0; j < cache.GetLength(1); j++){		
					cache[i, j, 0] = -1;
				}
			}

			lines = System.IO.File.ReadAllLines(@"assemble.txt");
			mem = System.IO.File.ReadAllLines(@"memoria.txt");
			while (!exit)
			{
				//Console.WriteLine(PC);
				if (!lines[PC].Contains(":"))
				{
					//Console.WriteLine(lines[PC]);
					// for (int i = 0; i < cache.Length; i++)
					// {
					// 	foreach (List<int> el in cache[i]){
					// 		Console.WriteLine("\nAki Vemos o cojunto: " + i);
					// 		foreach (int eli in el){
                	// 			Console.Write(eli + ", ");
					// 	}
					// 	}
					// }
					
					analisaInst(lines[PC]);
				}
				PC++;
				//if (PC == 6) { exit = true; }
			}
			Console.WriteLine("CacheHit " + cacheHit);
			Console.WriteLine("CacheMiss " + cacheMiss);

			try{
				using (System.IO.StreamWriter file = new System.IO.StreamWriter(@"CacheMissHit.txt", true))
				{
					file.WriteLine(cacheHit);
					file.WriteLine(cacheMiss);
				}
			}catch(Exception e){
				Console.WriteLine(e.ToString());
			}

		}

		static void analisaInst(String inst)
		{
			string[] instT = inst.Split();

			for (int i = 0; i < instT.Length; i++)
			{
				instT[i] = instT[i].Replace(",", "");
			}


			switch (instT[0])
			{
				case "add":
					add(instT[1], instT[2], instT[3]);
					break;
				case "jal":
					jal(instT[1]);
					break;
				case "jr":
					jr();
					break;
				case "sw":
					sw(instT[1], instT[2]);
					break;
				case "lw":
					lw(instT[1], instT[2]);
					break;
				case "tam":
					tam(instT[1]);
					break;
				case "slt":
					slt(instT[1], instT[2], instT[3]);
					break;
				case "sll":
					sll(instT[1], instT[2], instT[3]);
					break;
				case "bnq":
					bnq(instT[1], instT[3]);
					break;
				case "exit":
					exit = true;
					break;
				default:
					Console.WriteLine("Instrução não encontrada");
					break;
			}
		}

		static void slt(String arg1, String arg2, String arg3)
		{
			if (arg3.Contains("$"))
			{
				if (regs[dizReg(arg2)] <= regs[dizReg(arg3)])
				{
					regs[dizReg(arg1)] = 1;
				}
				else
				{
					regs[dizReg(arg1)] = 0;
				}
			}
			else
			{
				if (regs[dizReg(arg2)] < dizReg(arg3))
				{
					regs[dizReg(arg1)] = 1;
				}
				else
				{
					regs[dizReg(arg1)] = 0;
				}
			}
		}


		static void tam(String arg1)
		{
			regs[dizReg(arg1)] = mem.Length - 1;
		}

		static void sll(String arg1, String arg2, String arg3)
		{
			regs[dizReg(arg1)] = (regs[dizReg(arg2)] * 2) * Convert.ToInt32(arg3);
		}

		static void bnq(String arg1, String arg3)
		{
			if (regs[dizReg(arg1)] != 0)
			{
				int r = procuraNoArray(arg3);
				if (r == -1)
				{
					Console.WriteLine("erro no codigo");
				}
				else
				{
					PC = r;
				}
			}
		}


		/*
		Precisamos agora, ao armazenar uma memória em um novo endereço da cache

		*/
		static void sw(String arg1, String arg2){
			//Primeiro procuramos a linha em que iremos armazenar
			arg2 = arg2.Replace(")", "");
			string[] argsment2 = arg2.Split('(');
			int linha = (Convert.ToInt32(argsment2[0]) + regs[dizReg(argsment2[1])]) / 4;

			//Depois armazenamos arg1 na linha
			string[] linhas = System.IO.File.ReadAllLines(@"memoria.txt");


			bool existe = false;
			//int linhaCache = 0; //Vai falar o local correspondente para guardar na cache
			for (int i = 0; i < linhas.Length; i++) if (i == linha) existe = true;
			//Se ela já existir, substituimos..,
			if (existe == true)
			{
				//linhaCache = linha;
				linhas[linha] = "" + regs[dizReg(arg1)];
				System.IO.File.WriteAllLines(@"memoria.txt", linhas);
				//Se não...
			}
			else
			{
				//linhaCache = linha;
				//Vamos ter que preencher com espaços vazios o arquivo
				//Até a linha que vamos escrever
				using (System.IO.StreamWriter file =
						new System.IO.StreamWriter(@"memoria.txt", true))
				{
					for (int i = linhas.Length + 1; i < linha; i++)
					{
						//linhaCache++;
						file.WriteLine("");
					}
					file.WriteLine(regs[dizReg(arg1)]);
				}
			}

			//Aqui já temos confirmado o local de onde atualmente estará o valor do bloco
			//Primeiro zeramos onde estava anteriomente na cache
			for(int i = 0; i < cache.GetLength(0); i++){
				for(int j = 0; j < cache.GetLength(1); j++){
					if(cache[i, j, 1] == regs[dizReg(arg1)]){
						cache[i, j, 1] = 0;
						cache[i, j, 0] = -1; //Setta a posição com nenhuma linha
					}
				}
			}

			//Depois repreenchemos uma nova posição igual ao que fazemos no load
			int linhaCache = linha % (cache.GetLength(0));
			
			//Posição da linha na cache
			
			cache[linhaCache, ponteirosCache[linhaCache], 0] = linha;
			//Valor da linha na cache
			cache[linhaCache , ponteirosCache[linhaCache] , 1] = Convert.ToInt32(linhas[linha]);
			ponteirosCache[linhaCache]++; //Ponteiro avança para a próxima posição
			
			//Se o ponteiro chegou ultrapassou o número de colunas ele volta para o inicio
			if(ponteirosCache[linhaCache] >= cache.GetLength(1)){
				ponteirosCache[linhaCache] = 0;
			}

			/*
			Console.WriteLine("\n\nSituação na Cache Store\n\n");
			for(int i = 0; i < cache.GetLength(0); i++){
				for(int j = 0; j < cache.GetLength(1); j++){		
					Console.Write(cache[i, j, 1] + ",");
				}
				Console.WriteLine("");
			}
			*/
		}

		static void jr()
		{
			PC = RA - 1;
		}

		//Vamos pegar carregar o valor da posição de memória referente a arg2 no compilador
		/*
		Em relação a cache:
		Ao ver qual a linha que quer ser carregada, vemos inicialmente se o valor dela já
		está na cache. Se tiver não há necessidade de buscar na memória, se não tiver
		puxa da memória e atualiza a cache 
		*/
		static void lw(String arg1, String arg2){
			bool errou = true;
			try{
				//Vamos primeiro ver a linha em nosso arquivo que queremos carregar
				arg2 = arg2.Replace(")", "");
				string[] argsment2 = arg2.Split('(');
				int linha = (Convert.ToInt32(argsment2[0]) + regs[dizReg(argsment2[1])]) / 4;				

				string[] linhas = System.IO.File.ReadAllLines(@"memoria.txt");
				//Console.WriteLine("\nValores:" + linhas[linha] + "," + linha);

				//Vamos verificar em cada linha da cache se já há uma referência
				//para a linha da memória, se houver essa refência pegamos o valor referente
				//a cache e salvamos no registrador
				for (int i = 0; i < cache.GetLength(0); i++){
					for(int j = 0; j < cache.GetLength(1); j++){
						if(cache[i,j,0] == linha ){
							//Jogamos o valor no registrador e damos cacheHit
							regs[dizReg(arg1)] = cache[i,j,1];
							errou = false; //Achou na cache
							cacheHit++; //Acertoooou
						}
					}
				}

				//Se o que ele queria não estava na cache
				if(errou){

				//Vamos precisar carregar todo o arquivo para simbolizar a leitura em memória

				//Vamos verificar se a linha existe mesmo no arquivo
				bool existe = false;
				cacheMiss++; //Contabiliza o cacheMiss
				for (int i = 0; i < linhas.Length; i++) if (i == linha) existe = true;
				//Se existir, fazemos a busca e carregamos tanto no registrador quanto na cache
				if (existe)
				{
				
					//Registrador recebe o valor direto da memória
					regs[dizReg(arg1)] = Convert.ToInt32(linhas[linha]);

					int linhaCache = linha % (cache.GetLength(0));
					//Posição da linha na cache
					cache[linhaCache, ponteirosCache[linhaCache], 0] = linha;
					//Valor da linha na cache
					cache[linhaCache , ponteirosCache[linhaCache] , 1] = Convert.ToInt32(linhas[linha]);
					ponteirosCache[linhaCache]++; //Ponteiro avança para a próxima posição
					
					//Se o ponteiro chegou ultrapassou o número de colunas ele volta para o inicio
					if(ponteirosCache[linhaCache] >= cache.GetLength(1)){
						ponteirosCache[linhaCache] = 0;
					}
					//Se não, o programa printa mensagem de erro e encerra
				}
				else
				{
					System.Console.WriteLine("Memória não alocada");
					Environment.Exit(1);
				}
			}
			}
			catch (FormatException)
			{
				System.Console.WriteLine("Memória não alocada");
				Environment.Exit(1);
			}
			catch(Exception e){

				Console.WriteLine("ERRO \n" + e.ToString());
			}
			/*
			Console.WriteLine("\n\nSituação na Cache Load\n\n");
			for(int i = 0; i < cache.GetLength(0); i++){
				for(int j = 0; j < cache.GetLength(1); j++){		
					Console.Write(cache[i, j, 1] + ",");
				}
				Console.WriteLine("");
			}
			*/
		}

		static void jal(String arg)
		{
			RA = PC + 1;
			int r = procuraNoArray(arg);
			if (r == -1)
			{
				Console.WriteLine("erro no codigo");
			}
			else
			{
				PC = r;
			}
		}

		static int dizReg(String reg)
		{
			if (!reg.Contains("$"))
			{
				return Convert.ToInt32(reg);
			}
			switch (reg)
			{
				case "$t0":
					return 0;
				case "$t1":
					return 1;
				case "$t2":
					return 2;
				case "$t3":
					return 3;
				case "$t4":
					return 4;
				case "$s0":
					return 5;
				case "$s1":
					return 6;
				case "$s2":
					return 7;
				case "$s3":
					return 8;
				default:
					Console.WriteLine("Registrador não encontrado");
					while (true) ;
			}
		}

		static int procuraNoArray(String arg)
		{
			int i;
			for (i = 0; i < lines.Length; i++)
			{
				if (lines[i].Equals(arg + ":"))
				{
					return i;
				}
			}
			return -1;
		}


		static void add(String reg, String arg2, String arg3)
		{
		
				if (!arg2.Contains("$") && arg3.Contains("$"))
				{
					if (arg3.Equals("$zero"))
					{
						regs[dizReg(reg)] = dizReg(arg2) + 0;
					}
					else
					{
						regs[dizReg(reg)] = dizReg(arg2) + regs[dizReg(arg3)];
					}
				}
				if (arg2.Contains("$") && !arg3.Contains("$"))
				{
					if (arg2.Equals("$zero"))
					{
						regs[dizReg(reg)] = 0 + dizReg(arg3);
					}
					else
					{
						regs[dizReg(reg)] = regs[dizReg(arg2)] + dizReg(arg3);
					}
				}
				if (arg2.Contains("$") && arg3.Contains("$"))
				{
					if (arg2.Equals("$zero"))
					{
						regs[dizReg(reg)] = 0 + regs[dizReg(arg3)];
					}
					if (arg3.Equals("$zero"))
					{
						regs[dizReg(reg)] = regs[dizReg(arg2)] + 0;
					}
					else
					{
						regs[dizReg(reg)] = regs[dizReg(arg2)] + regs[dizReg(arg3)];
					}
				
			}
		}


	}
}
