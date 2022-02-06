# %%
from random import randint, uniform

# %%
def add_two(mat):
    a = randint(0, len(mat)-1) # Choose any x
    b = randint(0, len(mat)-1) # Choose any y

    while(mat[a][b]!=0):  # If the x,y coord is occupied, try again and again
        a = randint(0,len(mat)-1)
        b = randint(0,len(mat)-1)

    # 10% chance that the number will be 4 instead of 2. 
    mat[a][b] = (uniform(0, 1) < 0.1)*2 + 2  

    return mat

def reverse(mat):
    new=[]
    for i in range(len(mat)):
        new.append([])
        for j in range(len(mat[0])):
            new[i].append(mat[i][len(mat[0])-j-1])
    return new

def transpose(mat):
    new=[]
    for i in range(len(mat[0])):
        new.append([])
        for j in range(len(mat)):
            new[i].append(mat[j][i])
    return new

def cover_up(mat):
    new = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    done = False
    for i in range(4):
        count=0
        for j in range(4):
            if mat[i][j]!=0:
                new[i][count]=mat[i][j]
                if j!=count:
                    done=True
                count+=1
    return new, done

def merge(mat):
    done = False
    addPoints = 0
    for i in range(4):
         for j in range(3):
             if mat[i][j]==mat[i][j+1] and mat[i][j]!=0:
                 mat[i][j]*=2
                 addPoints += mat[i][j]
                 mat[i][j+1]=0
                 done=True
    return mat, done, addPoints
