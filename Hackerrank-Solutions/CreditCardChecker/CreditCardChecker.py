# Enter your code here. Read input from STDIN. Print output to STDOUT
from copy import deepcopy

def checksum(N,cardnumbers):
    temp1=[0]*N
    result=[0]*N
    k=0
    A=[0]*N
    B=[0]*N
    for m in cardnumbers:
        temp1[k]=[int(d) for d in str(m)]
        temp2=deepcopy(temp1)
        for i in range(len(str(m))//2):
            print(i)
            A[k]+=temp1[k][(2*i)+1]
            if ((temp1[k][(2*i)])*2 >= 10):
                temp1[k][(2*i)]=(((temp2[k][(2*i)])*2)-9)
            elif ((temp1[k][(2*i)])*2 < 10):
                temp1[k][(2*i)]=(temp2[k][(2*i)])*2
            B[k]+=temp1[k][(2*i)]
            print(temp1)
            if (A[k]+B[k])%10==0:
                result[k]='Yes'
            else:
                result[k]='No'
        print(A,B)     
        k+=1
    return(result)

if __name__ == '__main__':
    N = int(input().strip()) 

    cardnumbers=[]

    for k in range(N):
        cardnumbers.append(int(input().strip()))      

    print(checksum(N,cardnumbers))
	