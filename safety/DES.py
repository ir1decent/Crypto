import random
import os

# fmt: off
# 密钥置换选择 1
key_table1 = [56, 48, 40, 32, 24, 16, 8, 0, 57, 49, 41, 33, 25, 17, 9,  1, 58, 50, 42, 34, 26, 18, 10,  2, 59, 51, 43, 35, 62, 54, 46, 38, 30, 22, 14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 60, 52, 44, 36, 28, 20, 12,  4, 27, 19, 11,  3]
# 密钥置换选择 2
key_table2 = [13, 16, 10, 23, 0, 4, 2, 27, 14, 5, 20, 9, 22, 18, 11, 3, 25, 7, 15, 6, 26, 19, 12, 1, 40, 51, 30, 36, 46, 54, 29, 39, 50, 44, 32, 47, 43, 48, 38, 55, 33, 52, 45, 41, 49, 35, 28, 31]
# 初始置换 IP
IP = [57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3, 61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7, 56, 48, 40, 32, 24, 16, 8,  0, 58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4, 62, 54, 46, 38, 30, 22, 14, 6]
# 逆初始置换
IP_1 = [39, 7, 47, 15, 55, 23, 63, 31, 38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29, 36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27, 34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41,  9, 49, 17, 57, 25, 32, 0, 40, 8, 48, 16, 56, 24]
# 选择扩展运算 E
E = [31, 0, 1, 2, 3, 4, 3, 4, 5, 6, 7, 8, 7, 8, 9, 10, 11, 12, 11, 12, 13, 14, 15, 16, 15, 16, 17, 18, 19, 20, 19, 20, 21, 22, 23, 24, 23, 24, 25, 26, 27, 28, 27, 28, 29, 30, 31, 0]
# 置换运算 P
P = [15, 6, 19, 20, 28, 11, 27, 16, 0, 14, 22, 25, 4, 17, 30, 9, 1, 7, 23, 13, 31, 26, 2, 8, 18, 12, 29, 5, 21, 10, 3, 24]
# S盒
sbox = [
# S1
[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7,
0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8,
4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0,
15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],
# S2
[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10,
3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5,
0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15,
13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
# S3
[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8,
13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1,
13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7,
1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],

# S4
[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15,
13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9,
10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4,
3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],

# S5
[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9,
14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6,
4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14,
11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],

# S6
[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11,
10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8,
9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6,
4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],

# S7
[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1,
13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6,
1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2,
6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],

# S8
[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7,
1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2,
7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8,
2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
]

#循环左移位数
l=[1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

#需要传输的明文
#key_bin的奇偶校验检查
def check(key_bin):
	for i in range(0,64,8):
		xor=int(key_bin[i])^int(key_bin[i+1])^int(key_bin[i+2])^int(key_bin[i+3])^int(key_bin[i+4])^int(key_bin[i+5])^int(key_bin[i+6])
		if xor!=int(key_bin[i+7]):
			return False
	return True
#密钥置换选择1
def key_ex1(key):
	s=''
	for i in key_table1:
		s+=key[i]
	return s
#密钥置换选择2
def key_ex2(key):
    s=''
    for i in key_table2:
        s+=key[i]
    return s
#密钥循环左移
def key_ml(key,r):
    # print('key=',key,'len=',len(key))
    s=key
    for i in range(l[r]):
    	s=s[1:]+s[:1]
    # print('s=',s,'len=',len(s))
    return s
#获取全部的子密钥   
def get_wholekey(key_bin):
	key=[]
	#密钥置换选择1
	key1_res=key_ex1(key_bin)
	# print(key1_res,len(key1_res))
	L=key1_res[:28]
	R=key1_res[28:]
	# print('l=',L,len(L))
	# print('r=',R,len(R))
	for i in range(16):
		#循环左移
		L=key_ml(L,i)
		R=key_ml(R,i)
		#密钥置换选择2
		key.append(key_ex2(L+R))
	print('16 keys activate successfully！')
	return key

#扩展置换E
def extend_E(R):
	r=''
	for i in E:
		r+=R[i]
	return r
#代换选择S盒
def alter_s(t):
	j=0
	res=''
	for i in range(0,48,6):
		c=int(t[i+1:i+5],2)
		r=int(t[i]+t[i+5],2)
		res+='{:04b}'.format((sbox[j][r*16+c]))
		j+=1
	#print(res)
	return res
#P置换
def p_repl(s):
	p=''
	for i in P:
		p+=s[i]
	return p

def DES(M,key):#DES加密
	#首先将明文进行初始置换IP
	m=''
	for i in IP:
		m+=M[i]
	L=[]
	R=[]
	#print('m=',m)
	L.append(m[:32])
	R.append(m[32:])
	#16轮结构
	for i in range(16):
		print(i,'round:')
		L.append(R[i])
		#将R进行扩展置换E
		R_extend=extend_E(R[i])
		#异或子密钥 K(i)
		#print('r=',R_extend)
		t=''
		for j in range(48):
			t+=str(int(R_extend[j])^int(key[i][j]))
		print('t=',t,'  48 Digits')
		#代换选择S盒
		s=alter_s(t)
		#print('s=',s)
		#P置换
		p=p_repl(s)
		#异或L(i-1)
		# print('p=', p)
		r=''
		for j in range(32):
			r+=str(int(p[j])^int(L[i][j]))
		R.append(r)
		print('32left+32right',L[i],R[i])
	#左右交换
	c=R[16]+L[16]
	#逆初始置换
	cipher=''
	for i in IP_1:
		cipher+=c[i]
	return cipher

def get_rand_key():
	#随机生成密钥
	key_seed=os.urandom(8)	#随机获取8个字符
	random_KEY=''
	for i in key_seed:
		binstr='{:07b}'.format(i)
		xor=int(binstr[0])^int(binstr[1])^int(binstr[2])^int(binstr[3])^int(binstr[4])^int(binstr[5])^int(binstr[6])
		for i in range(7):
			random_KEY+=str(binstr[i])
		random_KEY+=str(xor)
	print('random key: ',random_KEY,'  ',len(random_KEY),'Digits')		
	return random_KEY
			
def DES_encrypto(message,key):
	#print('64digits key：',key)
	if check(key)==False:
		print('test not pass！')
		return 
	print('test pass！')
	#将明文转成64位
	key=get_wholekey(key)
	print('Plaintext：',message)
	M=''
	for i in message:
		M+='{:08b}'.format(ord(i))
	print('Plaintext in bin：     ',M,'   ',len(M),'Digits')
	ciphertext=DES(M,key)
	print('Encrypted txet in bin：',ciphertext,'   ',len(ciphertext),'Digits')
	return ciphertext,key

def DES_decrypto(ciphertext,key):
	plainbin=DES(ciphertext,key)
	print('Decrypted text in bin：',plainbin,'   ',len(plainbin),'Digits')
	plaintext=''
	for i in range(0,64,8):
		plaintext+=chr(int(plainbin[i:i+8],2))
	print('Decrypted plaintext：',plaintext)

key_bin=get_rand_key()
message='Hellodes'

ciphertext,key=DES_encrypto(message,key_bin)
key=key[::-1]
DES_decrypto(ciphertext,key)
