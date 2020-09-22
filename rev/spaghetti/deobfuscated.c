#include<stdio.h>
#include<stdlib.h>
#include<stdint.h>
#include<string.h>
#include<unistd.h>

#define BUF_SIZE 2048

static inline void wrapper(uint32_t *eax,uint32_t *ebx,uint32_t *ecx,uint32_t *edx)
{
	asm volatile (
		"cpuid"      //AssemblerTemplate
		
		:"=a"(*eax), //OutputOperands
		 "=b"(*ebx),
		 "=c"(*ecx),
		 "=d"(*edx)
		
		:"0"(*eax),  //InputOperands
		 "2"(*ecx)
	);
}

void win(void)
{
	FILE *file;
	char buf[255];
	file=fopen("flag.txt","r");
	if(!file)
		return;
	fscanf(file,"%s",buf);
	printf("%s\n",buf);
	fclose(file);
}

int main(intargc,char*argv[])
{
	setvbuf(stdout,NULL,_IONBF,0);
	
	uint32_t eax;
	eax=0;
	char input[17];
	
	fgets(input,sizeof(input),stdin);
	char *buf = malloc(sizeof(char)*17);
	
	buf[0]='C';
	buf[1]='P';
	buf[2]='U';
	buf[3]=':';
	wrapper(&eax,(uint32_t*)&buf[4],(uint32_t*)&buf[12],(uint32_t*)&buf[8]);
	buf[16]='\0';
	
	if(strncmp(buf,input,17)==0)
		win();
		
	free(buf);
	return 0;
}


