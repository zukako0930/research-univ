import random
import numpy as np
from scipy.sparse import lil_matrix
#from IPython.html.widgets import FloatProgress
from ipywidgets import FloatProgress
from IPython.display import display
from time import sleep

class NCTM:    
    def __init__(self, K, alpha, beta, gamma, eta, max_iter, verbose=0):
        self.K=K
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.eta = eta
        self.max_iter = max_iter
        self.verbose=verbose

    def fit(self,W,X,Vw,Vx):
        #プログレスバーの表示
        fp = FloatProgress(min=0, max=self.max_iter)
        display(fp)
        fp.value=0
        
        self._W = W
        self._X = X
        self._D = len(W)
        self._Vw = Vw # number of vocabularies
        self._Vx = Vx # number of vocabularies

        self.Z = self._init_Z()
        self.Y = self._init_Y()
        self.R = self._init_R()

        self.ndk = self._init_ndk()
        self.mdk = self._init_mdk()
        self.nkw = self._init_nkw() # for W
        self.nkx = self._init_nkx() # for x
        self.m0x = self._init_m0x() # number of noise assignment for x

        nkw_sum = self.nkw.sum(axis=1)
        nkx_sum = self.nkx.sum(axis=1)
        m0x_sum = self.m0x.sum()
        m1x_sum = nkx_sum.sum()

        remained_iter = self.max_iter
        while True:
            if self.verbose: print(remained_iter)
            for d in np.random.choice(self._D, self._D, replace=False):
                # Sample Z
                for i in np.random.choice(len(self._W[d]), len(self._W[d]), replace=False):
                    k = self.Z[d][i]
                    v = self._W[d][i]

                    self.ndk[d][k] -= 1
                    self.nkw[k][v] -= 1
                    nkw_sum[k] -= 1

                    self.Z[d][i] = self._sample_z(d,k,v,nkw_sum)

                    self.ndk[d][self.Z[d][i]] += 1
                    self.nkw[self.Z[d][i]][v] += 1
                    nkw_sum[self.Z[d][i]] += 1
            for d in np.random.choice(self._D, self._D, replace=False):
                # Sample Y
                for i in np.random.choice(len(self._X[d]), len(self._X[d]), replace=False):
                    if self.R[d][i]==1:
                        k = self.Y[d][i]
                        u = self._X[d][i]

                        self.mdk[d][k] -= 1
                        self.nkx[k][u] -= 1
                        nkx_sum[k] -= 1

                        self.Y[d][i] = self._sample_y(d,u,nkx_sum)

                        self.mdk[d][self.Y[d][i]] += 1
                        self.nkx[self.Y[d][i]][u] += 1
                        nkx_sum[self.Y[d][i]] += 1
            for d in np.random.choice(self._D, self._D, replace=False):
                # Sample R
                for i in np.random.choice(len(self._X[d]), len(self._X[d]), replace=False):
                    r = self.R[d][i]
                    k = self.Y[d][i]
                    u = self._X[d][i]

                    if r==0:
                        self.m0x[u] -= 1
                        m0x_sum -= 1
                    else:
                        self.mdk[d][k] -= 1
                        self.nkx[k][u] -= 1
                        nkx_sum[k] -= 1
                        m1x_sum -= 1

                    self.R[d][i] = self._sample_r(u,k,nkx_sum,m0x_sum,m1x_sum)

                    if self.R[d][i]==0:
                        self.m0x[u] += 1
                        m0x_sum += 1
                    else:
                        self.mdk[d][k] += 1
                        self.nkx[k][u] += 1
                        nkx_sum[k] += 1
                        m1x_sum += 1
            remained_iter -= 1
            #イテレーションと同時にプログレスバーも進める
            fp.value+=1
            if remained_iter <= 0: break
        return self

    def _init_Z(self):
        Z = []
        for d in range(len(self._W)):
            Z.append(np.random.randint(low=0,high=self.K,size=len(self._W[d])))
        return Z

    def _init_Y(self):
        Y = []
        for d in range(len(self._X)):
            Y.append(np.random.choice(self.Z[d],size=len(self._X[d])))
        return Y

    def _init_R(self):
        R = []
        for d in range(len(self._X)):
            R.append(np.random.choice([0,1],size=len(self._X[d])))
        return R

    def _init_ndk(self):
        ndk = np.zeros((self._D,self.K))
        for d in range(self._D):
            for i in range(len(self._W[d])):
                k = self.Z[d][i]
                ndk[d,k]+=1
        return ndk


    def _init_mdk(self):
        mdk = np.zeros((self._D,self.K))
        for d in range(self._D):
            for i in range(len(self._X[d])):
                #print(self._X[d])
                if self.R[d][i]==1:
                    k = self.Y[d][i]
                    mdk[d,k]+=1
        return mdk

    def _init_nkw(self):
        nkw = np.zeros((self.K,self._Vw))
        for d in range(self._D):
            for i in range(len(self._W[d])):
                k = self.Z[d][i]
                v = self._W[d][i]
                nkw[k,v]+=1
        return nkw

    def _init_nkx(self):
        nkx = np.zeros((self.K,self._Vx))
        for d in range(self._D):
            for i in range(len(self._X[d])):
                if self.R[d][i]==1:
                    k = self.Y[d][i]
                    u = self._X[d][i]
                    nkx[k,u]+=1
        return nkx

    def _init_m0x(self):
        m0x = np.zeros(self._Vx)
        for d in range(self._D):
            for i in range(len(self._X[d])):
                r = self.R[d][i]
                u = self._X[d][i]
                if r==0: m0x[u]+=1
        return m0x

    def _sample_z(self,d,old_k,v,nkw_sum):
        nkw = self.nkw[:,v] # k-dimensional vector

        if self.ndk[d,old_k]==0 and self.mdk[d,old_k]>0:
            return old_k
        else:
            ndk = self.ndk[d].copy()
            ndk[ndk==0] += 1
            prob = (self.ndk[d]+self.alpha) * ((nkw+self.beta)/(nkw_sum+self.beta*self._Vw)) * ((ndk+1)/ndk)**self.mdk[d]
            prob = prob/prob.sum()
            z = np.random.multinomial(n=1, pvals=prob).argmax()
            return z

    def _sample_y(self,d,u,nkx_sum):
        nkx = self.nkx[:,u] # k-dimensional vector

        prob = self.ndk[d] * ((nkx+self.gamma)/(nkx_sum+self.gamma*self._Vx))
        prob = prob/prob.sum()
        y = np.random.multinomial(n=1, pvals=prob).argmax()
        return y

    def _sample_r(self,u,k,nkx_sum,m0x_sum,m1x_sum):
        nkx = self.nkx[k,u]
        p0 = (m0x_sum+self.eta) * ((self.m0x[u]+self.gamma)/(m0x_sum+self.gamma*self._Vx))
        p1 = (m1x_sum+self.eta) * ((nkx+self.gamma)/(nkx_sum[k]+self.gamma*self._Vx))
        p = p1/(p1+p0)
        r = np.random.multinomial(n=1, pvals=[1-p,p]).argmax()
        return r